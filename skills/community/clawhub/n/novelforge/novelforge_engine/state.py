"""File-backed Novel project state and its non-skippable chapter gates."""

from pathlib import Path

from .io import (
    append_jsonl,
    file_lock,
    read_frontmatter,
    read_json,
    safe_id,
    sha256_file,
    write_frontmatter_atomic,
    write_json_atomic,
)


STATES = (
    "PLANNED",
    "BLUEPRINT_VALID",
    "CONTEXT_LOCKED",
    "DRAFTED",
    "TEXT_PASS",
    "ENGINE_PASS",
    "SETTLED",
    "DELIVERABLE",
)


class InvalidTransition(ValueError):
    pass


def _novel_dir(root):
    return Path(root) / ".novelforge"


def _state_path(root, chapter):
    if not safe_id(chapter):
        raise ValueError("chapter id must be a single path-safe identifier")
    return _novel_dir(root) / "state" / "chapters" / (chapter + ".json")


def _audit(root, event):
    append_jsonl(_novel_dir(root) / "audit.jsonl", event)


def _find_chapter_body_path(root, chapter):
    root = Path(root).resolve()
    candidates = (
        root / "chapters" / (chapter + ".md"),
        root / "chapters" / (chapter + ".txt"),
        root / "wiki" / "chapters" / (chapter + ".md"),
        root / "wiki" / "chapters" / (chapter + ".txt"),
    )
    for c in candidates:
        if c.is_file():
            return c
    return None


def _find_blueprint_path(root, chapter):
    from .blueprint import find_blueprint_file
    return find_blueprint_file(root, chapter)


def _mark_stale_unlocked(root, chapter, reason):
    """Mark every downstream artifact stale while the state lock is held."""
    root = Path(root)
    for artifact in (
        _novel_dir(root) / "context" / (chapter + ".json"),
        _novel_dir(root) / "reviews" / (chapter + "-text.json"),
        _novel_dir(root) / "reviews" / (chapter + "-engine.json"),
        _novel_dir(root) / "settlements" / (chapter + ".json"),
    ):
        if artifact.is_file():
            value = read_json(artifact)
            value["status"] = "STALE"
            value["invalidated"] = reason
            write_json_atomic(artifact, value)

    # Invalidate story files originated from this chapter
    from .wiki import WIKI_FOLDERS
    search_dirs = [root / f for f in WIKI_FOLDERS if (root / f).is_dir()]
    if (root / "wiki").is_dir():
        search_dirs.append(root / "wiki")

    for folder_dir in search_dirs:
        for artifact in folder_dir.rglob("*.md"):
            if artifact.name == "index.md":
                continue
            try:
                meta, body = read_frontmatter(artifact)
            except Exception:
                continue
            if isinstance(meta, dict) and meta.get("_source_chapter") == chapter:
                meta["status"] = "STALE"
                meta["invalidated"] = reason
                write_frontmatter_atomic(artifact, meta, body)

    # Legacy support for .novelforge/state/<folder>/*.json
    for folder in ("entities", "hooks", "relations", "timeline"):
        folder_path = _novel_dir(root) / "state" / folder
        if folder_path.is_dir():
            for artifact in folder_path.glob("*.json"):
                try:
                    value = read_json(artifact)
                except (OSError, ValueError, TypeError):
                    continue
                if isinstance(value, dict) and value.get("_source_chapter") == chapter:
                    value["status"] = "STALE"
                    value["invalidated"] = reason
                    write_json_atomic(artifact, value)

    state_path = _state_path(root, chapter)
    if state_path.is_file():
        current = read_json(state_path)
        if isinstance(current.get("metadata"), dict):
            current["metadata"].pop("review", None)
            current["metadata"].pop("review_kind", None)
            current["metadata"].pop("review_hash", None)
            current["metadata"].pop("review_hashes", None)
        current.update({"status": "PLANNED", "invalidated": reason, "version": int(current.get("version", 0)) + 1})
        write_json_atomic(state_path, current)
    _audit(root, {"action": "chapter.invalidate", "chapter": chapter, "reason": reason})


def _read_current_review(root, chapter, kind, body_hash):
    artifact = _novel_dir(root) / "reviews" / (chapter + "-" + kind + ".json")
    if not artifact.is_file():
        raise InvalidTransition("{} review with current source hash is required".format(kind))
    review = read_json(artifact)
    if (
        not isinstance(review, dict)
        or review.get("chapter") != chapter
        or review.get("kind") != kind
        or review.get("result") != "PASS"
        or review.get("status") == "STALE"
        or review.get("source_hash") != body_hash
    ):
        raise InvalidTransition("{} review with current source hash is required".format(kind))


