#!/usr/bin/env python3
"""presidio-scrub.py -- Analyze text for PII, anonymize with reversible tokens, store mapping."""

import json, os, sys, time, urllib.request

ANALYZER_URL = os.environ.get("PRESIDIO_ANALYZER_URL", "http://localhost:5002")
MAPPING_DIR = os.environ.get("PRESIDIO_MAPPING_DIR", os.path.expanduser("~/.openclaw/presidio/mappings"))
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECOGNIZERS_FILE = os.path.join(SKILL_DIR, "configs", "recognizers.json")

def http_post(url, data):
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None

def check_health():
    a = http_post(f"{ANALYZER_URL}/analyze", {"text": "health", "language": "en"}) is not None
    b = http_post(os.environ.get("PRESIDIO_ANONYMIZER_URL", "http://localhost:5001") + "/anonymize",
        {"text": "h", "anonymizers": {"DEFAULT": {"type": "replace", "new_value": "x"}}, "analyzer_results": []}) is not None
    return a, b

def main():
    session_id = sys.argv[1] if len(sys.argv) > 1 else str(int(time.time()))
    if len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
    elif not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    else:
        print(json.dumps({"error": "No input text"})); sys.exit(1)

    # Health check
    a_ok, b_ok = check_health()
    if not a_ok or not b_ok:
        print(json.dumps({"error": "BLOCKED: Presidio is not healthy.", "analyzer": "up" if a_ok else "DOWN", "anonymizer": "up" if b_ok else "DOWN"}))
        sys.exit(1)

    # Load custom recognizers
    recognizers = []
    if os.path.exists(RECOGNIZERS_FILE):
        with open(RECOGNIZERS_FILE) as f:
            recognizers = json.load(f).get("ad_hoc_recognizers", [])

    # Analyze
    payload = {"text": text, "language": "en"}
    if recognizers:
        payload["ad_hoc_recognizers"] = recognizers
    entities = http_post(f"{ANALYZER_URL}/analyze", payload)
    if entities is None:
        print(json.dumps({"error": "Analyzer returned no response"})); sys.exit(1)
    if len(entities) == 0:
        print(json.dumps({"text": text, "pii_found": 0, "mapping_file": None, "session_id": session_id}, indent=2)); return

    # Remove overlapping entities (keep highest score, then longest match)
    entities_by_score = sorted(entities, key=lambda x: (-x.get("score", 0), -(x["end"] - x["start"])))
    filtered = []
    for ent in entities_by_score:
        overlap = False
        for kept in filtered:
            if ent["start"] < kept["end"] and ent["end"] > kept["start"]:
                overlap = True
                break
        if not overlap:
            filtered.append(ent)
    entities = filtered

    # Whitelist: exclude WhatsApp JIDs from PII detection
    WHATSAPP_SUFFIXES = ("@g.us", "@s.whatsapp.net", "@lid", "@broadcast")
    entities = [e for e in entities if not any(text[e["start"]:e["end"]].endswith(suffix) for suffix in WHATSAPP_SUFFIXES)]
    if len(entities) == 0:
        print(json.dumps({"text": text, "pii_found": 0, "mapping_file": None, "session_id": session_id}, indent=2)); return

    # Build tokens
    entities_fwd = sorted(entities, key=lambda x: x["start"])
    type_counters, token_map, reverse_map = {}, {}, {}
    for e in entities_fwd:
        original = text[e["start"]:e["end"]]
        if original in token_map:
            continue
        etype = e["entity_type"]
        type_counters[etype] = type_counters.get(etype, 0) + 1
        token = f"[{etype}_{type_counters[etype]}]"
        token_map[original] = token
        reverse_map[token] = original

    # Replace (reverse order)
    anonymized = text
    for e in sorted(entities, key=lambda x: x["start"], reverse=True):
        original = text[e["start"]:e["end"]]
        if original in token_map:
            anonymized = anonymized[:e["start"]] + token_map[original] + anonymized[e["end"]:]

    # Save mapping
    os.makedirs(MAPPING_DIR, exist_ok=True)
    mf = os.path.join(MAPPING_DIR, f"{session_id}.json")
    with open(mf, "w") as f:
        json.dump({"session_id": session_id, "created": int(time.time()), "reverse_map": reverse_map, "entity_count": len(entities_fwd), "entity_types": list(type_counters.keys())}, f, indent=2)
    os.chmod(mf, 0o600)

    print(json.dumps({"text": anonymized, "pii_found": len(entities_fwd), "entity_types": list(type_counters.keys()), "mapping_file": mf, "session_id": session_id}, indent=2))

if __name__ == "__main__":
    main()
