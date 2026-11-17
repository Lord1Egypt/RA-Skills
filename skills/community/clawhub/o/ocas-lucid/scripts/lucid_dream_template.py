#!/usr/bin/env python3
"""
Lucid Dream Cycle - Nightly Journal Curator (Production Template)
============================================================
This script implements the full dream cycle for the ocas-lucid skill.
It is designed to be written to /tmp/ and executed via terminal() in cron mode.

Usage: python3 /tmp/lucid_dream.py

Key design decisions encoded here:
1. Scan classification uses SKILL-LEVEL EXCEPTIONS (not just filename patterns)
2. Priority sorting ensures high-signal journals are processed before the 40-cap
3. MemPalace MCP calls are wrapped in try/except degraded mode
4. All records are written even in degraded mode (classification still valuable)
5. entities_observed type guard (can be int instead of list)
6. File discovery handles both date subdirs and skill-root-level files
7. Multi-batch support (process 200+ journals per run to clear scan backlogs)
"""
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

# === PATHS (pathlib) ===
DATA_DIR = Path(os.path.expanduser("~/.hermes/commons/data/ocas-lucid"))
JOURNALS_DIR = Path(os.path.expanduser("~/.hermes/commons/journals"))
LUCID_JOURNALS_DIR = Path(os.path.expanduser("~/.hermes/commons/journals/ocas-lucid"))
CONFIG_PATH = DATA_DIR / "config.json"
INGESTION_LOG_PATH = DATA_DIR / "ingestion_log.jsonl"
DECISIONS_PATH = DATA_DIR / "decisions.jsonl"
RECIRCULATION_PATH = DATA_DIR / "recirculation_queue.jsonl"
EVIDENCE_PATH = DATA_DIR / "evidence.jsonl"

# === SCAN CLASSIFICATION (with skill-level exceptions) ===
SCAN_PATTERNS = [
    '-scan-', '_scan_', '-scan.', '_scan.',
    '-sweep-', '_sweep_', '-sweep.', '_sweep.',
    'watch-sweep', 'deep-scan-', 'light-scan',
    'daily-', '_daily_', 'weekly-', '_weekly_',
    'journal-scan', 'forge-journal-scan', 'forge_journal_',
    'update_check_', 'conflict-scan', 'ingest-cron',
]

def is_scan(fp):
    name = fp.split('/')[-1].lower()
    # Skill-level exceptions — NEVER classify these as scans
    if 'mentor-light' in name or 'mentor-light-caller' in name:
        return False
    if '/ocas-vesper/' in fp or '/ocas-taste/' in fp:
        return False
    if 'praxis-review' in name or 'praxis-debrief' in name or 'praxis-update' in name:
        return False
    if 'dispatch-triage' in name or 'dispatch-draft' in name:
        return False
    # ocas-custodian/light-* and /deep-* files are NOT pure scans
    if '/ocas-custodian/' in fp and ('/light-' in fp or '/deep-' in fp):
        return False
    # ocas-spot/spot-* without sweep/watch are interesting
    if '/ocas-spot/' in fp:
        fname = fp.split('/')[-1].lower()
        if 'sweep' not in fname and 'watch' not in fname:
            return False
    for p in SCAN_PATTERNS:
        if p in name:
            return True
    return False

# === PRIORITY SORTING ===
SKILL_PRIORITY = {
    'ocas-mentor': 0, 'ocas-vesper': 1, 'ocas-praxis': 2, 'ocas-taste': 3,
    'ocas-dispatch': 4, 'ocas-spot': 5, 'ocas-forge': 6, 'ocas-custodian': 7,
    'ocas-elephas': 8, 'ocas-finch': 9, 'ocas-bones': 10, 'ocas-sands': 11,
    'dispatch': 50,
}

def priority_key(fp):
    """Sort key: interesting (non-scan) first, then by skill priority, then alphabetical."""
    fp_str = str(fp)
    parts = fp_str.split('/')
    try:
        skill_idx = parts.index('journals') + 1
        skill = parts[skill_idx] if skill_idx < len(parts) else ""
    except (ValueError, IndexError):
        skill = ""
    scan = is_scan(fp_str)
    return (1 if scan else 0, SKILL_PRIORITY.get(skill, 50), parts[-1])