def _review_metadata_matches_current(root, chapter, kinds, state):
    metadata = state.get("metadata") if isinstance(state, dict) else None
    review_hashes = metadata.get("review_hashes") if isinstance(metadata, dict) else None
    if not isinstance(review_hashes, dict) or set(review_hashes) != set(kinds):
        return False
    for kind in kinds:
        path = _novel_dir(root) / "reviews" / (chapter + "-" + kind + ".json")
        if not path.is_file() or review_hashes.get(kind) != sha256_file(path):
            return False
    return True


def _context_matches_current_inputs(root, chapter, ticket, blueprint_path):
    """Validate a Context Ticket against its declared files and active engine."""
    if not isinstance(ticket, dict) or ticket.get("schema") != 1 or ticket.get("chapter") != chapter:
        return False
    dependencies = ticket.get("dependencies")
    if not isinstance(dependencies, dict):
        return False
    if any(not isinstance(values, list) or any(not safe_id(value) for value in values) for values in dependencies.values()):
        return False
    if not isinstance(ticket.get("dependency_hashes"), dict) or not isinstance(ticket.get("payload"), dict):
        return False
    snapshot = ticket.get("engine_snapshot")
    if (
        not isinstance(snapshot, dict)
        or not safe_id(snapshot.get("id"))
        or not isinstance(snapshot.get("version"), int)
        or isinstance(snapshot.get("version"), bool)
        or not isinstance(snapshot.get("active_cards"), list)
        or any(not isinstance(card_id, str) or not card_id for card_id in snapshot.get("active_cards", []))
        or not isinstance(snapshot.get("source_hashes"), dict)
        or any(not isinstance(digest, str) or len(digest) != 64 for digest in snapshot.get("source_hashes", {}).values())
    ):
        return False
    try:
        from .blueprint import read_blueprint_document
        from .context import _engine_snapshot, _load_dependencies

        blueprint = read_blueprint_document(blueprint_path)
        if not isinstance(blueprint, dict) or ticket.get("dependencies") != blueprint.get("dependencies"):
            return False
        payload, dependency_hashes = _load_dependencies(Path(root), dependencies)
        return (
            ticket.get("blueprint_hash") == sha256_file(blueprint_path)
            and ticket.get("payload") == payload
            and ticket.get("dependency_hashes") == dependency_hashes
            and snapshot == _engine_snapshot(Path(root), blueprint)
        )
    except (OSError, ValueError, KeyError, TypeError):
        return False


def _settlement_matches_current_inputs(root, chapter, settlement, body_hash):
    if (
        not isinstance(settlement, dict)
        or settlement.get("schema") != 1
        or settlement.get("chapter") != chapter
        or settlement.get("status") != "APPLIED"
        or settlement.get("source_hash") != body_hash
        or not isinstance(settlement.get("facts"), list)
        or not isinstance(settlement.get("review_hashes"), dict)
        or settlement.get("applied") is not True
        or set(settlement.get("review_hashes", {})) != {"text", "engine"}
        or any(
            not isinstance(value, str) or len(value) != 64
            for value in settlement.get("review_hashes", {}).values()
        )
    ):
        return False
    for kind in ("text", "engine"):
        review_path = _novel_dir(root) / "reviews" / (chapter + "-" + kind + ".json")
        try:
            _read_current_review(root, chapter, kind, body_hash)
            if settlement["review_hashes"].get(kind) != sha256_file(review_path):
                return False
        except (OSError, ValueError, KeyError, TypeError, InvalidTransition):
            return False
    fact_ids = set()
    folder_by_type = {
        "entity": "entities",
        "character": "characters",
        "location": "locations",
        "item": "items",
        "faction": "factions",
        "hook": "hooks",
        "relation": "relations",
        "event": "timeline",
    }
    for fact in settlement["facts"]:
        if (
            not isinstance(fact, dict)
            or not safe_id(fact.get("id"))
            or fact.get("type") not in folder_by_type
            or fact["id"] in fact_ids
        ):
            return False
        fact_ids.add(fact["id"])
        folder = folder_by_type.get(fact["type"], "entities")
        wiki_file = Path(root) / folder / (fact["id"] + ".md")
        if not wiki_file.is_file():
            wiki_file = Path(root) / "wiki" / folder / (fact["id"] + ".md")
        legacy_folder = {"hook": "hooks", "relation": "relations", "event": "timeline"}.get(fact["type"], "entities")
        legacy_file = Path(root) / ".novelforge" / "state" / legacy_folder / (fact["id"] + ".json")
        if wiki_file.is_file():
            try:
                value, _ = read_frontmatter(wiki_file)
            except Exception:
                return False
        elif legacy_file.is_file():
            try:
                value = read_json(legacy_file)
            except Exception:
                return False
        else:
            return False

        expected_projection = dict(fact)
        expected_projection.update({"_source_chapter": chapter, "_source_body_hash": body_hash})
        if not isinstance(value, dict):
            return False
        # compare shared keys
        for k, v in expected_projection.items():
            if value.get(k) != v:
                return False
    return True


