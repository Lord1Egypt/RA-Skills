"""Validation for domain-knowledge blueprints.

Strict checks (errors):
- meta.blueprintType is in {architecture, domain-knowledge}
- domain-knowledge blueprint requires non-empty meta.detectedIntent
- architecture blueprint must not contain knowledge entities
- domain-knowledge blueprint must contain >=1 knowledge entity
- knowledge entities require id, name, entityType
- IDs are unique within the knowledge block
- relations.from / relations.to must reference existing IDs
- domain-knowledge blueprint requires >=3 clarifyRequests, each pointing to an
  existing entity via targetEntityId

Soft checks (warnings):
- relation type not in the recognised whitelist (allow user-defined types)

Out of scope (deferred to Phase 3, see design v2 §10):
- cycle detection in relations
- semantic validation of relation type ↔ from/to entity types
- soft schema for severity / level / etc.
- entityType camelCase enforcement
"""
from __future__ import annotations

from collections import Counter
from typing import Any


VALID_BLUEPRINT_TYPES = ("architecture", "domain-knowledge")

KNOWLEDGE_RELATION_TYPES = (
    "solves",
    "prevents",
    "measures",
    "enforces",
    "requires",
    "causes",
    "impacts",
    "supports",
    "enforcedBy",
    "measuredBy",
)

ARCHITECTURE_RELATION_TYPES = (
    "supports",
    "depends",
    "realizes",
)

ALL_RELATION_TYPES = frozenset(KNOWLEDGE_RELATION_TYPES + ARCHITECTURE_RELATION_TYPES)


def _issue(
    severity: str,
    error_code: str,
    message: str,
    affected_ids: list[str],
    suggested_fix: str,
) -> dict[str, Any]:
    return {
        "severity": severity,
        "errorCode": error_code,
        "message": message,
        "affectedIds": affected_ids,
        "suggestedFix": suggested_fix,
    }


def _collect_all_ids(blueprint: dict[str, Any]) -> set[str]:
    """Collect every entity id from library (architecture + knowledge)."""
    library = blueprint.get("library", {}) or {}
    ids: set[str] = set()
    for key, collection in library.items():
        if key == "knowledge":
            continue
        if isinstance(collection, list):
            for item in collection:
                if isinstance(item, dict) and "id" in item:
                    ids.add(item["id"])
    knowledge = library.get("knowledge", {}) or {}
    if isinstance(knowledge, dict):
        for entities in knowledge.values():
            if isinstance(entities, list):
                for entity in entities:
                    if isinstance(entity, dict) and "id" in entity:
                        ids.add(entity["id"])
    return ids


def _knowledge_has_any_entity(knowledge: dict[str, Any] | None) -> bool:
    if not isinstance(knowledge, dict):
        return False
    for value in knowledge.values():
        if isinstance(value, list) and value:
            return True
    return False


