"""cli 模块单元测试：纯函数 helper 与无副作用分支。

涉及 db / 真实 git 的端到端命令在 dev-integration 阶段覆盖。
"""

from types import SimpleNamespace

import pytest

import cli


class TestPathVariants:
    def test_expands_both_slash_styles(self):
        variants = cli._path_variants(["a/b/c"])
        assert "a/b/c" in variants
        assert "a\\b\\c" in variants

    def test_dedups(self):
        # 无斜杠路径正反斜杠转换后相同，应去重为一项
        assert cli._path_variants(["plain"]) == ["plain"]


class TestLabelWhere:
    def test_no_label_returns_empty_clause(self):
        assert cli._label_where(None) == ("", [])

    def test_label_without_repos_returns_none(self, mocker):
        mocker.patch("cli.paths_for_label", return_value=[])
        assert cli._label_where("ghost") == (None, None)

    def test_label_with_repos_builds_in_clause(self, mocker):
        mocker.patch("cli.paths_for_label", return_value=["/r1"])
        frag, params = cli._label_where("work")
        assert frag.startswith(" AND repo_path IN (")
        assert "/r1" in params
        assert frag.count("?") == len(params)


class TestResolveRepo:
    def test_non_git_dir_exits(self, tmp_path):
        with pytest.raises(SystemExit):
            cli.resolve_repo(str(tmp_path))

    def test_git_dir_resolves(self, tmp_path):
        (tmp_path / ".git").mkdir()
        result = cli.resolve_repo(str(tmp_path))
        assert result == tmp_path.resolve()


class TestHookContent:
    def test_hook_content_has_markers(self):
        content = cli.get_hook_content()
        assert cli.MARKER_BEGIN in content
        assert cli.MARKER_END in content
        assert "git-log-tracker hook" in content

    def test_global_hook_content_has_markers(self):
        content = cli.get_global_hook_content()
        assert cli.MARKER_BEGIN in content
        assert cli.MARKER_END in content


class TestEditableFields:
    def test_expected_fields(self):
        assert cli.EDITABLE_FIELDS == {
            "branch", "commit_subject", "commit_body", "repo_path", "repo_name"
        }


class TestCmdUpdateInvalidField:
    def test_rejects_non_editable_field(self, capsys):
        args = SimpleNamespace(field="id", hash="abc", value="x")
        cli.cmd_update(args)
        out = capsys.readouterr().out
        assert "not editable" in out
