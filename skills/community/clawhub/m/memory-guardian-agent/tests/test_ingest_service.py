"""Tests for mg_app.ingest_service — application-layer ingest orchestration."""

import json
import os
import pytest

from mg_app.ingest_service import IngestService, _fill_fields, _detect_provenance, _evaluate_pool
from mg_repo.meta_json_repository import MetaJsonRepository


@pytest.fixture
def workspace(tmp_path):
    ws = str(tmp_path)
    meta_path = os.path.join(ws, "memory", "meta.json")
    os.makedirs(os.path.dirname(meta_path), exist_ok=True)
    # Initialize meta.json
    with open(meta_path, "w") as f:
        json.dump({
            "version": "0.4.2",
            "memories": [],
            "conflicts": [],
            "security_rules": [],
            "entities": {},
        }, f)
    return ws


@pytest.fixture
def repo(workspace):
    meta_path = os.path.join(workspace, "memory", "meta.json")
    return MetaJsonRepository(meta_path, workspace=workspace)


@pytest.fixture
def service(repo):
    return IngestService(repo)


class TestFillFields:
    def test_content_only(self):
        fields = _fill_fields(content="hello")
        assert fields["content"] == "hello"
        assert fields["is_case"] is False

    def test_case_fields(self):
        fields = _fill_fields(situation="sit", judgment="judg")
        assert fields["is_case"] is True
        assert "情境：sit" in fields["content"]


class TestDetectProvenance:
    def test_default(self):
        level, source = _detect_provenance("普通内容")
        assert level == "L2"

    def test_explicit(self):
        level, source = _detect_provenance("test", source="human")
        assert level == "L1"


class TestEvaluatePool:
    def test_empty_pool(self):
        result = _evaluate_pool("test content", [])
        assert result["duplicate"] is None
        assert result["active_count"] == 0

    def test_with_duplicate(self):
        mems = [{"id": "mem_1", "content": "exact match content here", "status": "active"}]
        result = _evaluate_pool("exact match content here", mems)
        assert result["duplicate"] is not None

    def test_active_count(self):
        mems = [
            {"id": "mem_1", "content": "a b c", "status": "active"},
            {"id": "mem_2", "content": "d e f", "status": "archived"},
            {"id": "mem_3", "content": "g h i", "status": "observing"},
        ]
        result = _evaluate_pool("test", mems)
        assert result["active_count"] == 2


class TestIngestService:
    def test_create_basic_memory(self, service, workspace):
        result = service.ingest(
            content="test memory content",
            importance=0.5,
            tags=["test"],
            workspace=workspace,
        )
        assert result["action"] == "created"
        assert result["id"].startswith("mem_")

    def test_create_case(self, service, workspace):
        result = service.ingest(
            content=None,
            importance=0.7,
            tags=["case_tag"],
            workspace=workspace,
            situation="当发生X时",
            judgment="应该做Y",
        )
        assert result["action"] == "created"
        mem = result["memory"]
        assert mem["situation"] == "当发生X时"
        assert mem["judgment"] == "应该做Y"

    def test_dedup_prevents_duplicate(self, service, workspace):
        service.ingest(content="unique content xyz", importance=0.5, tags=[], workspace=workspace)
        result = service.ingest(content="unique content xyz", importance=0.5, tags=[], workspace=workspace)
        assert result["action"] == "dedup_found"

    def test_update_existing(self, service, workspace):
        create = service.ingest(content="original", importance=0.5, tags=[], workspace=workspace)
        mem_id = create["id"]
        result = service.ingest(
            content="updated",
            importance=0.8,
            tags=["new_tag"],
            workspace=workspace,
            update_id=mem_id,
        )
        assert result["action"] == "updated"

    def test_update_not_found(self, service, workspace):
        result = service.ingest(
            content="test",
            importance=0.5,
            tags=[],
            workspace=workspace,
            update_id="nonexistent_id",
        )
        assert result["action"] == "not_found"

    def test_no_content_error(self, service, workspace):
        result = service.ingest(
            content=None,
            importance=0.5,
            tags=[],
            workspace=workspace,
        )
        assert result["action"] == "error"

    def test_classification_applied(self, service, workspace):
        result = service.ingest(
            content="memory-guardian v0.4.5 项目开发",
            importance=0.6,
            tags=["项目"],
            workspace=workspace,
        )
        assert result["action"] == "created"
        classification = result.get("classification")
        assert classification is not None
        assert classification["primary_tag"] == "project"

    def test_provenance_assigned(self, service, workspace):
        result = service.ingest(
            content="记住这个偏好设置",
            importance=0.5,
            tags=[],
            workspace=workspace,
        )
        mem = result["memory"]
        assert mem["provenance_level"] == "L1"

    def test_memory_file_written(self, service, workspace):
        result = service.ingest(
            content="test file write",
            importance=0.5,
            tags=["test"],
            workspace=workspace,
        )
        assert result["written_file"] is not None
        assert os.path.exists(result["written_file"])

    def test_blocked_by_security(self, service, workspace):
        # Add a security rule
        meta = service.repo.load_meta()
        meta["security_rules"] = [{
            "id": "test-block",
            "pattern": r"BLOCKED_CONTENT",
            "description": "test block",
            "severity": "critical",
        }]
        service.repo.save_meta(meta)
        result = service.ingest(
            content="This has BLOCKED_CONTENT in it",
            importance=0.5,
            tags=[],
            workspace=workspace,
        )
        assert result["action"] == "blocked"