def validate_meta(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    meta = blueprint.get("meta", {}) or {}
    bp_type = meta.get("blueprintType", "architecture")

    if bp_type not in VALID_BLUEPRINT_TYPES:
        issues.append(_issue(
            "error",
            "INVALID_BLUEPRINT_TYPE",
            f"Invalid blueprintType: {bp_type!r}.",
            [],
            f"Set meta.blueprintType to one of {list(VALID_BLUEPRINT_TYPES)}.",
        ))
        return issues

    if bp_type == "domain-knowledge":
        intent = meta.get("detectedIntent", "")
        if not isinstance(intent, str) or not intent.strip():
            issues.append(_issue(
                "error",
                "MISSING_DETECTED_INTENT",
                "domain-knowledge blueprint must have non-empty meta.detectedIntent.",
                [],
                "Populate meta.detectedIntent with a single-sentence summary of user intent.",
            ))

    return issues


def validate_knowledge_block(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    meta = blueprint.get("meta", {}) or {}
    bp_type = meta.get("blueprintType", "architecture")
    library = blueprint.get("library", {}) or {}
    knowledge = library.get("knowledge", {}) or {}

    if bp_type == "architecture":
        if _knowledge_has_any_entity(knowledge):
            issues.append(_issue(
                "error",
                "ARCHITECTURE_WITH_KNOWLEDGE",
                "architecture blueprint should not contain knowledge entities.",
                [],
                "Set blueprintType to 'domain-knowledge' or remove the knowledge block.",
            ))
        return issues

    # domain-knowledge from here on
    if not _knowledge_has_any_entity(knowledge):
        issues.append(_issue(
            "error",
            "DOMAIN_KNOWLEDGE_EMPTY",
            "domain-knowledge blueprint must have at least one knowledge entity.",
            [],
            "Add entities to library.knowledge (painPoints, strategies, etc.).",
        ))
        return issues

    # Per-entity core field checks + per-block id uniqueness
    knowledge_ids: list[str] = []
    if isinstance(knowledge, dict):
        for type_plural, entities in knowledge.items():
            if not isinstance(entities, list):
                continue
            for entity in entities:
                if not isinstance(entity, dict):
                    issues.append(_issue(
                        "error",
                        "KNOWLEDGE_ENTITY_NOT_OBJECT",
                        f"{type_plural} contains a non-object entity.",
                        [],
                        "Each entity must be a JSON object.",
                    ))
                    continue

                ent_id = entity.get("id")
                ent_label = ent_id if isinstance(ent_id, str) else "<no-id>"
                if not isinstance(ent_id, str) or not ent_id.strip():
                    issues.append(_issue(
                        "error",
                        "KNOWLEDGE_MISSING_ID",
                        f"{type_plural} entity is missing core field 'id'.",
                        [],
                        "Add 'id' (format: '{prefix}-{seq}', e.g. 'pain-001').",
                    ))
                else:
                    knowledge_ids.append(ent_id)

                name = entity.get("name")
                if not isinstance(name, str) or not name.strip():
                    issues.append(_issue(
                        "error",
                        "KNOWLEDGE_MISSING_NAME",
                        f"{type_plural} entity '{ent_label}' is missing core field 'name'.",
                        [ent_label] if ent_label != "<no-id>" else [],
                        "Add a non-empty 'name'.",
                    ))

                entity_type = entity.get("entityType")
                if not isinstance(entity_type, str) or not entity_type.strip():
                    issues.append(_issue(
                        "error",
                        "KNOWLEDGE_MISSING_ENTITYTYPE",
                        f"{type_plural} entity '{ent_label}' is missing core field 'entityType'.",
                        [ent_label] if ent_label != "<no-id>" else [],
                        "Add 'entityType' (e.g. 'painPoint', 'strategy').",
                    ))

    duplicates = [
        item_id for item_id, count in Counter(knowledge_ids).items() if count > 1
    ]
    for dup in duplicates:
        issues.append(_issue(
            "error",
            "KNOWLEDGE_DUPLICATE_ID",
            f"Duplicate knowledge entity id: {dup}.",
            [dup],
            "Rename one of the duplicate entities.",
        ))

    return issues


def validate_relations_basic(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    """Phase-2 minimal relations validation: id refs + type whitelist (warn).

    Cycle detection and semantic validation are deferred (see design v2 §10).
    """
    issues: list[dict[str, Any]] = []
    relations = blueprint.get("relations", []) or []
    if not isinstance(relations, list):
        return issues

    all_ids = _collect_all_ids(blueprint)

    for rel in relations:
        if not isinstance(rel, dict):
            continue
        rel_id = rel.get("id", "<no-id>")
        rel_type = rel.get("type")
        from_id = rel.get("from")
        to_id = rel.get("to")

        if isinstance(rel_type, str) and rel_type not in ALL_RELATION_TYPES:
            issues.append(_issue(
                "warning",
                "RELATION_UNKNOWN_TYPE",
                f"Relation '{rel_id}' uses non-standard type '{rel_type}'.",
                [rel_id] if isinstance(rel_id, str) else [],
                f"Standard types: {sorted(ALL_RELATION_TYPES)}.",
            ))

        if isinstance(from_id, str) and from_id and from_id not in all_ids:
            issues.append(_issue(
                "error",
                "RELATION_MISSING_FROM",
                f"Relation '{rel_id}' references non-existent 'from' id: {from_id}.",
                [rel_id] if isinstance(rel_id, str) else [],
                "Create the entity or fix the reference.",
            ))

        if isinstance(to_id, str) and to_id and to_id not in all_ids:
            issues.append(_issue(
                "error",
                "RELATION_MISSING_TO",
                f"Relation '{rel_id}' references non-existent 'to' id: {to_id}.",
                [rel_id] if isinstance(rel_id, str) else [],
                "Create the entity or fix the reference.",
            ))

    return issues


def validate_clarify_requests(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    """For domain-knowledge blueprints, clarifyRequests are mandatory and structured.

    - >=3 entries
    - Each must have a non-empty 'question'
    - Each must have 'targetEntityId' pointing to an existing library entity

    For architecture blueprints, clarifyRequests are optional (legacy clarify.py
    output that may use 'affectedIds' instead is left untouched here).
    """
    issues: list[dict[str, Any]] = []
    meta = blueprint.get("meta", {}) or {}
    bp_type = meta.get("blueprintType", "architecture")
    if bp_type != "domain-knowledge":
        return issues

    context = blueprint.get("context", {}) or {}
    clarify_requests = context.get("clarifyRequests", []) or []

    if not isinstance(clarify_requests, list) or len(clarify_requests) < 3:
        issues.append(_issue(
            "error",
            "CLARIFY_REQUESTS_INSUFFICIENT",
            f"domain-knowledge blueprint must have >=3 clarifyRequests, got "
            f"{len(clarify_requests) if isinstance(clarify_requests, list) else 0}.",
            [],
            "Generate at least 3 clarification questions targeting library entities.",
        ))
        return issues

    all_ids = _collect_all_ids(blueprint)

    for req in clarify_requests:
        if not isinstance(req, dict):
            continue
        req_id = req.get("id", "<no-id>")
        target_id = req.get("targetEntityId")
        question = req.get("question")

        if not isinstance(target_id, str) or not target_id.strip():
            issues.append(_issue(
                "error",
                "CLARIFY_REQUEST_MISSING_TARGET",
                f"clarifyRequest '{req_id}' missing targetEntityId.",
                [req_id] if isinstance(req_id, str) else [],
                "Each clarification must point to a specific entity via targetEntityId.",
            ))
        elif target_id not in all_ids:
            issues.append(_issue(
                "error",
                "CLARIFY_REQUEST_INVALID_TARGET",
                f"clarifyRequest '{req_id}' targetEntityId '{target_id}' is not in library.",
                [req_id] if isinstance(req_id, str) else [],
                "Fix the entity reference or remove this clarifyRequest.",
            ))

        if not isinstance(question, str) or not question.strip():
            issues.append(_issue(
                "error",
                "CLARIFY_REQUEST_MISSING_QUESTION",
                f"clarifyRequest '{req_id}' missing or empty 'question'.",
                [req_id] if isinstance(req_id, str) else [],
                "Provide specific question text.",
            ))

    return issues


def validate_knowledge_extension(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    """Run all v2 knowledge-related checks. Returns combined issues list."""
    issues: list[dict[str, Any]] = []
    issues.extend(validate_meta(blueprint))
    issues.extend(validate_knowledge_block(blueprint))
    issues.extend(validate_relations_basic(blueprint))
    issues.extend(validate_clarify_requests(blueprint))
    return issues