def _require_transition_artifact(root, chapter, target):
    root = Path(root)
    if target in ("DRAFTED", "TEXT_PASS", "ENGINE_PASS", "SETTLED", "DELIVERABLE"):
        context_path = _novel_dir(root) / "context" / (chapter + ".json")
        blueprint_path = _find_blueprint_path(root, chapter)
        context = read_json(context_path) if context_path.is_file() else {}
        if (
            not context_path.is_file()
            or blueprint_path is None
            or not isinstance(context, dict)
            or context.get("status") != "LOCKED"
            or not _context_matches_current_inputs(root, chapter, context, blueprint_path)
        ):
            _mark_stale_unlocked(root, chapter, "context input changed before chapter transition")
            raise InvalidTransition("locked context artifact is stale or missing")
    current_state = read_chapter_state(root, chapter)
    if target in ("ENGINE_PASS", "SETTLED", "DELIVERABLE"):
        kinds = ("text",) if target == "ENGINE_PASS" else ("text", "engine")
        if not _review_metadata_matches_current(root, chapter, kinds, current_state):
            _mark_stale_unlocked(root, chapter, "review artifact hash changed")
            raise InvalidTransition("review artifact hash metadata is stale or missing")
    if target == "BLUEPRINT_VALID":
        from .blueprint import read_blueprint_document
        artifact = _find_blueprint_path(root, chapter)
        if artifact is None:
            raise InvalidTransition("blueprint artifact is required")
        blueprint = read_blueprint_document(artifact)
        dependencies = blueprint.get("dependencies") if isinstance(blueprint, dict) else None
        if (
            not isinstance(blueprint, dict)
            or blueprint.get("id") != chapter
            or not isinstance(blueprint.get("phase"), str)
            or not blueprint["phase"].strip()
            or not isinstance(dependencies, dict)
            or any(
                not isinstance(values, list)
                or any(not safe_id(identifier) for identifier in values)
                for values in dependencies.values()
            )
        ):
            raise InvalidTransition("valid blueprint artifact is required")
        if "scene_types" in blueprint and (
            not isinstance(blueprint["scene_types"], list)
            or any(not isinstance(value, str) or not value for value in blueprint["scene_types"])
        ):
            raise InvalidTransition("valid blueprint artifact is required")
        if "state" in blueprint and not isinstance(blueprint["state"], dict):
            raise InvalidTransition("valid blueprint artifact is required")
        if "scenes" in blueprint:
            scenes = blueprint["scenes"]
            if not isinstance(scenes, list):
                raise InvalidTransition("valid blueprint artifact is required")
            for scene in scenes:
                required = ("id", "location", "characters", "goal", "pressure", "information_change", "exit_state")
                if (
                    not isinstance(scene, dict)
                    or not safe_id(scene.get("id"))
                    or not isinstance(scene.get("location"), str)
                    or not isinstance(scene.get("characters"), list)
                    or any(not isinstance(value, str) for value in scene["characters"])
                    or any(not isinstance(scene.get(key), str) for key in required[3:])
                ):
                    raise InvalidTransition("valid blueprint artifact is required")
        if "settlement" in blueprint:
            settlement = blueprint["settlement"]
            if (
                not isinstance(settlement, dict)
                or not isinstance(settlement.get("changes", []), list)
                or not isinstance(settlement.get("next_question", ""), str)
            ):
                raise InvalidTransition("valid blueprint artifact is required")
    elif target == "CONTEXT_LOCKED":
        artifact = _novel_dir(root) / "context" / (chapter + ".json")
        blueprint = _find_blueprint_path(root, chapter)
        ticket = read_json(artifact) if artifact.is_file() else {}
        if (
            not artifact.is_file()
            or not isinstance(ticket, dict)
            or ticket.get("chapter") != chapter
            or ticket.get("status") != "LOCKED"
            or blueprint is None
            or ticket.get("blueprint_hash") != sha256_file(blueprint)
            or not _context_matches_current_inputs(root, chapter, ticket, blueprint)
        ):
            raise InvalidTransition("locked context artifact is required")
    elif target == "DRAFTED":
        artifact = _find_chapter_body_path(root, chapter)
        if artifact is None or not artifact.read_bytes():
            raise InvalidTransition("chapter body is required")
    elif target in ("TEXT_PASS", "ENGINE_PASS", "SETTLED", "DELIVERABLE"):
        body = _find_chapter_body_path(root, chapter)
        if body is None:
            raise InvalidTransition("chapter body is required")
        body_hash = sha256_file(body)
        required_reviews = ("text",) if target == "TEXT_PASS" else ("text", "engine")
        for kind in required_reviews:
            try:
                _read_current_review(root, chapter, kind, body_hash)
            except InvalidTransition:
                if target != "TEXT_PASS":
                    _mark_stale_unlocked(root, chapter, "review source hash changed")
                raise
        if target in ("SETTLED", "DELIVERABLE"):
            artifact = _novel_dir(root) / "settlements" / (chapter + ".json")
            settlement = read_json(artifact) if artifact.is_file() else {}
            valid_settlement = _settlement_matches_current_inputs(root, chapter, settlement, body_hash)
            if not valid_settlement:
                _mark_stale_unlocked(root, chapter, "settlement source hash changed")
                raise InvalidTransition("settlement with current source hash is required")
        if target == "DELIVERABLE":
            from .wiki import validate_wiki

            try:
                validate_wiki(root)
            except (OSError, ValueError, TypeError) as exc:
                raise InvalidTransition("story wiki artifact is missing or stale: {}".format(exc))


