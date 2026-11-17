"""Validate the file-backed project envelope before delivery."""

from pathlib import Path
import re

from .blueprint import find_blueprint_file, read_blueprint_document, validate_blueprint_document
from .engine import load_engine
from .io import append_jsonl, file_lock, read_json, safe_id, sha256_file, write_json_atomic
from .state import (
    STATES,
    _context_matches_current_inputs,
    _find_chapter_body_path,
    _review_metadata_matches_current,
    _settlement_matches_current_inputs,
)
from .wiki import validate_wiki


_REQUIRED_PATHS = (
    ".novelforge/state/project.json",
    ".novelforge/state/chapters",
    ".novelforge/context",
    ".novelforge/reviews",
    ".novelforge/settlements",
    ".novelforge/audit.jsonl",
    "blueprints",
    "chapters",
)
_REQUIRED_DIRECTORIES = set(_REQUIRED_PATHS) - {".novelforge/state/project.json", ".novelforge/audit.jsonl"}


def _engine_root(root, engine_id):
    if engine_id == "jin-yong":
        return Path(__file__).resolve().parents[1] / "engines" / engine_id
    return Path(root) / ".novelforge" / "engines" / engine_id


def verify_project(root):
    root = Path(root).resolve()
    errors = []
    for relative in _REQUIRED_PATHS:
        path = root / relative
        if not path.exists():
            if relative in ("blueprints", "chapters") and (root / "wiki" / relative).exists():
                pass
            else:
                errors.append({"path": relative, "problem": "required project path is missing"})
        elif relative in _REQUIRED_DIRECTORIES and not path.is_dir():
            errors.append({"path": relative, "problem": "required project path is not a directory"})
    project_path = root / ".novelforge" / "state" / "project.json"
    if project_path.is_file():
        project = read_json(project_path)
        if not isinstance(project, dict):
            errors.append({"path": str(project_path.relative_to(root)), "problem": "project profile must be an object"})
            project = {}
        if project.get("schema") != 1:
            errors.append({"path": str(project_path.relative_to(root)), "problem": "unsupported project schema"})
        if not safe_id(project.get("engine")):
            errors.append({"path": str(project_path.relative_to(root)), "problem": "project engine is required"})
        else:
            try:
                load_engine(_engine_root(root, project["engine"]))
            except (OSError, ValueError, KeyError) as exc:
                errors.append({"path": str(project_path.relative_to(root)), "problem": "active engine is invalid: {}".format(exc)})
        if "engines" in project and (
            not isinstance(project["engines"], list)
            or any(not safe_id(item) for item in project["engines"])
        ):
            errors.append({"path": str(project_path.relative_to(root)), "problem": "engines must be a string list"})
        if "style_detectors" in project and not isinstance(project["style_detectors"], list):
            errors.append({"path": str(project_path.relative_to(root)), "problem": "style_detectors must be a list"})
        elif isinstance(project.get("style_detectors"), list) and any(
            not isinstance(item, dict) or not isinstance(item.get("pattern"), str) or not item["pattern"]
            for item in project["style_detectors"]
        ):
            errors.append({"path": str(project_path.relative_to(root)), "problem": "style_detectors require pattern objects"})
        elif isinstance(project.get("style_detectors"), list):
            for item in project["style_detectors"]:
                try:
                    re.compile(item["pattern"])
                except (re.error, TypeError):
                    errors.append({"path": str(project_path.relative_to(root)), "problem": "style detector pattern is invalid"})
                    break
        policies = project.get("policies", {})
        if not isinstance(policies, dict):
            errors.append({"path": str(project_path.relative_to(root)), "problem": "policies must be an object"})
        elif "blocking_rules" in policies and (
            not isinstance(policies["blocking_rules"], list)
            or any(not isinstance(item, str) or not item for item in policies["blocking_rules"])
        ):
            errors.append({"path": str(project_path.relative_to(root)), "problem": "blocking_rules must be a string list"})
        elif policies.get("style_detector_mode", "warning") not in ("warning", "blocking"):
            errors.append({"path": str(project_path.relative_to(root)), "problem": "style_detector_mode must be warning or blocking"})
        if "scale" in project:
            scale = project["scale"]
            if not isinstance(scale, dict):
                errors.append({"path": str(project_path.relative_to(root)), "problem": "scale must be an object"})
            else:
                if scale.get("tier") not in ("short", "novella", "standard", "epic"):
                    errors.append({"path": str(project_path.relative_to(root)), "problem": "scale.tier must be short, novella, standard, or epic"})
                if "target_words" in scale and (not isinstance(scale["target_words"], int) or scale["target_words"] <= 0):
                    errors.append({"path": str(project_path.relative_to(root)), "problem": "scale.target_words must be a positive integer"})
                if "words_per_chapter" in scale and (not isinstance(scale["words_per_chapter"], int) or scale["words_per_chapter"] <= 0):
                    errors.append({"path": str(project_path.relative_to(root)), "problem": "scale.words_per_chapter must be a positive integer"})
    chapters_dir = root / ".novelforge" / "state" / "chapters"
    for state_path in sorted(chapters_dir.glob("*.json")):
        try:
            chapter_state = read_json(state_path)
            chapter = chapter_state.get("chapter", state_path.stem)
            status = chapter_state.get("status")
            if state_path.stem != chapter:
                errors.append({"path": str(state_path.relative_to(root)), "problem": "state filename does not match chapter id"})
            if not safe_id(chapter):
                errors.append({"path": str(state_path.relative_to(root)), "problem": "chapter id is not path-safe"})
                continue
            if status not in STATES:
                errors.append({"path": str(state_path.relative_to(root)), "problem": "unknown chapter state"})
                continue
            blueprint_path = find_blueprint_file(root, chapter)
            if status != "PLANNED":
                if blueprint_path is None or not blueprint_path.is_file():
                    errors.append({"path": f"blueprints/{chapter}.md", "problem": "blueprint is missing"})
                else:
                    blueprint = read_blueprint_document(blueprint_path)
                    try:
                        validate_blueprint_document(blueprint, chapter)
                    except (ValueError, TypeError, KeyError):
                        errors.append({"path": str(blueprint_path.relative_to(root)), "problem": "blueprint is invalid"})
            if status in ("CONTEXT_LOCKED", "DRAFTED", "TEXT_PASS", "ENGINE_PASS", "SETTLED", "DELIVERABLE"):
                context_path = root / ".novelforge" / "context" / (chapter + ".json")
                if blueprint_path is None or not blueprint_path.is_file() or not context_path.is_file():
                    errors.append({"path": str(context_path.relative_to(root)), "problem": "locked context is missing"})
                else:
                    context = read_json(context_path)
                    if not isinstance(context, dict) or context.get("status") != "LOCKED" or not _context_matches_current_inputs(root, chapter, context, blueprint_path):
                        errors.append({"path": str(context_path.relative_to(root)), "problem": "context ticket is stale or invalid"})
            body = _find_chapter_body_path(root, chapter)
            if status in ("DRAFTED", "TEXT_PASS", "ENGINE_PASS", "SETTLED", "DELIVERABLE") and (body is None or not body.is_file()):
                errors.append({"path": f"chapters/{chapter}.md", "problem": "chapter body is missing"})
                continue
            if body is None or not body.is_file():
                continue
            body_hash = sha256_file(body)
            required_reviews = []
            if status in ("TEXT_PASS", "ENGINE_PASS", "SETTLED", "DELIVERABLE"):
                required_reviews.append("text")
            if status in ("ENGINE_PASS", "SETTLED", "DELIVERABLE"):
                required_reviews.append("engine")
            for kind in required_reviews:
                review_path = root / ".novelforge" / "reviews" / (chapter + "-" + kind + ".json")
                if not review_path.is_file():
                    errors.append({"path": str(review_path.relative_to(root)), "problem": "required review is missing"})
                else:
                    review = read_json(review_path)
                    if (
                        not isinstance(review, dict)
                        or review.get("chapter") != chapter
                        or review.get("kind") != kind
                        or review.get("result") != "PASS"
                        or review.get("status") == "STALE"
                    ):
                        errors.append({"path": str(review_path.relative_to(root)), "problem": "review is not a passing artifact"})
                    if not isinstance(review, dict) or review.get("source_hash") != body_hash:
                        errors.append({"path": str(review_path.relative_to(root)), "problem": "review source hash is stale"})
            if required_reviews and not _review_metadata_matches_current(root, chapter, tuple(required_reviews), chapter_state):
                errors.append({"path": str(state_path.relative_to(root)), "problem": "review artifact hash metadata is stale or missing"})
            if status in ("SETTLED", "DELIVERABLE"):
                settlement_path = root / ".novelforge" / "settlements" / (chapter + ".json")
                if not settlement_path.is_file():
                    errors.append({"path": str(settlement_path.relative_to(root)), "problem": "settlement is missing"})
                else:
                    settlement = read_json(settlement_path)
                    if (
                        not isinstance(settlement, dict)
                        or settlement.get("chapter") != chapter
                        or settlement.get("status") == "STALE"
                        or not isinstance(settlement.get("facts", []), list)
                    ):
                        errors.append({"path": str(settlement_path.relative_to(root)), "problem": "settlement is not a valid artifact"})
                    if not isinstance(settlement, dict) or settlement.get("source_hash") != body_hash or not _settlement_matches_current_inputs(root, chapter, settlement, body_hash):
                        errors.append({"path": str(settlement_path.relative_to(root)), "problem": "settlement source hash is stale"})
            if status == "DELIVERABLE":
                manifest_path = root / ".novelforge" / "wiki-manifest.json"
                try:
                    validate_wiki(root)
                except (OSError, ValueError, AttributeError, TypeError):
                    errors.append({"path": str(manifest_path.relative_to(root)), "problem": "wiki manifest is missing or invalid"})
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append({"path": str(state_path.relative_to(root)), "problem": "invalid chapter state: {}".format(exc)})
    return {"status": "FAIL" if errors else "PASS", "errors": errors}


def activate_engine(root, engine_id):
    """Select an installed engine without requiring manual state edits."""
    if not safe_id(engine_id):
        raise ValueError("engine id must be a path-safe identifier")
    root = Path(root).resolve()
    project_path = root / ".novelforge" / "state" / "project.json"
    if not project_path.is_file():
        raise ValueError("project is not initialized")
    engine_root = _engine_root(root, engine_id)
    engine = load_engine(engine_root)
    if engine["id"] != engine_id:
        raise ValueError("engine directory and manifest id do not match")
    lock = root / ".novelforge" / "locks" / "project.lock"
    with file_lock(lock):
        project = read_json(project_path)
        project["engine"] = engine["id"]
        project.setdefault("engines", [])
        if not isinstance(project["engines"], list):
            raise ValueError("project engines must be a string list")
        if engine["id"] not in project["engines"]:
            project["engines"].append(engine["id"])
        write_json_atomic(project_path, project)
        append_jsonl(root / ".novelforge" / "audit.jsonl", {"action": "engine.activate", "engine": engine["id"]})
    return {"status": "PASS", "engine": engine["id"]}
