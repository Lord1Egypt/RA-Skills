"""Deterministic Context Ticket construction from explicit dependency IDs."""

import json
from pathlib import Path

from .blueprint import find_blueprint_file, read_blueprint_document
from .engine import load_engine, select_cards
from .io import read_frontmatter, read_json, safe_id, sha256_file, write_json_atomic
from .state import (
    _settlement_matches_current_inputs,
    invalidate_chapter,
    read_chapter_state,
    transition_chapter,
)


class ContextError(ValueError):
    pass


_KIND_FOLDERS = {
    "entities": ("characters", "locations", "items", "factions", "entities", "wiki/characters", "wiki/locations", "wiki/items", "wiki/factions", "wiki/entities", ".novelforge/state/entities"),
    "characters": ("characters", "wiki/characters"),
    "locations": ("locations", "wiki/locations"),
    "items": ("items", "wiki/items"),
    "factions": ("factions", "wiki/factions"),
    "hooks": ("hooks", "wiki/hooks", ".novelforge/state/hooks"),
    "relations": ("relations", "wiki/relations", ".novelforge/state/relations"),
    "events": ("timeline", "wiki/timeline", ".novelforge/state/timeline"),
}


def _safe_id(value):
    return safe_id(value)


def _find_dependency_path(root, kind, identifier):
    root = Path(root).resolve()
    folders = _KIND_FOLDERS.get(kind, ())
    for folder_rel in folders:
        folder = root / folder_rel
        for ext in (".md", ".json"):
            candidate = folder / (identifier + ext)
            if candidate.is_file():
                return candidate
    return None


def _read_dependency(path):
    path = Path(path)
    if path.suffix == ".md":
        meta, _body = read_frontmatter(path)
        return meta
    return read_json(path)


def _find_chapter_body_path(root, chapter):
    root = Path(root).resolve()
    candidates = (
        root / "wiki" / "chapters" / (chapter + ".md"),
        root / "wiki" / "chapters" / (chapter + ".txt"),
        root / "chapters" / (chapter + ".md"),
        root / "chapters" / (chapter + ".txt"),
    )
    for c in candidates:
        if c.is_file():
            return c
    return None


def _load_dependencies(root, dependencies):
    root = Path(root).resolve()
    loaded = {}
    hashes = {}
    for kind, ids in dependencies.items():
        if kind not in _KIND_FOLDERS or not isinstance(ids, list):
            raise ContextError("dependencies must use known list fields")
        loaded[kind] = []
        for identifier in ids:
            if not _safe_id(identifier):
                raise ContextError("unsafe dependency id")
            path = _find_dependency_path(root, kind, identifier)
            if path is None:
                raise ContextError("missing dependency: {}".format(identifier))
            value = _read_dependency(path)
            if not isinstance(value, dict):
                raise ContextError("dependency must be an object: {}".format(identifier))
            if value.get("status") == "STALE":
                raise ContextError("stale dependency: {}".format(identifier))
            owner = value.get("_source_chapter")
            if owner is not None:
                if not _safe_id(owner):
                    raise ContextError("dependency provenance is invalid: {}".format(identifier))
                source_hash = value.get("_source_body_hash")
                body_path = _find_chapter_body_path(root, owner)
                settlement_path = root / ".novelforge" / "settlements" / (owner + ".json")
                if (
                    not isinstance(source_hash, str)
                    or len(source_hash) != 64
                    or body_path is None
                    or sha256_file(body_path) != source_hash
                    or not settlement_path.is_file()
                ):
                    raise ContextError("dependency provenance is stale: {}".format(identifier))
                owner_settlement = read_json(settlement_path)
                if (
                    not isinstance(owner_settlement, dict)
                    or owner_settlement.get("status") != "APPLIED"
                    or owner_settlement.get("applied") is not True
                    or owner_settlement.get("source_hash") != source_hash
                ):
                    raise ContextError("dependency settlement is stale: {}".format(identifier))
                if not _settlement_matches_current_inputs(root, owner, owner_settlement, source_hash):
                    raise ContextError("dependency settlement artifact is stale: {}".format(identifier))
            loaded[kind].append(value)
            hashes["{}:{}".format(kind, identifier)] = sha256_file(path)
    return loaded, hashes


def _engine_root(root, engine_id):
    if engine_id == "jin-yong":
        return Path(__file__).resolve().parents[1] / "engines" / engine_id
    return Path(root) / ".novelforge" / "engines" / engine_id