def init_project(root):
    root = Path(root).resolve()
    directories = (
        root / ".novelforge" / "state" / "chapters",
        root / ".novelforge" / "context",
        root / ".novelforge" / "reviews",
        root / ".novelforge" / "settlements",
        root / ".novelforge" / "locks",
        root / "blueprints",
        root / "chapters",
        root / "characters",
        root / "locations",
        root / "items",
        root / "factions",
        root / "hooks",
        root / "relations",
        root / "timeline",
        root / "entities",
    )
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    index_file = root / "index.md"
    if not index_file.exists():
        from .wiki import rebuild_wiki
        rebuild_wiki(root)
    project = _novel_dir(root) / "state" / "project.json"
    if not project.exists():
        write_json_atomic(
            project,
            {
                "schema": 1,
                "name": root.name,
                "engine": "jin-yong",
                "engines": ["jin-yong"],
                "style_detectors": [],
                "policies": {"style_detector_mode": "warning"},
            },
        )
    _audit(root, {"action": "project.init", "root": str(root), "schema": 1})
    return read_json(project)


def read_chapter_state(root, chapter):
    path = _state_path(root, chapter)
    if not path.exists():
        return {"chapter": chapter, "status": "PLANNED", "version": 0}
    return read_json(path)


def transition_chapter(root, chapter, target, metadata=None):
    if target not in STATES:
        raise InvalidTransition("unknown chapter state: " + str(target))
    root = Path(root).resolve()
    lock = _novel_dir(root) / "locks" / "state.lock"
    with file_lock(lock):
        current = read_chapter_state(root, chapter)
        current_status = current["status"]
        try:
            expected = STATES[STATES.index(current_status) + 1]
        except (ValueError, IndexError):
            expected = None
        if target != expected:
            raise InvalidTransition("cannot transition {} from {} to {}".format(chapter, current_status, target))
        _require_transition_artifact(root, chapter, target)
        updated = dict(current)
        updated.update({"chapter": chapter, "status": target, "version": int(current.get("version", 0)) + 1})
        if metadata:
            merged_metadata = dict(current.get("metadata", {})) if isinstance(current.get("metadata"), dict) else {}
            prior_review_hashes = dict(merged_metadata.get("review_hashes", {})) if isinstance(merged_metadata.get("review_hashes"), dict) else {}
            merged_metadata.update(metadata)
            merged_review_hashes = prior_review_hashes
            if isinstance(metadata.get("review_hashes"), dict):
                merged_review_hashes.update(metadata["review_hashes"])
            if merged_review_hashes:
                merged_metadata["review_hashes"] = merged_review_hashes
            updated["metadata"] = merged_metadata
        write_json_atomic(_state_path(root, chapter), updated)
        _audit(root, {"action": "chapter.transition", "chapter": chapter, "from": current_status, "to": target})
        return updated


def invalidate_chapter(root, chapter, reason):
    root = Path(root).resolve()
    lock = _novel_dir(root) / "locks" / "state.lock"
    with file_lock(lock):
        _mark_stale_unlocked(root, chapter, reason)
