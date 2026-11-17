"""Idempotent chapter settlement and native wiki fact updates."""

from pathlib import Path

from .io import (
    format_frontmatter,
    parse_frontmatter,
    read_frontmatter,
    read_json,
    safe_id,
    sha256_file,
    write_frontmatter_atomic,
    write_json_atomic,
)
from .state import invalidate_chapter, read_chapter_state, transition_chapter
from .wiki import rebuild_wiki


class SettlementError(ValueError):
    pass


_FOLDER_BY_TYPE = {
    "entity": "entities",
    "character": "characters",
    "location": "locations",
    "item": "items",
    "faction": "factions",
    "hook": "hooks",
    "relation": "relations",
    "event": "timeline",
}


def _safe_id(value):
    return safe_id(value)


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


def _validate(settlement):
    if not isinstance(settlement, dict) or not _safe_id(settlement.get("chapter")):
        raise SettlementError("settlement requires chapter")
    if not isinstance(settlement.get("source_hash"), str) or len(settlement["source_hash"]) != 64:
        raise SettlementError("settlement requires sha256 source_hash")
    if not isinstance(settlement.get("facts", []), list):
        raise SettlementError("settlement facts must be a list")
    fact_ids = set()
    for fact in settlement["facts"]:
        if not isinstance(fact, dict) or not _safe_id(fact.get("id")) or fact.get("type") not in _FOLDER_BY_TYPE:
            raise SettlementError("fact requires id and known type")
        if fact["id"] in fact_ids:
            raise SettlementError("settlement fact ids must be unique")
        fact_ids.add(fact["id"])


def _current_review_hashes(root, chapter, body_hash):
    hashes = {}
    for kind in ("text", "engine"):
        path = root / ".novelforge" / "reviews" / (chapter + "-" + kind + ".json")
        if not path.is_file():
            raise SettlementError("{} review is required before settlement".format(kind))
        review = read_json(path)
        if (
            not isinstance(review, dict)
            or review.get("chapter") != chapter
            or review.get("kind") != kind
            or review.get("result") != "PASS"
            or review.get("status") == "STALE"
            or review.get("source_hash") != body_hash
        ):
            raise SettlementError("{} review is stale".format(kind))
        hashes[kind] = sha256_file(path)
    return hashes


