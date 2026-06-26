"""models 模块单元测试：校验 SQLAlchemy Commit 模型的表名与列定义。"""

import models


class TestCommitModel:
    def test_tablename(self):
        assert models.Commit.__tablename__ == "commits"

    def test_has_expected_columns(self):
        cols = set(models.Commit.__table__.columns.keys())
        expected = {
            "id", "commit_hash", "short_hash", "author_name", "author_email",
            "author_ts", "committer_name", "committer_email", "commit_subject",
            "commit_body", "branch", "repo_path", "repo_name", "parent_hashes",
            "recorded_at",
        }
        assert expected <= cols

    def test_commit_hash_unique_and_not_null(self):
        col = models.Commit.__table__.columns["commit_hash"]
        assert col.unique is True
        assert col.nullable is False

    def test_id_is_primary_key(self):
        assert models.Commit.__table__.columns["id"].primary_key is True
