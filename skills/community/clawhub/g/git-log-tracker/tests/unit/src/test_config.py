"""config 模块单元测试。

覆盖配置读取、排除匹配、以及 labels.json 的增删查持久化逻辑。
所有涉及磁盘的用例均通过 isolated_config 重定向到临时目录。
"""

import config


class TestReadConfig:
    def test_missing_file_returns_defaults(self, tmp_path):
        cfg = config.read_config(tmp_path / "nope.toml")
        assert cfg == {"hooks": {"exclude": []}, "database": {"path": "index.db"}}

    def test_reads_existing_toml(self, tmp_path):
        p = tmp_path / "config.toml"
        p.write_text(
            '[hooks]\nexclude = ["/tmp/*"]\n[database]\npath = "x.db"\n',
            encoding="utf-8",
        )
        cfg = config.read_config(p)
        assert cfg["hooks"]["exclude"] == ["/tmp/*"]
        assert cfg["database"]["path"] == "x.db"


class TestIsExcludedRepo:
    def test_matches_wildcard(self):
        cfg = {"hooks": {"exclude": ["/tmp/*"]}}
        assert config.is_excluded_repo("/tmp/foo", cfg) is True

    def test_no_match(self):
        cfg = {"hooks": {"exclude": ["/tmp/*"]}}
        assert config.is_excluded_repo("/home/alice/proj", cfg) is False

    def test_backslashes_normalized(self):
        cfg = {"hooks": {"exclude": ["*/secret/*"]}}
        assert config.is_excluded_repo(r"C:\work\secret\repo", cfg) is True

    def test_empty_excludes(self):
        assert config.is_excluded_repo("/anything", {}) is False


class TestDefaultConfigContent:
    def test_contains_sections(self):
        content = config.get_default_config_content()
        assert "[hooks]" in content
        assert "[database]" in content
        assert "exclude" in content


class TestEnsureConfigExists:
    def test_creates_dir_and_file(self, isolated_config):
        path = config.ensure_config_exists()
        assert path.exists()
        assert path == isolated_config / "config.toml"
        assert "[hooks]" in path.read_text(encoding="utf-8")

    def test_idempotent_keeps_existing(self, isolated_config):
        first = config.ensure_config_exists()
        first.write_text("custom = true\n", encoding="utf-8")
        config.ensure_config_exists()
        assert first.read_text(encoding="utf-8") == "custom = true\n"


class TestNormalizePath:
    def test_returns_absolute_forward_slashes(self, tmp_path):
        result = config._normalize_path(str(tmp_path / "a" / "b"))
        assert "\\" not in result
        assert result.endswith("/a/b")


class TestReadLabels:
    def test_missing_returns_empty(self, isolated_config):
        assert config.read_labels() == {}

    def test_non_dict_returns_empty(self, isolated_config):
        isolated_config.mkdir(parents=True, exist_ok=True)
        (isolated_config / "labels.json").write_text("[1, 2]", encoding="utf-8")
        assert config.read_labels() == {}

    def test_broken_json_returns_empty(self, isolated_config):
        isolated_config.mkdir(parents=True, exist_ok=True)
        (isolated_config / "labels.json").write_text("{not json", encoding="utf-8")
        assert config.read_labels() == {}


class TestLabelMutations:
    def test_add_label_creates_entry(self, isolated_config, tmp_path):
        repo = str(tmp_path / "myrepo")
        config.add_label(repo, "work")
        assert config.labels_for_path(repo) == ["work"]

    def test_add_label_dedup(self, isolated_config, tmp_path):
        repo = str(tmp_path / "myrepo")
        config.add_label(repo, "work")
        config.add_label(repo, "work")
        assert config.labels_for_path(repo) == ["work"]

    def test_add_multiple_labels_ordered(self, isolated_config, tmp_path):
        repo = str(tmp_path / "myrepo")
        config.add_label(repo, "work")
        config.add_label(repo, "oss")
        assert config.labels_for_path(repo) == ["work", "oss"]

    def test_remove_label_present(self, isolated_config, tmp_path):
        repo = str(tmp_path / "myrepo")
        config.add_label(repo, "work")
        assert config.remove_label(repo, "work") is True
        assert config.labels_for_path(repo) == []

    def test_remove_label_absent(self, isolated_config, tmp_path):
        repo = str(tmp_path / "myrepo")
        assert config.remove_label(repo, "ghost") is False

    def test_remove_last_label_drops_key(self, isolated_config, tmp_path):
        repo = str(tmp_path / "myrepo")
        config.add_label(repo, "work")
        config.remove_label(repo, "work")
        assert config.read_labels() == {}

    def test_paths_for_label(self, isolated_config, tmp_path):
        r1 = str(tmp_path / "r1")
        r2 = str(tmp_path / "r2")
        config.add_label(r1, "work")
        config.add_label(r2, "work")
        config.add_label(r2, "oss")
        paths = config.paths_for_label("work")
        assert len(paths) == 2
        assert set(config.paths_for_label("oss")) == {config._normalize_path(r2)}

    def test_labels_for_path_unknown(self, isolated_config, tmp_path):
        assert config.labels_for_path(str(tmp_path / "unknown")) == []
