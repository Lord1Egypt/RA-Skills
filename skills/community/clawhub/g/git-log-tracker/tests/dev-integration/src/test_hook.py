"""hook 模块 dev-integration 测试。

使用真实临时 git 仓库 + 真实 SQLite，验证 record_commit 从 git 读取
提交元数据并落库的完整链路。
"""

import db
import hook


class TestRecordCommitEndToEnd:
    def test_records_real_commit(self, isolated_home, git_repo):
        assert hook.record_commit(str(git_repo)) is True

        conn = db.get_connection(isolated_home["db_path"])
        try:
            rows = conn.execute("SELECT * FROM commits").fetchall()
            assert len(rows) == 1
            row = rows[0]
            assert row["repo_name"] == "repo"
            assert row["commit_subject"] == "feat: 初始提交"
            assert row["commit_body"] == "正文说明"
            assert row["branch"] in ("master", "main")
            assert len(row["commit_hash"]) == 40
        finally:
            conn.close()

    def test_insert_or_ignore_dedups(self, isolated_home, git_repo):
        # 同一提交记录两次，唯一约束应去重为 1 行
        assert hook.record_commit(str(git_repo)) is True
        assert hook.record_commit(str(git_repo)) is True

        conn = db.get_connection(isolated_home["db_path"])
        try:
            count = conn.execute("SELECT COUNT(*) FROM commits").fetchone()[0]
            assert count == 1
        finally:
            conn.close()

    def test_excluded_repo_not_recorded(self, isolated_home, git_repo):
        repo_norm = str(git_repo).replace("\\", "/")
        isolated_home["config_path"].write_text(
            f'[hooks]\nexclude = ["{repo_norm}"]\n[database]\npath = "index.db"\n',
            encoding="utf-8",
        )
        assert hook.record_commit(str(git_repo)) is False

    def test_get_repo_path_in_real_repo(self, git_repo, monkeypatch):
        # get_repo_path 不接受 cwd 参数，临时切到仓库目录验证真实 git 解析
        monkeypatch.chdir(git_repo)
        resolved = hook.get_repo_path().replace("\\", "/")
        assert resolved.endswith("/repo")
