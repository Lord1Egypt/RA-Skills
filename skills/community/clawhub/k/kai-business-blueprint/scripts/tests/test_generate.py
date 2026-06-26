import json
import subprocess
import sys
from pathlib import Path

from business_blueprint.validate import validate_blueprint


ROOT = Path(__file__).resolve().parents[1]


def test_plan_creates_skeleton_with_source(tmp_path: Path) -> None:
    """--plan creates a valid empty blueprint with source text stored."""
    source = tmp_path / "brief.txt"
    source.write_text(
        "零售客户需要会员运营和门店运营，导购负责会员注册，CRM和POS支撑订单管理。",
        encoding="utf-8",
    )
    output = tmp_path / "solution.blueprint.json"

    result = subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli",
         "--plan", str(output), "--from", str(source), "--industry", "retail"],
        cwd=ROOT, capture_output=True, text=True,
    )

    assert result.returncode == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["meta"]["industry"] == "retail"
    assert "零售客户" in payload["context"]["sourceRefs"][0]["excerpt"]
    # Skeleton only — AI agent fills entities
    assert isinstance(payload["library"]["capabilities"], list)
    assert isinstance(payload["library"]["actors"], list)
    assert isinstance(payload["library"]["flowSteps"], list)
    assert isinstance(payload["library"]["systems"], list)
    assert "industryHints" not in payload


def test_plan_requires_source_text(tmp_path: Path) -> None:
    """--plan without --from should fail."""
    output = tmp_path / "solution.blueprint.json"
    result = subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli",
         "--plan", str(output), "--industry", "retail"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 1
    assert "requires source text" in result.stderr


def test_validate_blueprint_with_entities(tmp_path: Path) -> None:
    """Validate works correctly on a blueprint with entities written by AI agent."""
    output = tmp_path / "test.blueprint.json"
    blueprint = {
        "version": "1.0",
        "meta": {"title": "Test", "industry": "retail"},
        "context": {"goals": [], "scope": [], "assumptions": [], "constraints": [],
                    "sourceRefs": [], "clarifyRequests": [], "clarifications": []},
        "library": {
            "capabilities": [
                {"id": "cap-member", "name": "会员运营", "level": 1,
                 "description": "会员管理", "ownerActorIds": [], "supportingSystemIds": ["sys-crm"]},
                {"id": "cap-store", "name": "门店运营", "level": 1,
                 "description": "门店管理", "ownerActorIds": [], "supportingSystemIds": ["sys-pos"]},
            ],
            "actors": [{"id": "actor-guide", "name": "导购"}],
            "flowSteps": [
                {"id": "flow-register", "name": "会员注册", "actorId": "actor-guide",
                 "capabilityIds": ["cap-member"], "systemIds": [], "stepType": "task",
                 "inputRefs": [], "outputRefs": []},
            ],
            "systems": [
                {"id": "sys-crm", "kind": "system", "name": "CRM", "aliases": [],
                 "description": "客户关系管理",
                 "resolution": {"status": "canonical", "canonicalName": "CRM"},
                 "capabilityIds": ["cap-member"]},
                {"id": "sys-pos", "kind": "system", "name": "POS", "aliases": [],
                 "description": "收银系统",
                 "resolution": {"status": "canonical", "canonicalName": "POS"},
                 "capabilityIds": ["cap-store"]},
            ],
        },
        "relations": [],
        "views": [],
        "editor": {"fieldLocks": {}, "theme": "enterprise-default"},
        "artifacts": {},
    }
    output.write_text(json.dumps(blueprint, ensure_ascii=False), encoding="utf-8")

    result = validate_blueprint(blueprint)
    assert "summary" in result
    assert result["summary"]["errorCount"] == 0
