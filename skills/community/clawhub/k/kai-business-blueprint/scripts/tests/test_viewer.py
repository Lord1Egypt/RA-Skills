import json
from pathlib import Path

from business_blueprint.model import write_json
from business_blueprint.viewer import write_viewer_package


def test_write_viewer_package_creates_viewer_and_handoff(tmp_path: Path) -> None:
    blueprint = {
        "version": "1.0",
        "meta": {
            "revisionId": "rev-2",
            "parentRevisionId": "rev-1",
            "lastModifiedBy": "human",
        },
        "context": {},
        "library": {
            "capabilities": [
                {
                    "id": "cap-membership",
                    "name": "会员运营",
                    "description": "原始描述 </script><script>alert('xss')</script>",
                }
            ],
            "actors": [],
            "flowSteps": [],
            "systems": [{"id": "sys-crm", "name": "CRM", "description": "原始系统描述"}],
        },
        "relations": [],
        "views": [],
        "editor": {"fieldLocks": {"meta.title": "human"}},
        "artifacts": {},
    }
    blueprint_path = tmp_path / "input" / "solution.blueprint.json"
    write_json(blueprint_path, blueprint)

    viewer_path = tmp_path / "nested" / "output" / "solution.viewer.html"
    handoff_path = tmp_path / "nested" / "output" / "solution.handoff.json"
    patch_path = tmp_path / "nested" / "logs" / "solution.patch.jsonl"

    write_viewer_package(blueprint_path, viewer_path, handoff_path, patch_path)

    assert viewer_path.exists()
    assert handoff_path.exists()
    assert patch_path.exists()
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    assert handoff["revisionId"] == "rev-2"
    assert handoff["parentRevisionId"] == "rev-1"
    assert handoff["lastModifiedBy"] == "human"
    assert handoff["blueprintPath"].endswith("solution.blueprint.json")
    assert Path(handoff["viewerPath"]).name == "solution.viewer.html"
    assert Path(handoff["viewerPath"]).parent.name == "output"
    assert Path(handoff["viewerPath"]).parent.parent.name == "nested"
    assert Path(handoff["patchPath"]).name == "solution.patch.jsonl"
    assert Path(handoff["patchPath"]).parent.name == "logs"
    assert Path(handoff["patchPath"]).parent.parent.name == "nested"

    patch_seed = patch_path.read_text(encoding="utf-8").strip().splitlines()
    assert patch_seed
    seed_entry = json.loads(patch_seed[0])
    assert seed_entry["op"] == "seed_patch_log"
    assert seed_entry["revisionId"] == "rev-2"
    assert seed_entry["fieldLocks"] == {"meta.title": "human"}

    viewer_html = viewer_path.read_text(encoding="utf-8")
    assert "card-desc" in viewer_html
    assert "原始描述 </script><script>alert('xss')</script>" not in viewer_html
    assert "alert('xss')" in viewer_html
    assert "<\\/script>" in viewer_html
    assert "solution.patch.jsonl" in viewer_html
    assert "seed_patch_log" in viewer_html
    assert "realPatchEntries" in viewer_html
    assert "savedPatchSnapshot" in viewer_html


def test_write_viewer_package_preserves_existing_patch_log(tmp_path: Path) -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "rev-3", "lastModifiedBy": "ai"},
        "context": {},
        "library": {
            "capabilities": [],
            "actors": [],
            "flowSteps": [],
            "systems": [],
        },
        "relations": [],
        "views": [],
        "editor": {"fieldLocks": {}},
        "artifacts": {},
    }
    blueprint_path = tmp_path / "input" / "solution.blueprint.json"
    write_json(blueprint_path, blueprint)

    viewer_path = tmp_path / "nested" / "output" / "solution.viewer.html"
    handoff_path = tmp_path / "nested" / "output" / "solution.handoff.json"
    patch_path = tmp_path / "nested" / "logs" / "solution.patch.jsonl"
    patch_path.parent.mkdir(parents=True, exist_ok=True)
    original_patch = '{"op":"existing_entry","value":1}\n'
    patch_path.write_text(original_patch, encoding="utf-8")

    write_viewer_package(blueprint_path, viewer_path, handoff_path, patch_path)

    assert patch_path.read_text(encoding="utf-8") == original_patch
    assert viewer_path.exists()
    assert handoff_path.exists()
    viewer_html = viewer_path.read_text(encoding="utf-8")
    assert "existing_entry" in viewer_html
    assert "solution.patch.jsonl" in viewer_html
    assert "realPatchEntries" in viewer_html
    assert "savedPatchSnapshot" in viewer_html
