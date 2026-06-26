"""Tests for mg_repo.meta_json_repository — meta.json persistence wrapper."""

import json
import os
import pytest

from mg_repo.meta_json_repository import MetaJsonRepository, _hash_meta


@pytest.fixture
def repo(tmp_path):
    meta_path = os.path.join(str(tmp_path), "memory", "meta.json")
    os.makedirs(os.path.dirname(meta_path), exist_ok=True)
    with open(meta_path, "w") as f:
        json.dump({"version": "0.4.2", "memories": [], "conflicts": [],
                   "security_rules": [], "entities": {}}, f)
    return MetaJsonRepository(meta_path, workspace=str(tmp_path))


@pytest.fixture
def minimal_meta():
    return {
        "version": "0.4.2",
        "memories": [],
        "conflicts": [],
        "security_rules": [],
        "entities": {},
    }


class TestHashMeta:
    def test_same_content_same_hash(self):
        meta = {"a": 1, "b": 2}
        assert _hash_meta(meta) == _hash_meta(meta)

    def test_different_content_different_hash(self):
        assert _hash_meta({"a": 1}) != _hash_meta({"a": 2})

    def test_key_order_irrelevant(self):
        assert _hash_meta({"a": 1, "b": 2}) == _hash_meta({"b": 2, "a": 1})


class TestMetaJsonRepository:
    def test_load_meta_returns_default(self, repo):
        meta = repo.load_meta()
        assert "version" in meta
        assert "memories" in meta

    def test_save_returns_normalized(self, repo, minimal_meta):
        minimal_meta["version"] = "0.4.5"
        result = repo.save_meta(minimal_meta)
        # save_meta normalizes and returns the normalized version
        assert "version" in result
        assert "memories" in result

    def test_save_creates_directory(self, tmp_path):
        deep_path = os.path.join(str(tmp_path), "a", "b", "c", "meta.json")
        r = MetaJsonRepository(deep_path, workspace=str(tmp_path))
        r.save_meta({"version": "0.4.2", "memories": []})
        assert os.path.exists(deep_path)

    def test_dry_run_does_not_write(self, tmp_path):
        meta_path = os.path.join(str(tmp_path), "meta.json")
        r = MetaJsonRepository(meta_path, workspace=str(tmp_path), dry_run=True)
        r.save_meta({"version": "0.4.5", "memories": []})
        assert not os.path.exists(meta_path)

    def test_mutate_meta_changes(self, repo, minimal_meta):
        repo.save_meta(minimal_meta)

        def add_memory(meta):
            meta["memories"].append({"id": "mem_test", "content": "hello"})
            return "ok"

        result = repo.mutate_meta(add_memory)
        assert result["changed"] is True
        assert result["meta"]["memories"][0]["id"] == "mem_test"
        assert result["result"] == "ok"

    def test_mutate_meta_no_change(self, repo, minimal_meta):
        repo.save_meta(minimal_meta)

        def noop(meta):
            return "noop"

        result = repo.mutate_meta(noop)
        assert result["changed"] is False

    def test_mutate_meta_dry_run(self, repo, minimal_meta, tmp_path):
        # Create a separate dry_run repo
        meta_path = os.path.join(str(tmp_path), "memory", "meta.json")
        os.makedirs(os.path.dirname(meta_path), exist_ok=True)
        with open(meta_path, "w") as f:
            json.dump({"version": "0.4.2", "memories": []}, f)
        dry_repo = MetaJsonRepository(meta_path, workspace=str(tmp_path), dry_run=True)

        def add_memory(meta):
            meta["memories"].append({"id": "mem_test"})
            return "ok"

        result = dry_repo.mutate_meta(add_memory)
        assert result["changed"] is True
        assert result.get("dry_run") is True
        # File should not have been updated
        with open(meta_path) as f:
            saved = json.load(f)
        assert len(saved.get("memories", [])) == 0

    def test_append_event(self, repo, minimal_meta):
        repo.save_meta(minimal_meta)
        event = {"type": "test_event", "data": 42}
        result = repo.append_event(event)
        assert isinstance(result, dict)
        loaded = repo.load_meta()
        assert len(loaded["event_log"]) == 1
        assert loaded["event_log"][0]["type"] == "test_event"

    def test_record_hit(self, repo, minimal_meta):
        repo.save_meta(minimal_meta)
        stats = repo.record_hit("test_module", input_count=5, output_count=3)
        assert stats is not None
        assert stats["runs"] == 1

    def test_derive_workspace(self, tmp_path):
        meta_path = os.path.join(str(tmp_path), "memory", "meta.json")
        r = MetaJsonRepository(meta_path)
        assert r.workspace == str(tmp_path)

    def test_derive_workspace_non_standard(self, tmp_path):
        meta_path = os.path.join(str(tmp_path), "data", "meta.json")
        r = MetaJsonRepository(meta_path)
        assert r.workspace == os.path.join(str(tmp_path), "data")
