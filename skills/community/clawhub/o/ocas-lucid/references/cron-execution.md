# Cron Execution — Lucid Dream Cycle

How to run the dream cycle in cron context.

## The Pattern

```python
# 1. Write the dream cycle script to /tmp/
write_file(path="/tmp/lucid_dream.py", content=<script>)

# 2. Execute via terminal
terminal(command="python3 /tmp/lucid_dream.py", timeout=120)
```

**Never use `execute_code`** — it is blocked in cron mode.

## Script Structure

The script should:
1. Read config from `~/.hermes/commons/data/ocas-lucid/config.json`
2. Scan `~/.hermes/commons/journals/` for unprocessed journals
3. Separate scan/sweep files from interesting files
4. Process interesting files first (up to cap of 40)
5. Classify each journal by relevance score
6. Write decisions to `decisions.jsonl`
7. Write ingestion log entries to `ingestion_log.jsonl`
8. Write recirculation entries to `recirculation_queue.jsonl`
9. Write evidence record to `evidence.jsonl`
10. Write dream journal to `journals/ocas-lucid/YYYY-MM-DD/{run_id}.json`
11. Update config with new cursor and stats

## Two-Pass Classification

**Pass 1 — Interesting journals** (non-scan filenames):
- Process all non-scan journals up to the 40-journal cap
- These are the high-value targets: mentor, praxis reviews, dispatch, vesper, taste

**Pass 2 — Scan journals** (if cap remains):
- Process scan/sweep journals only after all interesting journals are done
- Most will score as skips — this is expected

## Scan Classification Rules (CRITICAL)

The scan classification MUST use skill-level exceptions. A simple filename pattern match will misclassify high-value journals:

```python
SCAN_PATTERNS = ['-scan-', '_scan_', '-scan.', '_scan.', '-sweep-', '_sweep_', 
                 '-sweep.', '_sweep.', 'watch-sweep', 'deep-scan-', 'light-scan',
                 'daily-', '_daily_', 'weekly-', '_weekly_', 'journal-scan',
                 'forge-journal-scan', 'forge_journal_', 'update_check_', 
                 'conflict-scan', 'ingest-cron']

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
    for p in SCAN_PATTERNS:
        if p in name:
            return True
    return False
```

**Why this matters**: `mentor-light-*` files are high-value mentor evaluations. `ocas-custodian/light-*` files contain real lesson/blocker content (scores 6-7). Without exceptions, these get auto-skipped as scans.

## Priority Sorting (MANDATORY)

After separating interesting from scan, sort interesting journals by priority BEFORE capping:

```python
SKILL_PRIORITY = {
    'ocas-mentor': 0, 'ocas-vesper': 1, 'ocas-praxis': 2, 'ocas-taste': 3,
    'ocas-dispatch': 4, 'ocas-spot': 5, 'ocas-forge': 6, 'ocas-custodian': 7,
}
# Sort by (is_scan, skill_priority, filename)
files.sort(key=lambda f: (0 if not is_scan(f) else 1, 
                          SKILL_PRIORITY.get(f.split('/')[4], 50), 
                          f.split('/')[-1]))
```

Without this, alphabetical ordering puts dispatch/forge/praxis-ingest before mentor/vesper, and the 40-journal cap cuts off all high-signal journals.

## Config Path Resolution (CRITICAL — Multi-Config Ambiguity)

There are typically **multiple** `config.json` files for ocas-lucid on the filesystem:

| Path | Status |
|------|--------|
| `<hermes-home>/commons/data/ocas-lucid/config.json` | Active cron data dir (write target) |
| `<hermes-home>/profiles/indigo/commons/data/ocas-lucid/config.json` | Profile-specific config (may be authoritative) |
| `<commons>/data/ocas-lucid/config.json` | Stale copy — DO NOT WRITE TO THIS |
| `<repo-root>/commons/data/ocas-lucid/config.json` | Repo copy — stale |

**Rule**: Before writing the dream cycle script, identify the active config. Check which one has the highest `streak` value — that's the config the cron job has been incrementing, and the one your script must read/write.

**Safe approach**: 
1. Check candidate paths for existence and compare `streak` values
2. Use the path with the highest `streak` as the active config
3. After writing, re-read the same path to confirm cursor/stats updated correctly

**Never** hardcode `<hermes-home>/commons/` or `<commons>/` without verification — you will write to the stale copy and think the run succeeded while the cron job continues from the old cursor.

## Path Expansion Pitfall (CRITICAL)

When reading `config.json` fields like `source_journals_path` or `lucid_journals_path`, the values often contain `~` (e.g., `~/.hermes/commons/journals`). These do NOT auto-expand in Python's `open()`, `os.path.exists()`, or `os.makedirs()`.

**Bug**: `open(config['source_journals_path'])` → `FileNotFoundError: [Errno 2] No such file or found: '<hermes-home>/profiles/indigo/home/.hermes/commons/journals'`

The `~` is treated as a literal directory component rather than expanding to `/root`.

**Fix**: Always call `os.path.expanduser()` on every path read from config:
```python
JOURNALS_DIR_PATH = os.path.expanduser(config.get('source_journals_path', '<hermes-home>/commons/journals'))
```

