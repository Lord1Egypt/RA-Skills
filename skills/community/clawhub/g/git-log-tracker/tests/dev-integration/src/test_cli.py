"""cli 模块 dev-integration 测试。

- hook 管理命令（install/uninstall/status）使用真实临时 git 仓库
- 查询命令（find/list/stats/delete/update）使用真实 SQLite + 预填数据
- global 命令 mock subprocess，避免污染真实全局 git 配置
"""

from types import SimpleNamespace

import db
import cli


def _insert(db_path, **over):
    """向 commits 表插入一行，返回 commit_hash。"""
    fields = {
        "commit_hash": "a" * 40,
        "short_hash": "aaaaaaa",
        "author_name": "Alice",
        "author_email": "alice@example.com",
        "author_ts": "2026-06-01T12:00:00+08:00",
        "committer_name": "Alice",
        "committer_email": "alice@example.com",
        "commit_subject": "feat: 初始提交",
        "commit_body": "正文",
        "branch": "master",
        "repo_path": "/data/r1",
        "repo_name": "r1",
        "parent_hashes": None,
    }
    fields.update(over)
    conn = db.get_connection(db_path)
    try:
        conn.execute(
            "INSERT INTO commits (commit_hash, short_hash, author_name, author_email, "
            "author_ts, committer_name, committer_email, commit_subject, commit_body, "
            "branch, repo_path, repo_name, parent_hashes) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            tuple(fields[k] for k in (
                "commit_hash", "short_hash", "author_name", "author_email",
                "author_ts", "committer_name", "committer_email", "commit_subject",
                "commit_body", "branch", "repo_path", "repo_name", "parent_hashes",
            )),
        )
        conn.commit()
    finally:
        conn.close()
    return fields["commit_hash"]


# ---------------------------------------------------------------------------
# Hook 管理命令（真实 git 仓库）
# ---------------------------------------------------------------------------

class TestHookManagement:
    def test_install_creates_hook(self, git_repo, capsys):
        cli.cmd_install(SimpleNamespace(repo=str(git_repo)))
        hook_file = git_repo / ".git" / "hooks" / "post-commit"
        assert hook_file.exists()
        assert cli.MARKER_BEGIN in hook_file.read_text(encoding="utf-8")
        assert "created" in capsys.readouterr().out.lower()

    def test_install_twice_idempotent(self, git_repo, capsys):
        cli.cmd_install(SimpleNamespace(repo=str(git_repo)))
        capsys.readouterr()
        cli.cmd_install(SimpleNamespace(repo=str(git_repo)))
        assert "already installed" in capsys.readouterr().out

    def test_install_appends_to_existing_hook(self, git_repo, capsys):
        hook_file = git_repo / ".git" / "hooks" / "post-commit"
        hook_file.write_text("#!/bin/sh\necho existing\n", encoding="utf-8")
        cli.cmd_install(SimpleNamespace(repo=str(git_repo)))
        content = hook_file.read_text(encoding="utf-8")
        assert "echo existing" in content
        assert cli.MARKER_BEGIN in content
        assert "appended" in capsys.readouterr().out.lower()

    def test_status_reflects_install(self, git_repo, capsys):
        cli.cmd_status(SimpleNamespace(repo=str(git_repo)))
        assert "not installed" in capsys.readouterr().out
        cli.cmd_install(SimpleNamespace(repo=str(git_repo)))
        capsys.readouterr()
        cli.cmd_status(SimpleNamespace(repo=str(git_repo)))
        assert "installed" in capsys.readouterr().out

    def test_uninstall_removes_our_hook_only(self, git_repo, capsys):
        hook_file = git_repo / ".git" / "hooks" / "post-commit"
        hook_file.write_text("#!/bin/sh\necho existing\n", encoding="utf-8")
        cli.cmd_install(SimpleNamespace(repo=str(git_repo)))
        capsys.readouterr()
        cli.cmd_uninstall(SimpleNamespace(repo=str(git_repo)))
        content = hook_file.read_text(encoding="utf-8")
        assert "echo existing" in content
        assert cli.MARKER_BEGIN not in content

    def test_uninstall_deletes_file_when_only_ours(self, git_repo, capsys):
        # 文件仅含 marker 块（无 shebang 等其它内容）时，移除后应删除整个文件
        hook_file = git_repo / ".git" / "hooks" / "post-commit"
        hook_file.write_text(
            f"{cli.MARKER_BEGIN}\ngit-log-tracker hook\n{cli.MARKER_END}\n",
            encoding="utf-8",
        )
        cli.cmd_uninstall(SimpleNamespace(repo=str(git_repo)))
        assert not hook_file.exists()
        assert "only our hook" in capsys.readouterr().out.lower()

    def test_uninstall_no_hook(self, git_repo, capsys):
        cli.cmd_uninstall(SimpleNamespace(repo=str(git_repo)))
        assert "No post-commit hook" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# 查询 / 修改命令（真实 SQLite）
# ---------------------------------------------------------------------------