def apply_settlement(root, settlement):
    _validate(settlement)
    root = Path(root).resolve()
    chapter = settlement["chapter"]
    state = read_chapter_state(root, chapter)
    target = root / ".novelforge" / "settlements" / (chapter + ".json")
    body_path = _find_chapter_body_path(root, chapter)
    if target.exists():
        existing = read_json(target)
        if existing.get("status") == "STALE":
            pass
        elif body_path is None or sha256_file(body_path) != existing.get("source_hash"):
            existing["status"] = "STALE"
            write_json_atomic(target, existing)
            invalidate_chapter(root, chapter, "chapter body hash changed")
            raise SettlementError("settlement is stale; pass the chapter gates again")
    if body_path is None or sha256_file(body_path) != settlement["source_hash"]:
        if state["status"] in ("TEXT_PASS", "ENGINE_PASS"):
            invalidate_chapter(root, chapter, "chapter body hash changed before settlement")
        raise SettlementError("chapter body hash does not match settlement")
    canonical = dict(settlement)
    canonical["schema"] = 1
    canonical["status"] = "APPLIED"
    try:
        canonical["review_hashes"] = _current_review_hashes(root, chapter, settlement["source_hash"])
    except SettlementError:
        if state["status"] in ("TEXT_PASS", "ENGINE_PASS"):
            invalidate_chapter(root, chapter, "chapter body or review hash changed before settlement")
        raise
    canonical["applied"] = True
    if target.exists() and existing.get("status") != "STALE":
        if existing.get("review_hashes") != canonical["review_hashes"]:
            existing["status"] = "STALE"
            write_json_atomic(target, existing)
            invalidate_chapter(root, chapter, "settlement review evidence changed")
            raise SettlementError("settlement review evidence is stale; pass the chapter gates again")
        if existing == canonical:
            return {"idempotent": True, "chapter": chapter}
        raise SettlementError("settlement already exists with different content")
    if state["status"] != "ENGINE_PASS":
        raise SettlementError("settlement requires ENGINE_PASS")

    # Clean up obsolete facts from previous stale settlement if type/folder changed
    old_facts = existing.get("facts", []) if target.exists() and isinstance(existing, dict) and existing.get("status") == "STALE" else []
    current_facts = {fact["id"]: fact for fact in canonical["facts"]}
    for fact in old_facts:
        if not isinstance(fact, dict):
            continue
        replacement = current_facts.get(fact.get("id"))
        folder = _FOLDER_BY_TYPE.get(fact.get("type"))
        replacement_folder = _FOLDER_BY_TYPE.get(replacement.get("type")) if isinstance(replacement, dict) else None
        if replacement_folder == folder:
            continue
        if not folder or not _safe_id(fact.get("id")):
            continue
        # check file path
        wiki_file = root / folder / (fact["id"] + ".md")
        if not wiki_file.is_file():
            wiki_file = root / "wiki" / folder / (fact["id"] + ".md")
        if wiki_file.is_file():
            try:
                meta, _ = read_frontmatter(wiki_file)
                if meta.get("_source_chapter") == chapter:
                    wiki_file.unlink()
            except (OSError, ValueError):
                pass

    # Normalize character pressure_events into personality.pressure_log
    normalized_facts = []
    for fact in canonical["facts"]:
        fact = dict(fact)
        if fact.get("type") == "character" and isinstance(fact.get("pressure_event"), dict):
            pe = fact.pop("pressure_event")
            folder = _FOLDER_BY_TYPE[fact["type"]]
            entity_wiki = root / folder / (fact["id"] + ".md")
            if not entity_wiki.is_file():
                entity_wiki = root / "wiki" / folder / (fact["id"] + ".md")
            personality = {}
            if entity_wiki.is_file():
                try:
                    existing_meta, _ = read_frontmatter(entity_wiki)
                    if isinstance(existing_meta.get("personality"), dict):
                        personality = dict(existing_meta["personality"])
                except (OSError, ValueError):
                    personality = {}
            elif (root / ".novelforge" / "state" / "entities" / (fact["id"] + ".json")).is_file():
                try:
                    legacy = read_json(root / ".novelforge" / "state" / "entities" / (fact["id"] + ".json"))
                    if isinstance(legacy.get("personality"), dict):
                        personality = dict(legacy["personality"])
                except (OSError, ValueError):
                    personality = {}

            log = list(personality.get("pressure_log", []))
            log.append({"chapter": chapter, "event": pe.get("event", ""), "weight": pe.get("weight", 0), "toward": pe.get("toward", "")})
            personality["pressure_log"] = log
            fact["personality"] = personality
        normalized_facts.append(fact)
    canonical["facts"] = normalized_facts

    # Write each fact into root/folder/
    for fact in canonical["facts"]:
        folder = _FOLDER_BY_TYPE[fact["type"]]
        folder_path = root / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        wiki_path = folder_path / (fact["id"] + ".md")
        existing_meta = {}
        existing_body = ""
        if wiki_path.is_file():
            try:
                existing_meta, existing_body = read_frontmatter(wiki_path)
            except Exception:
                existing_meta, existing_body = {}, ""
        elif (root / "wiki" / folder / (fact["id"] + ".md")).is_file():
            try:
                existing_meta, existing_body = read_frontmatter(root / "wiki" / folder / (fact["id"] + ".md"))
            except Exception:
                existing_meta, existing_body = {}, ""

        meta = dict(existing_meta)
        meta.update(fact)
        meta["_source_chapter"] = chapter
        meta["_source_body_hash"] = canonical["source_hash"]

        body = existing_body
        if not body.strip():
            name = meta.get("name", meta.get("id", "Untitled"))
            lines = [f"# {name}\n"]
            for key in sorted(meta):
                if key in ("id", "name", "type", "_source_chapter", "_source_body_hash", "personality"):
                    continue
                lines.append(f"\n## {key.replace('_', ' ').title()}\n\n{meta[key]}")
            body = "\n".join(lines).rstrip() + "\n"

        write_frontmatter_atomic(wiki_path, meta, body)

    write_json_atomic(target, canonical)
    rebuild_wiki(root)
    transition_chapter(root, chapter, "SETTLED", {"settlement_hash": sha256_file(target)})
    return {"idempotent": False, "chapter": chapter}
