import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_plan_creates_skeleton(tmp_path: Path) -> None:
    """--plan creates a valid empty blueprint JSON with source text stored."""
    blueprint = tmp_path / "solution.blueprint.json"
    subprocess.run(
        [
            sys.executable, "-m", "business_blueprint.cli",
            "--plan", str(blueprint),
            "--from", "云之家 AI 转型业务蓝图：门店运营、会员运营、供应链协同",
            "--industry", "retail",
        ],
        cwd=ROOT,
        check=True,
    )
    assert blueprint.exists()
    data = json.loads(blueprint.read_text())
    assert data["meta"]["industry"] == "retail"
    assert len(data["context"]["sourceRefs"]) == 1
    assert "云之家" in data["context"]["sourceRefs"][0]["excerpt"]
    # No hardcoded entities — AI agent fills these
    assert isinstance(data["library"]["capabilities"], list)


def test_plan_requires_source_text(tmp_path: Path) -> None:
    """--plan without --from should error."""
    blueprint = tmp_path / "solution.blueprint.json"
    result = subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli",
         "--plan", str(blueprint), "--industry", "retail"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "requires source text" in result.stderr


def test_export_and_validate(tmp_path: Path) -> None:
    """AI agent writes blueprint JSON, then --export generates SVG + HTML."""
    blueprint_path = tmp_path / "solution.blueprint.json"
    blueprint = {
        "version": "1.0",
        "meta": {"title": "Test", "industry": "retail"},
        "context": {"goals": [], "scope": [], "assumptions": [], "constraints": [],
                    "sourceRefs": [], "clarifyRequests": [], "clarifications": []},
        "library": {
            "capabilities": [
                {"id": "cap-store", "name": "门店运营", "level": 1,
                 "description": "门店日常经营", "ownerActorIds": ["actor-mgr"],
                 "supportingSystemIds": ["sys-pos"]},
                {"id": "cap-member", "name": "会员运营", "level": 1,
                 "description": "会员管理", "ownerActorIds": [],
                 "supportingSystemIds": ["sys-crm"]},
            ],
            "actors": [{"id": "actor-mgr", "name": "店长"}],
            "flowSteps": [
                {"id": "flow-register", "name": "会员注册", "actorId": "actor-mgr",
                 "capabilityIds": ["cap-member"], "systemIds": [], "stepType": "task",
                 "inputRefs": [], "outputRefs": []},
            ],
            "systems": [
                {"id": "sys-pos", "kind": "system", "name": "POS",
                 "aliases": [], "description": "收银系统",
                 "resolution": {"status": "canonical", "canonicalName": "POS"},
                 "capabilityIds": ["cap-store"]},
                {"id": "sys-crm", "kind": "system", "name": "CRM",
                 "aliases": [], "description": "客户关系管理",
                 "resolution": {"status": "canonical", "canonicalName": "CRM"},
                 "capabilityIds": ["cap-member"]},
            ],
        },
        "relations": [
            {"id": "rel-1", "type": "supports", "from": "sys-pos", "to": "cap-store", "label": "支撑"},
            {"id": "rel-2", "type": "supports", "from": "sys-crm", "to": "cap-member", "label": "支撑"},
        ],
        "views": [],
        "editor": {"fieldLocks": {}, "theme": "enterprise-default"},
        "artifacts": {},
    }
    blueprint_path.write_text(json.dumps(blueprint, ensure_ascii=False), encoding="utf-8")

    subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli", "--export", str(blueprint_path)],
        cwd=ROOT, check=True,
    )

    assert (tmp_path / "solution.exports" / "solution.svg").exists()
    assert (tmp_path / "solution.blueprint.html").exists()
    # No drawio/excalidraw/mermaid by default
    assert not (tmp_path / "solution.exports" / "solution.drawio").exists()

    validation = subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli", "--validate", str(blueprint_path)],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    payload = json.loads(validation.stdout)
    assert "summary" in payload


def test_project_generates_projection_json(tmp_path: Path) -> None:
    blueprint_path = tmp_path / "solution.blueprint.json"
    blueprint = {
        "version": "1.0",
        "meta": {
            "title": "Retail Blueprint",
            "industry": "retail",
            "revisionId": "rev-1",
            "lastModifiedAt": "2026-04-20T12:00:00Z",
        },
        "context": {
            "goals": ["Reduce checkout queue time"],
            "scope": ["Store operations"],
            "assumptions": [],
            "constraints": [],
            "sourceRefs": [],
            "clarifyRequests": [],
            "clarifications": [],
        },
        "library": {
            "capabilities": [],
            "actors": [],
            "flowSteps": [],
            "systems": [],
        },
        "relations": [],
        "views": [],
        "editor": {"fieldLocks": {}, "theme": "enterprise-default"},
        "artifacts": {},
    }
    blueprint_path.write_text(json.dumps(blueprint, ensure_ascii=False), encoding="utf-8")

    subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli", "--project", str(blueprint_path)],
        cwd=ROOT,
        check=True,
    )

    projection_path = tmp_path / "solution.projection.json"
    assert projection_path.exists()
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    assert projection["meta"]["adapterVersion"] == "v1"
    assert projection["summary"]["goals"] == ["Reduce checkout queue time"]