class TestFind:
    def test_find_full_hash(self, temp_db, capsys):
        h = _insert(temp_db, commit_hash="b" * 40, short_hash="bbbbbbb")
        cli.cmd_find(SimpleNamespace(hash=h))
        out = capsys.readouterr().out
        assert "b" * 40 in out
        assert "alice@example.com" in out

    def test_find_prefix_unique(self, temp_db, capsys):
        _insert(temp_db, commit_hash="c" * 40, short_hash="ccccccc")
        cli.cmd_find(SimpleNamespace(hash="cccc"))
        assert "subject" in capsys.readouterr().out

    def test_find_prefix_multiple(self, temp_db, capsys):
        _insert(temp_db, commit_hash="abc" + "0" * 37, short_hash="abc0000",
                commit_subject="first")
        _insert(temp_db, commit_hash="abc" + "1" * 37, short_hash="abc1111",
                commit_subject="second")
        cli.cmd_find(SimpleNamespace(hash="abc"))
        assert "Multiple commits match" in capsys.readouterr().out

    def test_find_not_found(self, temp_db, capsys):
        cli.cmd_find(SimpleNamespace(hash="deadbeef"))
        assert "not found" in capsys.readouterr().out.lower()


class TestList:
    def _args(self, **over):
        base = dict(n=20, repo=None, author=None, since=None, until=None,
                    branch=None, label=None)
        base.update(over)
        return SimpleNamespace(**base)

    def test_list_empty(self, temp_db, capsys):
        cli.cmd_list(self._args())
        assert "No commits found" in capsys.readouterr().out

    def test_list_shows_rows(self, temp_db, capsys):
        _insert(temp_db, commit_hash="d" * 40, short_hash="ddddddd")
        cli.cmd_list(self._args())
        out = capsys.readouterr().out
        assert "HASH" in out
        assert "ddddddd" in out

    def test_list_filter_by_author(self, temp_db, capsys):
        _insert(temp_db, commit_hash="e" * 40, author_email="alice@example.com")
        _insert(temp_db, commit_hash="f" * 40, author_email="bob@example.com",
                repo_name="r2")
        cli.cmd_list(self._args(author="bob@example.com"))
        out = capsys.readouterr().out
        assert "r2" in out
        assert "r1" not in out

    def test_list_filter_by_branch(self, temp_db, capsys):
        _insert(temp_db, commit_hash="1" * 40, branch="dev", short_hash="1111111")
        cli.cmd_list(self._args(branch="dev"))
        assert "1111111" in capsys.readouterr().out

    def test_list_label_no_repos(self, temp_db, capsys):
        cli.cmd_list(self._args(label="ghost"))
        assert "No repos with label" in capsys.readouterr().out

    def test_list_label_matches(self, temp_db, tmp_path, capsys):
        import config
        repo_norm = str((tmp_path / "labeled").resolve()).replace("\\", "/")
        _insert(temp_db, commit_hash="2" * 40, short_hash="2222222",
                repo_path=repo_norm)
        config.add_label(str(tmp_path / "labeled"), "work")
        cli.cmd_list(self._args(label="work"))
        assert "2222222" in capsys.readouterr().out


class TestStats:
    def test_stats_basic(self, temp_db, capsys):
        _insert(temp_db, commit_hash="3" * 40)
        _insert(temp_db, commit_hash="4" * 40, author_name="Bob",
                author_email="bob@x.com", repo_name="r2")
        cli.cmd_stats(SimpleNamespace(label=None))
        out = capsys.readouterr().out
        assert "Total commits: 2" in out
        assert "By repo" in out
        assert "By author" in out

    def test_stats_label_no_repos(self, temp_db, capsys):
        cli.cmd_stats(SimpleNamespace(label="ghost"))
        assert "No repos with label" in capsys.readouterr().out


class TestDelete:
    def test_delete_full_hash(self, temp_db, capsys):
        h = _insert(temp_db, commit_hash="5" * 40)
        cli.cmd_delete(SimpleNamespace(hash=h))
        assert "Deleted 1" in capsys.readouterr().out

    def test_delete_prefix(self, temp_db, capsys):
        _insert(temp_db, commit_hash="6" * 40, short_hash="6666666")
        cli.cmd_delete(SimpleNamespace(hash="6666"))
        assert "Deleted 1" in capsys.readouterr().out

    def test_delete_not_found(self, temp_db, capsys):
        cli.cmd_delete(SimpleNamespace(hash="ffffffff"))
        assert "not found" in capsys.readouterr().out.lower()


class TestUpdate:
    def test_update_editable_field(self, temp_db, capsys):
        h = _insert(temp_db, commit_hash="7" * 40)
        cli.cmd_update(SimpleNamespace(hash=h, field="branch", value="release"))
        assert "Updated branch" in capsys.readouterr().out
        conn = db.get_connection(temp_db)
        try:
            row = conn.execute(
                "SELECT branch FROM commits WHERE commit_hash = ?", (h,)
            ).fetchone()
            assert row["branch"] == "release"
        finally:
            conn.close()

    def test_update_prefix_not_found(self, temp_db, capsys):
        cli.cmd_update(SimpleNamespace(hash="9999", field="branch", value="x"))
        assert "not found" in capsys.readouterr().out.lower()