Even fallback defaults should use absolute paths or be expanded. This applies to ALL config-path fields: `ingestion_log_path`, `decisions_path`, `journals_path`, `source_journals_path`, `lucid_journals_path`.

## Degraded Mode

When MemPalace MCP is unavailable:
- Skip `mempalace_add_drawer`, `mempalace_kg_add`, `mempalace_check_duplicate` calls
- Log `degraded: mempalace` in evidence record
- Set `mempalace_filed: false` and `mempalace_error` in decision records
- Continue with all other writes (decisions, ingestion log, dream journal)
- The run is still valuable — classification and routing decisions are persisted

### SQLite Direct-Access Fallback (when MCP tools unavailable)

When MemPalace MCP tools are not registered (common in cron/CLI environments), the KG and ChromaDB are accessible directly via SQLite:

| Database | Path | Tables |
|----------|------|--------|
| Knowledge Graph | `<fs-root>/.mempalace/palace/knowledge_graph.sqlite3` | `entities`, `triples` |
| ChromaDB | `<fs-root>/.mempalace/palace/chroma.sqlite3` | `collections`, `embeddings`, etc. |

**Entity schema**: `(id TEXT PK, name TEXT, type TEXT, properties TEXT, created_at TEXT)`
**Triple schema**: `(id TEXT PK, subject TEXT, predicate TEXT, object TEXT, valid_from TEXT, valid_to TEXT, confidence REAL, source_closet TEXT, source_file TEXT, extracted_at TEXT)`

Minimal filing example:
```python
import sqlite3, uuid, json

def file_to_kg(entities, rel_path, skill, room):
    conn = sqlite3.connect("<fs-root>/.mempalace/palace/knowledge_graph.sqlite3")
    c = conn.cursor()
    for ent in entities:
        eid = ent["name"].lower().replace(" ", "_")[:40]
        c.execute("INSERT OR IGNORE INTO entities (id, name, type, properties) VALUES (?, ?, ?, ?)",
                  (eid, ent["name"], ent["type"], json.dumps({"source": rel_path})))
        c.execute("INSERT INTO triples (id, subject, predicate, object, source_closet, source_file) VALUES (?, ?, ?, ?, ?, ?)",
                  (str(uuid.uuid4()), ent["name"], "is_a", ent["type"], room, rel_path))
    conn.commit()
    conn.close()
```

**Note**: ChromaDB filing requires embedding computation — use the `mempalace_drawers` collection ID. The KG is the primary filing target; ChromaDB drawer insertion is best-effort and can be deferred.

## Decision Record Schema (enriched)

Each decision record should include these debug-friendly fields:

```python
d = {
    "timestamp": timestamp, "run_id": run_id, "filepath": str(fp),
    "relative_path": rel, "score": score, "classification": cls,
    "reasoning": "; ".join(signals) if signals else "no signals",
    "signals": signals, "mempalace_filed": False, "mempalace_error": None,
    "skill": skill, "wing": wing, "room": room,
    "entity_count": len(entities),      # NEW: helps diagnose scoring
    "narrative_len": len(narrative),    # NEW: catches extraction gaps
}
```

`narrative_len=0` for a journal that clearly has content (e.g., vesper briefings) is a signal that the narrative extraction is missing nested fields.

The script should:
1. Read the ingestion log to find all previously processed filepaths
2. Skip any filepaths already in the log
3. Process the next unprocessed batch (up to cap)
4. Update cursor to the last processed file

**Important**: The cursor tracks position in the *prioritized* ordering (interesting first), not alphabetical order.

## PosixPath JSON Serialization Pitfall

When writing evidence records or any JSON output, `pathlib.Path` (PosixPath) objects are **not** JSON-serializable. The `cursor_after` field and any filepath stored in evidence/dream journal dicts must be explicitly cast to `str()`:

```python
# WRONG — raises TypeError: Object of type PosixPath is not JSON serializable
evidence["cursor_after"] = batch[-1].relative_to(SOURCE_JOURNALS_PATH)

# CORRECT
evidence["cursor_after"] = str(batch[-1].relative_to(SOURCE_JOURNALS_PATH))
```

This applies to ALL dict values that might be Path objects — evidence, dream journal, ingestion log entries, and decision records.

## Elephas Pipeline Interaction

When invoked as `elephas.ingest.journals then elephas.consolidate.immediate`, the expected flow is:

1. **Lucid dream cycle** runs first — scans all OCAS journals, classifies, writes dream journal
2. **Elephas cron pipeline** runs second — scans the same journal directories for entity extraction, writes to Chronicle

The two pipelines are independent but operate on the same input data. Key observations:
- Elephas's `elephas_cron_pipeline.py` uses LadybugDB (`lb.configure("chronicle")`) — requires the LadybugDB service running on port 9192
- Elephas writes its run journals to `<hermes-home>/commons/journals/ocas-elephas/YYYY-MM-DD/` — these are excluded from Lucid's scan path
- JSON parse errors in source journals (especially `mentor-light-*` files) cause silent skips in elephas — see `references/elephas-pipeline-json-errors.md`
- The elephas pipeline's DEBUG stdout output is expected and harmless in cron context