# === NARRATIVE EXTRACTION ===
def extract_narrative(journal, filepath):
    parts = []
    NARRATIVE_FIELDS = ["summary", "description", "reasoning_summary",
                        "findings", "analysis", "report", "notes", "text", "content"]
    for field in NARRATIVE_FIELDS:
        val = journal.get(field)
        if isinstance(val, str) and len(val) > 10:
            parts.append(val)
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    for k in ["diagnosis", "summary", "description", "notes", "text"]:
                        v = item.get(k)
                        if isinstance(v, str) and len(v) > 10:
                            parts.append(v)
    # Vesper: nested decision.reasoning_summary
    decision = journal.get("decision", {})
    if isinstance(decision, dict):
        rs = decision.get("reasoning_summary", "")
        if rs and isinstance(rs, str) and len(rs) > 10:
            parts.append(rs)
    # Dispatch: content.decision.reasoning_summary
    content = journal.get("content", {})
    if isinstance(content, dict):
        d = content.get("decision", {})
        if isinstance(d, dict):
            rs = d.get("reasoning_summary", "")
            if rs and isinstance(rs, str) and len(rs) > 10:
                parts.append(rs)
    return " ".join(parts)[:3000]

def extract_entities(journal, filepath):
    entities = []
    # GUARD: entities_observed can be an int (count) instead of a list
    eo_list = journal.get("entities_observed", [])
    if not isinstance(eo_list, list):
        eo_list = []
    for eo in eo_list:
        if isinstance(eo, str):
            entities.append({"name": eo, "type": "unknown"})
        elif isinstance(eo, dict):
            name = eo.get("name", eo.get("label", ""))
            if name:
                entities.append({"name": name, "type": eo.get("type", "unknown")})
    # Vesper nested entities
    decision = journal.get("decision", {})
    if isinstance(decision, dict):
        payload = decision.get("payload", {})
        if isinstance(payload, dict):
            for eo in payload.get("entities_observed", []):
                if isinstance(eo, dict):
                    name = eo.get("name", eo.get("label", ""))
                    if name:
                        entities.append({"name": name, "type": eo.get("type", "unknown")})
    return entities

# === SCORING ===
def score_journal(journal, narrative, filepath):
    score = 0
    signals = []
    entities = extract_entities(journal, filepath)
    has_entities = len(entities) > 0

    # Pure metrics early exit
    if len(narrative) < 300 and not has_entities:
        return -3, ["pure_metrics(-3)"], entities

    lower = narrative.lower()

    if any(kw in lower for kw in ["learned", "correction", "mistake", "improvement",
            "should have", "could have", "better approach", "next time", "avoid",
            "fix", "resolved", "solution", "workaround"]):
        score += 4; signals.append("correction_or_lesson(+4)")

    if any(kw in lower for kw in ["decided", "decision", "chose", "selected",
            "determined", "conclusion", "recommend", "adopt", "approved", "rejected",
            "prefer", "opt for", "go with"]):
        score += 3; signals.append("decision_keywords(+3)")

    if has_entities:
        score += 2; signals.append("entity_density(+2)")

    if any(kw in lower for kw in ["blocked", "blocker", "error", "failed", "failure",
            "issue", "problem", "unavailable", "exhaustion", "limit", "rate limit",
            "429", "timeout", "crash"]) and len(narrative) > 200:
        score += 2; signals.append("blocker_context(+2)")

    if any(kw in lower for kw in ["cross-skill", "integration", "coordinated",
            "multiple skill", "skill cooperation", "inter-skill", "between skills"]):
        score += 2; signals.append("cross_skill(+2)")

    if any(kw in lower for kw in ["local_adaptation", "adapted", "customized",
            "modified", "preserved", "conflict_resolution", "merge conflict"]):
        score += 2; signals.append("adaptations(+2)")

    jtype = journal.get("journal_type", journal.get("type", ""))
    if jtype in ["Action", "Interaction", "action"]:
        score += 3; signals.append("user_directed(+3)")

    if len(narrative) > 500:
        score += 1; signals.append("artifacts(+1)")

    return score, signals, entities

def classify(score):
    if score >= 5: return "file"
    if score >= 3: return "recirculate"
    return "skip"

# === WING ASSIGNMENT ===
def get_wing_room(skill):
    mapping = {
        'ocas-custodian': ('system', 'operations'),
        'ocas-mentor': ('evolution', 'evolution'),
        'ocas-finch': ('evolution', 'evolution'),
        'ocas-forge': ('evolution', 'evolution'),
        'ocas-praxis': ('evolution', 'evolution'),
        'ocas-dispatch': ('operations', 'operations'),
        'ocas-spot': ('operations', 'operations'),
        'ocas-vesper': ('operations', 'operations'),
        'ocas-taste': ('preferences', 'preferences'),
        'ocas-elephas': ('knowledge', 'knowledge'),
        'ocas-bones': ('operations', 'operations'),
        'ocas-sands': ('preferences', 'preferences'),
    }
    return mapping.get(skill, ('root', 'operations'))