# ---------------------------------------------------------------------------
# 数据目录 / 标签 / record / global / main
# ---------------------------------------------------------------------------

class TestSetupAndMigrate:
    def test_setup_creates_config_and_db(self, isolated_home, capsys):
        cli.cmd_setup(SimpleNamespace())
        assert isolated_home["config_path"].exists()
        assert isolated_home["db_path"].exists()
        assert "Setup complete" in capsys.readouterr().out

    def test_migrate_up_to_date(self, temp_db, capsys):
        cli.cmd_migrate(SimpleNamespace())
        assert "up to date" in capsys.readouterr().out.lower()

    def test_migrate_runs_when_behind(self, isolated_home, capsys):
        import sqlite3
        # 建一个 user_version=0 的空库，触发迁移分支
        sqlite3.connect(str(isolated_home["db_path"])).close()
        cli.cmd_migrate(SimpleNamespace())
        out = capsys.readouterr().out
        assert "Migrated" in out


class TestReinstall:
    def test_reinstall_keep_config(self, temp_db, isolated_home, capsys):
        cli.cmd_reinstall(SimpleNamespace(keep_config=True))
        out = capsys.readouterr().out
        assert "Deleted database" in out
        assert isolated_home["db_path"].exists()  # 重建

    def test_reinstall_full(self, isolated_home, capsys):
        cli.cmd_setup(SimpleNamespace())
        capsys.readouterr()
        cli.cmd_reinstall(SimpleNamespace(keep_config=False))
        out = capsys.readouterr().out
        assert "Deleted data directory" in out
        assert isolated_home["config_path"].exists()  # 重建


class TestLabelCommand:
    def _args(self, **over):
        base = dict(action="list", repo=None, labels=[])
        base.update(over)
        return SimpleNamespace(**base)

    def test_label_add_and_list(self, isolated_home, git_repo, capsys):
        cli.cmd_label(self._args(action="add", repo=str(git_repo), labels=["work"]))
        out = capsys.readouterr().out
        assert "work" in out
        cli.cmd_label(self._args(action="list", repo=str(git_repo)))
        assert "work" in capsys.readouterr().out

    def test_label_list_all_empty(self, isolated_home, capsys):
        cli.cmd_label(self._args(action="list"))
        assert "No labels defined" in capsys.readouterr().out

    def test_label_rm(self, isolated_home, git_repo, capsys):
        cli.cmd_label(self._args(action="add", repo=str(git_repo), labels=["work"]))
        capsys.readouterr()
        cli.cmd_label(self._args(action="rm", repo=str(git_repo), labels=["work"]))
        assert "Removed label" in capsys.readouterr().out

    def test_label_add_requires_label(self, isolated_home, git_repo, capsys):
        cli.cmd_label(self._args(action="add", repo=str(git_repo), labels=[]))
        assert "at least one label" in capsys.readouterr().err


class TestRecordCommand:
    def test_record_explicit_repo(self, isolated_home, git_repo, capsys):
        cli.cmd_record(SimpleNamespace(repo=str(git_repo)))
        assert "Recorded" in capsys.readouterr().out

    def test_record_excluded(self, isolated_home, git_repo, capsys):
        repo_norm = str(git_repo).replace("\\", "/")
        isolated_home["config_path"].write_text(
            f'[hooks]\nexclude = ["{repo_norm}"]\n', encoding="utf-8",
        )
        cli.cmd_record(SimpleNamespace(repo=str(git_repo)))
        assert "excluded" in capsys.readouterr().out.lower()


class TestGlobalCommand:
    def test_global_on_creates_template(self, isolated_home, capsys, mocker):
        mocker.patch("cli.subprocess.run")
        cli.cmd_global(SimpleNamespace(off=False))
        hook_file = isolated_home["template_dir"] / "hooks" / "post-commit"
        assert hook_file.exists()
        assert "template hook" in capsys.readouterr().out.lower()

    def test_global_off_removes_template(self, isolated_home, capsys, mocker):
        # 先创建模板
        mocker.patch("cli.subprocess.run")
        cli.cmd_global(SimpleNamespace(off=False))
        capsys.readouterr()
        # off 分支：get 返回非匹配值，跳过 unset，但仍删 hook 文件
        mocker.patch("cli.subprocess.run",
                     return_value=SimpleNamespace(stdout="other", returncode=0))
        cli.cmd_global(SimpleNamespace(off=True))
        hook_file = isolated_home["template_dir"] / "hooks" / "post-commit"
        assert not hook_file.exists()


class TestMainDispatch:
    def test_main_setup(self, isolated_home, monkeypatch, capsys):
        monkeypatch.setattr("sys.argv", ["git-log-tracker", "setup"])
        cli.main()
        assert "Setup complete" in capsys.readouterr().out

    def test_main_no_command_prints_help(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.argv", ["git-log-tracker"])
        cli.main()
        assert "usage" in capsys.readouterr().out.lower()