def _engine_snapshot(root, blueprint):
    project = read_json(Path(root) / ".novelforge" / "state" / "project.json")
    engine_id = project.get("engine")
    if not safe_id(engine_id):
        raise ContextError("project engine is required")
    engine_root = _engine_root(root, engine_id)
    expected_root = (
        Path(__file__).resolve().parents[1] / "engines" / engine_id
        if engine_id == "jin-yong"
        else Path(root) / ".novelforge" / "engines" / engine_id
    ).resolve()
    if engine_root.resolve() != expected_root:
        raise ContextError("engine root is outside the project engine directory")
    engine = load_engine(engine_root)
    state = dict(blueprint.get("state", {}))
    state.update({"phase": blueprint.get("phase"), "scene_types": blueprint.get("scene_types", [])})
    cards = select_cards(engine_root, state)
    manifest_path = engine_root / "manifest.json"
    if manifest_path.is_file():
        manifest = read_json(manifest_path)
        source_hashes = dict(manifest.get("files", {}))
    else:
        source_hashes = {"engine.json": sha256_file(engine_root / "engine.json")}
        for relative in engine.get("card_files", []):
            source_hashes[relative] = sha256_file(engine_root / relative)
    return {
        "id": engine["id"],
        "version": engine["version"],
        "active_cards": [card["id"] for card in cards],
        "source_hashes": source_hashes,
    }


def build_context(root, chapter):
    root = Path(root).resolve()
    if not safe_id(chapter):
        raise ContextError("chapter id must be path-safe")
    blueprint_path = find_blueprint_file(root, chapter)
    if blueprint_path is None:
        raise ContextError("missing blueprint: {}".format(chapter))
    blueprint = read_blueprint_document(blueprint_path)
    if blueprint.get("id") != chapter:
        raise ContextError("blueprint id does not match chapter")
    dependencies = blueprint.get("dependencies")
    if not isinstance(dependencies, dict):
        raise ContextError("blueprint dependencies are required")
    state = read_chapter_state(root, chapter)
    output = root / ".novelforge" / "context" / (chapter + ".json")
    if state["status"] == "CONTEXT_LOCKED" and output.is_file():
        existing = read_json(output)
        if existing.get("blueprint_hash") != sha256_file(blueprint_path):
            existing["status"] = "STALE"
            write_json_atomic(output, existing)
            invalidate_chapter(root, chapter, "blueprint hash changed")
            raise ContextError("locked context is stale; validate the blueprint again")
    if state["status"] == "PLANNED":
        raise ContextError("blueprint must pass validation before context build")
    if state["status"] not in ("BLUEPRINT_VALID", "CONTEXT_LOCKED"):
        raise ContextError("context cannot be built from {}".format(state["status"]))
    try:
        loaded, hashes = _load_dependencies(root, dependencies)
        engine_snapshot = _engine_snapshot(root, blueprint)
    except (ContextError, OSError, ValueError, KeyError, TypeError) as exc:
        if state["status"] == "CONTEXT_LOCKED" and output.is_file():
            invalidate_chapter(root, chapter, "context input became stale: {}".format(exc))
        if isinstance(exc, ContextError):
            raise
        raise ContextError("context input is invalid: {}".format(exc))
    if state["status"] == "CONTEXT_LOCKED" and output.is_file():
        existing = read_json(output)
        if existing.get("dependency_hashes", {}) != hashes:
            existing["status"] = "STALE"
            write_json_atomic(output, existing)
            invalidate_chapter(root, chapter, "dependency hash changed")
            raise ContextError("locked context is stale; dependency changed")
        if existing.get("engine_snapshot") != engine_snapshot:
            existing["status"] = "STALE"
            write_json_atomic(output, existing)
            invalidate_chapter(root, chapter, "engine snapshot changed")
            raise ContextError("locked context is stale; engine changed")
    ticket = {
        "schema": 1,
        "chapter": chapter,
        "blueprint_hash": sha256_file(blueprint_path),
        "dependencies": dependencies,
        "payload": loaded,
        "dependency_hashes": hashes,
        "engine_snapshot": engine_snapshot,
        "status": "LOCKED",
    }
    write_json_atomic(output, ticket)
    if state["status"] == "BLUEPRINT_VALID":
        transition_chapter(root, chapter, "CONTEXT_LOCKED", {"context_hash": sha256_file(output)})
    return ticket
