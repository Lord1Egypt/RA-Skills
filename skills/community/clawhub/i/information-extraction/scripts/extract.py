#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

ENTITY_PATTERNS = [
    ("Organization", re.compile(r"\b(OpenAI|Google|Microsoft|Apple|Meta|Amazon)\b")),
    ("Location", re.compile(r"\b(United States|China|France|Paris|London|Beijing|Shanghai)\b")),
    ("Time", re.compile(r"\b(19|20)\d{2}\b")),
]

EVENT_TRIGGERS = {
    "published": "Publication",
    "released": "Release",
    "met": "Meeting",
    "acquired": "Acquisition",
    "announced": "Announcement",
}


def sent_split(text: str):
    parts = re.split(r"(?<=[.!?。！？])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def make_entity(entity_id, mention, etype, sentence):
    return {
        "id": entity_id,
        "mention": mention,
        "canonical_name": mention,
        "type": etype,
        "evidence": sentence,
        "confidence": 0.6,
        "metadata": {},
    }


def extract_entities(sentences):
    entities = []
    seen = {}
    next_id = 1
    for sent in sentences:
        for etype, pattern in ENTITY_PATTERNS:
            for m in pattern.finditer(sent):
                mention = m.group(0)
                key = (mention, etype)
                if key not in seen:
                    ent_id = f"ent_{next_id:03d}"
                    next_id += 1
                    seen[key] = ent_id
                    entities.append(make_entity(ent_id, mention, etype, sent))
    return entities, seen


def extract_relations(sentences, entities, seen):
    relations = []
    name_to_id = {e["canonical_name"]: e["id"] for e in entities}
    org_names = [e["canonical_name"] for e in entities if e["type"] == "Organization"]
    for sent in sentences:
        if "works for" in sent:
            parts = re.split(r"\bworks for\b", sent, maxsplit=1)
            left = parts[0].strip().split()[-1] if parts[0].strip().split() else None
            right = parts[1].strip().split()[0] if parts[1].strip().split() else None
            if left in name_to_id and right in name_to_id:
                relations.append({
                    "subject": name_to_id[left],
                    "predicate": "works_for",
                    "object": name_to_id[right],
                    "evidence": sent,
                    "confidence": 0.55,
                    "metadata": {},
                })
        pub_match = re.search(r"\b([A-Z][A-Za-z0-9\-]+(?:\s+[A-Z0-9][A-Za-z0-9\-]+)*)\s+(published|released|announced|acquired)\s+([A-Z][A-Za-z0-9\-]+(?:\s+[A-Z0-9][A-Za-z0-9\-]+)*)", sent)
        if pub_match:
            subj = pub_match.group(1).strip()
            pred = pub_match.group(2).strip().lower()
            obj = pub_match.group(3).strip()
            if subj in name_to_id:
                obj_id = name_to_id.get(obj)
                if not obj_id:
                    obj_id = f"ent_auto_{len(name_to_id)+1:03d}"
                    name_to_id[obj] = obj_id
                    entities.append(make_entity(obj_id, obj, "Document", sent))
                relations.append({
                    "subject": name_to_id[subj],
                    "predicate": pred if pred != "announced" else "published",
                    "object": obj_id,
                    "evidence": sent,
                    "confidence": 0.65,
                    "metadata": {},
                })
    return relations


def extract_events(sentences, entities):
    events = []
    next_id = 1
    for sent in sentences:
        for trigger, etype in EVENT_TRIGGERS.items():
            if re.search(rf"\b{re.escape(trigger)}\b", sent, flags=re.IGNORECASE):
                time_match = re.search(r"\b(19|20)\d{2}\b", sent)
                events.append({
                    "id": f"ev_{next_id:03d}",
                    "type": etype,
                    "trigger": trigger,
                    "participants": {},
                    "time": time_match.group(0) if time_match else None,
                    "location": None,
                    "evidence": sent,
                    "confidence": 0.55,
                    "metadata": {},
                })
                next_id += 1
                break
    return events


def extract_attributes(sentences, entities):
    attributes = []
    name_to_id = {e["canonical_name"]: e["id"] for e in entities}
    for sent in sentences:
        m = re.search(r"\b([A-Z][A-Za-z0-9\-]+) is ([^.]+)", sent)
        if m and m.group(1) in name_to_id:
            attributes.append({
                "entity_id": name_to_id[m.group(1)],
                "attribute": "description",
                "value": m.group(2).strip(),
                "evidence": sent,
                "confidence": 0.5,
                "metadata": {},
            })
    return attributes


def to_output(entities, relations, attributes, events):
    triples = []
    id_to_name = {e["id"]: e["canonical_name"] for e in entities}
    for rel in relations:
        triples.append({
            "subject": id_to_name.get(rel["subject"], rel["subject"]),
            "predicate": rel["predicate"],
            "object": id_to_name.get(rel["object"], rel["object"]),
            "evidence": rel["evidence"],
            "confidence": rel["confidence"],
        })
    for attr in attributes:
        triples.append({
            "subject": id_to_name.get(attr["entity_id"], attr["entity_id"]),
            "predicate": attr["attribute"],
            "object": attr["value"],
            "evidence": attr["evidence"],
            "confidence": attr["confidence"],
        })
    return {
        "triples": triples,
        "entities": entities,
        "attributes": attributes,
        "events": events,
        "ambiguities": [],
    }


def main():
    parser = argparse.ArgumentParser(description="Semi-automatic information extraction scaffold")
    parser.add_argument("--text", help="Input text")
    parser.add_argument("--stdin", action="store_true", help="Read input text from stdin")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    if args.stdin:
        text = sys.stdin.read()
    else:
        text = args.text or ""

    if not text.strip():
        raise SystemExit("No input text provided")

    sentences = sent_split(text)
    entities, seen = extract_entities(sentences)
    relations = extract_relations(sentences, entities, seen)
    attributes = extract_attributes(sentences, entities)
    events = extract_events(sentences, entities)
    output = to_output(entities, relations, attributes, events)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(str(out_path))


if __name__ == "__main__":
    main()