# === FILE DISCOVERY ===
def gather_unprocessed(processed):
    """Gather all unprocessed journal files, handling both date subdirs and root-level files."""
    all_files = []
    for skill_dir in sorted(JOURNALS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        if skill_dir.name == "ocas-lucid":
            continue
        for date_dir in sorted(skill_dir.iterdir()):
            if not date_dir.is_dir():
                # Handle files directly in skill dir (e.g., ocas-custodian/esc-run-*)
                if date_dir.suffix == ".json" and date_dir.name != "task-list.json":
                    fp_str = str(date_dir)
                    if fp_str not in processed and "ocas-lucid" not in fp_str:
                        all_files.append(date_dir)
                continue
            for f in sorted(date_dir.glob("*.json")):
                if f.name == "task-list.json":
                    continue
                fp_str = str(f)
                if fp_str not in processed and "ocas-lucid" not in fp_str:
                    all_files.append(f)
    return all_files

# === MEMPALACE FILING (SQLite fallback) ===
def file_to_kg(entities, rel_path, skill, room, narrative_summary):
    """File entities to MemPalace KG via SQLite direct access."""
    try:
        import sqlite3
        conn = sqlite3.connect("<mempalace>/palace/knowledge_graph.sqlite3")
        c = conn.cursor()
        filed = []
        for ent in entities:
            eid = ent["name"].lower().replace(" ", "_")[:40]
            c.execute("INSERT OR IGNORE INTO entities (id, name, type, properties) VALUES (?, ?, ?, ?)",
                      (eid, ent["name"], ent["type"], json.dumps({"source": rel_path, "skill": skill})))
            tid = str(uuid.uuid4())
            c.execute("INSERT OR IGNORE INTO triples (id, subject, predicate, object, source_closet, source_file) VALUES (?, ?, ?, ?, ?, ?)",
                      (tid, ent["name"], "is_a", ent["type"], room, rel_path))
            filed.append(ent["name"])
        # Add journal entity
        jid = rel_path.replace("/", "_").replace(".", "_")[:50]
        c.execute("INSERT OR IGNORE INTO entities (id, name, type, properties) VALUES (?, ?, ?, ?)",
                  (jid, f"journal:{rel_path}", "Document",
                   json.dumps({"skill": skill, "summary": narrative_summary[:200]})))
        c.execute("INSERT OR IGNORE INTO triples (id, subject, predicate, object, source_closet, source_file) VALUES (?, ?, ?, ?, ?, ?)",
                  (str(uuid.uuid4()), f"journal:{rel_path}", "produced_by", skill, room, rel_path))
        conn.commit()
        conn.close()
        return filed
    except Exception as e:
        return [f"ERROR: {e}"]

def main():
    run_id = f"dream-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}Z"
    timestamp = datetime.now(timezone.utc).isoformat()
    os.makedirs(LUCID_JOURNALS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR / "staging", exist_ok=True)

    # Read config & processed
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    processed = set()
    if INGESTION_LOG_PATH.exists():
        for line in INGESTION_LOG_PATH.read_text().strip().split("\n"):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                processed.add(entry.get("file") or entry.get("filepath") or entry.get("journal_file", ""))
            except json.JSONDecodeError:
                pass

    # Gather & sort
    all_files = gather_unprocessed(processed)
    total_available = len(all_files)
    all_files.sort(key=priority_key)

    # Process up to 200 journals per run (5 batches of 40) to clear scan backlogs
    BATCH_SIZE = 200
    to_process = all_files[:BATCH_SIZE]

    # Classify
    results = []
    for fp in to_process:
        try:
            with open(fp) as f:
                journal = json.load(f)
        except Exception as e:
            results.append((fp, None, -3, [f"read_error: {e}"], "skip", [], 0))
            continue
        narrative = extract_narrative(journal, str(fp))
        score, signals, entities = score_journal(journal, narrative, str(fp))
        cls = classify(score)
        results.append((fp, journal, score, signals, cls, entities, len(narrative)))

    # Write records
    decisions, ingestions, recircs = [], [], []
    filed = skipped = recirculated = 0
    file_details = []

    for fp, journal, score, signals, cls, entities, narrative_len in results:
        rel = str(fp).replace(str(JOURNALS_DIR) + "/", "")
        parts = str(fp).split('/')
        try:
            skill_idx = parts.index('journals') + 1
            skill = parts[skill_idx] if skill_idx < len(parts) else "unknown"
        except (ValueError, IndexError):
            skill = "unknown"

        d = {
            "timestamp": timestamp, "run_id": run_id, "filepath": str(fp),
            "relative_path": rel, "score": score, "classification": cls,
            "reasoning": "; ".join(signals) if signals else "no signals",
            "signals": signals, "mempalace_filed": False, "mempalace_error": None,
            "skill": skill, "entity_count": len(entities),
            "narrative_len": narrative_len
        }
        ing = {"run_id": run_id, "file": str(fp), "processed_at": timestamp,
               "classification": cls, "score": score}

        if cls == "file":
            filed += 1
            wing, room = get_wing_room(skill)
            d["wing"] = wing
            d["room"] = room
            d["mempalace_error"] = "pending_mcp"
            file_details.append({
                "path": rel, "score": score, "signals": signals,
                "skill": skill, "wing": wing, "room": room,
                "entities": entities, "narrative_len": narrative_len
            })
        elif cls == "recirculate":
            recirculated += 1
            recircs.append({
                "filepath": str(fp), "relative_path": rel, "score": score,
                "reasoning": "; ".join(signals), "re_evaluations": 0,
                "first_seen": timestamp, "last_evaluated": timestamp,
                "skill": skill
            })
        else:
            skipped += 1

        decisions.append(d)
        ingestions.append(ing)  # FIXED: was 'ig' (typo)

    # Append to data files
    with open(DECISIONS_PATH, 'a') as f:
        for d in decisions:
            f.write(json.dumps(d) + "\n")
    with open(INGESTION_LOG_PATH, 'a') as f:
        for ig in ingestions:
            f.write(json.dumps(ig) + "\n")
    with open(RECIRCULATION_PATH, 'a') as f:
        for r in recircs:
            f.write(json.dumps(r) + "\n")

    # File to MemPalace KG (SQLite fallback when MCP unavailable)
    mempalace_filed_count = 0
    for fd in file_details:
        wing, room = fd["wing"], fd["room"]
        summary = fd["signals"]
        filed_entities = file_to_kg(fd["entities"], fd["path"], fd["skill"], room, str(summary))
        if filed_entities and not any(str(e).startswith("ERROR") for e in filed_entities):
            mempalace_filed_count += 1
            # Update the decision record
            for d in decisions:
                if d["filepath"] == str(Path(JOURNALS_DIR) / fd["path"]):
                    d["mempalace_filed"] = True
                    d["mempalace_error"] = None

    # Evidence
    evidence = {
        "timestamp": timestamp, "run_id": run_id, "dream_cycle": True,
        "mode": "cron", "journals_scanned": len(results),
        "total_journals": total_available, "file_count": filed,
        "recirculate_count": recirculated, "skip_count": skipped,
        "filed_count": mempalace_filed_count,
        "not_activity_reason": None
    }
    with open(EVIDENCE_PATH, 'a') as f:
        f.write(json.dumps(evidence) + "\n")

    # Dream journal
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    run_dir = LUCID_JOURNALS_DIR / today
    os.makedirs(run_dir, exist_ok=True)

    dream = {
        "journal_spec_version": "1.3", "run_id": run_id, "timestamp": timestamp,
        "type": "Action",
        "summary": f"Dream {run_id}: {len(results)} journals from {total_available} available",
        "scan_count": len(results), "file_count": filed,
        "recirculate_count": recirculated, "skip_count": skipped,
        "total_journals": total_available, "file_details": file_details,
        "recirculate_details": [], "skip_details": [],
        "re_emergence_events": [], "signal_emissions": [],
        "not_activity_reason": None
    }
    with open(run_dir / f"{run_id}.json", 'w') as f:
        json.dump(dream, f, indent=2)

    # Update config
    if results:
        last = results[-1][0]
        config["cursor"] = str(last)
        try:
            config["cursor_file"] = str(last.relative_to(JOURNALS_DIR))
        except ValueError:
            config["cursor_file"] = str(last)
    config["last_run"] = timestamp
    config["last_run_status"] = "complete"
    config["streak"] = config.get("streak", 0) + 1
    config["total_filed"] = config.get("total_filed", 0) + filed
    config["total_skipped"] = config.get("total_skipped", 0) + skipped
    config["total_recirculated"] = config.get("total_recirculated", 0) + recirculated

    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"Dream {run_id}: {len(results)} processed ({filed} file, {recirculated} recirc, {skipped} skip) from {total_available} available")
    print(f"Cursor: {config.get('cursor_file', 'N/A')}")
    print(f"Streak: {config['streak']}")
    if file_details:
        print(f"\nFiled journals:")
        for fd in file_details:
            print(f"  [{fd['score']}] {fd['path']} -> {fd['wing']}/{fd['room']}")

if __name__ == "__main__":
    main()