#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

PREDICATE_MAP = {
    "publish": "published",
    "release": "released",
    "work_for": "works_for",
}


def normalize_entities(entities):
    canonical = {}
    result = []
    id_map = {}
    for ent in entities:
        key = (ent.get("canonical_name", "").strip().lower(), ent.get("type"))
        if key in canonical:
            id_map[ent["id"]] = canonical[key]["id"]
            continue
        canonical[key] = ent
        id_map[ent["id"]] = ent["id"]
        result.append(ent)
    return result, id_map


def normalize_relations(relations, id_map):
    out = []
    seen = set()
    for rel in relations:
        rel = dict(rel)
        rel["subject"] = id_map.get(rel["subject"], rel["subject"])
        rel["object"] = id_map.get(rel["object"], rel["object"])
        rel["predicate"] = PREDICATE_MAP.get(rel["predicate"], rel["predicate"])
        key = (rel["subject"], rel["predicate"], rel["object"])
        if key in seen:
            continue
        seen.add(key)
        out.append(rel)
    return out


def normalize_attributes(attributes, id_map):
    out = []
    seen = set()
    for attr in attributes:
        attr = dict(attr)
        attr["entity_id"] = id_map.get(attr["entity_id"], attr["entity_id"])
        key = (attr["entity_id"], attr["attribute"], str(attr["value"]))
        if key in seen:
            continue
        seen.add(key)
        out.append(attr)
    return out


def main():
    parser = argparse.ArgumentParser(description="Normalize extraction results")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text())
    entities, id_map = normalize_entities(data.get("entities", []))
    relations = normalize_relations(data.get("relations", []), id_map)
    attributes = normalize_attributes(data.get("attributes", []), id_map)

    id_to_name = {e["id"]: e.get("canonical_name", e["id"]) for e in entities}
    triples = []
    for rel in relations:
        triples.append({
            "subject": id_to_name.get(rel["subject"], rel["subject"]),
            "predicate": rel["predicate"],
            "object": id_to_name.get(rel["object"], rel["object"]),
            "evidence": rel.get("evidence"),
            "confidence": rel.get("confidence"),
        })
    for attr in attributes:
        triples.append({
            "subject": id_to_name.get(attr["entity_id"], attr["entity_id"]),
            "predicate": attr["attribute"],
            "object": attr["value"],
            "evidence": attr.get("evidence"),
            "confidence": attr.get("confidence"),
        })
    for event in data.get("events", []):
        event_id = event.get("id")
        event_type = event.get("type")
        if event_id and event_type:
            triples.append({
                "subject": event_id,
                "predicate": "is_a",
                "object": event_type,
                "evidence": event.get("evidence"),
                "confidence": event.get("confidence"),
            })
        if event_id and event.get("time"):
            triples.append({
                "subject": event_id,
                "predicate": "occurs_at",
                "object": event.get("time"),
                "evidence": event.get("evidence"),
                "confidence": event.get("confidence"),
            })

    out = {
        "triples": triples,
        "entities": entities,
        "relations": relations,
        "attributes": attributes,
        "events": data.get("events", []),
        "ambiguities": data.get("ambiguities", []),
    }
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(args.output)


if __name__ == "__main__":
    main()
