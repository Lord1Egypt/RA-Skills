"""hook 模块单元测试。

git 调用通过 mock subprocess 隔离（§4：unit 禁止进程外 I/O）。
本文件聚焦 get_commit_info 的解析逻辑与 record_commit 的分支控制。
"""

from types import SimpleNamespace

import hook


def _fake_run(stdout):
    return SimpleNamespace(stdout=stdout, returncode=0)


def _git_lines(subject="subj", parent="", ref="HEAD -> main", body="",
               cn="A", ce="a@x"):
    """按 get_commit_info 期望的字段顺序构造 git 输出：
    H h an ae aI cn ce s P D b（body 放最后）。
    """
    return "\n".join([
        "h" * 40, "hhhhhhh", "A", "a@x", "2026-01-01T00:00:00+08:00",
        cn, ce, subject, parent, ref, body,
    ])


class TestGetRepoPath:
    def test_strips_trailing_newline(self, mocker):
        mocker.patch("hook.subprocess.run", return_value=_fake_run("/path/to/repo\n"))
        assert hook.get_repo_path() == "/path/to/repo"


class TestGetCommitInfo:
    def test_parses_all_fields(self, mocker, git_log_output):
        mocker.patch("hook.subprocess.run", return_value=_fake_run(git_log_output))
        info = hook.get_commit_info("/repo")
        assert info["commit_hash"] == "a" * 40
        assert info["short_hash"] == "aaaaaaa"
        assert info["author_name"] == "Alice"
        assert info["author_email"] == "alice@example.com"
        assert info["commit_subject"] == "feat: 初始提交"
        assert info["commit_body"] == "正文内容"
        assert info["branch"] == "master"

    def test_detached_head_branch_none(self, mocker):
        mocker.patch("hook.subprocess.run",
                     return_value=_fake_run(_git_lines(ref="tag: v1.0")))
        info = hook.get_commit_info("/repo")
        assert info["branch"] is None

    def test_empty_body_and_parents_become_none(self, mocker):
        mocker.patch("hook.subprocess.run",
                     return_value=_fake_run(_git_lines(ref="HEAD -> main")))
        info = hook.get_commit_info("/repo")
        assert info["commit_body"] is None
        assert info["parent_hashes"] is None
        assert info["branch"] == "main"

    def test_parent_hashes_preserved(self, mocker):
        mocker.patch("hook.subprocess.run", return_value=_fake_run(
            _git_lines(subject="merge", parent="p1 p2", ref="HEAD -> main",
                       body="body")))
        info = hook.get_commit_info("/repo")
        assert info["parent_hashes"] == "p1 p2"

    def test_multiline_body_preserves_branch(self, mocker):
        """回归测试：带多行 body 的提交不应导致 branch/parent 错位。"""
        mocker.patch("hook.subprocess.run", return_value=_fake_run(
            _git_lines(subject="feat: x", parent="abc123", ref="HEAD -> dev",
                       body="第一行\n第二行\n第三行")))
        info = hook.get_commit_info("/repo")
        assert info["branch"] == "dev"
        assert info["parent_hashes"] == "abc123"
        assert info["commit_body"] == "第一行\n第二行\n第三行"

    def test_truncated_output_padded(self, mocker):
        # 只有 3 行，应被补齐为空字段而非抛 IndexError
        mocker.patch("hook.subprocess.run", return_value=_fake_run("h\nhh\nAlice"))
        info = hook.get_commit_info("/repo")
        assert info["commit_hash"] == "h"
        assert info["commit_subject"] == ""
        assert info["branch"] is None

    def test_empty_committer_becomes_none(self, mocker):
        mocker.patch("hook.subprocess.run", return_value=_fake_run(
            _git_lines(ref="HEAD -> main", cn="", ce="")))
        info = hook.get_commit_info("/repo")
        assert info["committer_name"] is None
        assert info["committer_email"] is None


class TestRecordCommit:
    def test_excluded_repo_returns_false(self, mocker):
        mocker.patch("hook.read_config", return_value={"hooks": {"exclude": ["*"]}})
        get_conn = mocker.patch("hook.get_connection")
        assert hook.record_commit("/any/repo") is False
        get_conn.assert_not_called()

    def test_success_inserts_and_returns_true(self, mocker, sample_commit):
        mocker.patch("hook.read_config", return_value={})
        mocker.patch("hook.get_commit_info", return_value=sample_commit)
        conn = mocker.MagicMock()
        mocker.patch("hook.get_connection", return_value=conn)
        assert hook.record_commit("/some/repo") is True
        conn.execute.assert_called_once()
        conn.commit.assert_called_once()
        conn.close.assert_called_once()

    def test_exception_returns_false(self, mocker):
        mocker.patch("hook.read_config", return_value={})
        mocker.patch("hook.get_commit_info", side_effect=RuntimeError("boom"))
        assert hook.record_commit("/some/repo") is False
