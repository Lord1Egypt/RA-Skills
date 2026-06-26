# compaction.md — Compaction Strategy + Thresholds + Aggressive Mode

> Complete strategy reference for memory compaction. Source: `scripts/memory_compact.py`

---

## Trigger Conditions

- `memory_md_kb > 15` (defined in SKILL.md) or `max_memory_kb` parameter
- Default `max_memory_kb = 5` (script CLI default, more aggressive)
- cron `run_batch` with `skip_compact=true` → no auto-compaction, requires manual trigger

---

## Compaction Flow (5 Steps)

### 1. Size Report
- MEMORY.md byte count + character count + token estimate
- Token estimate: CJK × 1.3 + ASCII word × 0.75

### 2. Section Token Analysis
- Split MEMORY.md by `#{1,3}` headings
- Calculate token count per section independently
- **Bloat threshold**: single section > 500 tokens → mark ⚠️

```python
# section_token_analysis() return format
[{"heading": str, "lines": int, "tokens": int, "preview": str}]
```

### 3. Cross-File Redundancy Detection
- Compare MEMORY.md with all `memory/YYYY-MM-DD.md`
- Calculate similarity using Jaccard distance

| Similarity | Severity | Recommendation |
|------------|----------|----------------|
| Jaccard < 0.3 (sim > 0.7) | high | REMOVE — fully duplicated |
| Jaccard 0.3-0.5 (sim 0.5-0.7) | medium | COMPACT — keep only decisions/action items |

- Detection condition: `shared_tokens > 5 AND similarity > 0.5`
- Only checks daily notes at section level (not full text)

### 4. Internal Redundancy Detection
- Duplicate lines within MEMORY.md (exact match, case-insensitive)
- Filter condition: line length > 10 characters
- Deduplicated display (each duplicate line shown once)

### 5. Daily Notes Bloat Detection
- Single daily note > 8KB → mark ⚠️
- Exceeds `DAILY_NOTE_ROTATE_BYTES` (30KB) → auto-rotate

---

## Aggressive Mode (`aggressive=true`)

Differences from normal mode:

| Dimension | Normal Mode | Aggressive Mode |
|-----------|-------------|-----------------|
| MEMORY.md handling | Analyze only, no modifications | Dedup + compress consecutive blank lines |
| Daily Notes | Analyze only, no modifications | Auto-rotate files exceeding 30KB |
| auto marking | Only remove high-severity redundancy | Same + MEMORY.md compression |

### aggressive_compact_memory_text() Logic
1. Preserve all `## ` heading lines
2. Remove duplicate lines (exact match)
3. Merge consecutive blank lines into a single blank line
4. Preserve trailing newline at end of file

### rotate_oversized_daily_notes() Logic
1. Move original file to `memory/archive/YYYY-MM-DD.full.md`
2. Replace original with summary (first 10 lines preview + metadata)
3. Only executed when `auto=true`

---

## Auto Mode Execution Conditions

```python
if auto and issues:
    # Only process severity == "high" cross-file redundancy
    # Regex match: \n?###?\s*{heading}\n.*?(?=\n###?\s|\Z)
    # Atomic write (tempfile + os.replace)
```

---

## Return Structure

```python
{
    "memory_size": int,          # Current byte count
    "memory_tokens": int,        # Token estimate
    "cross_file_issues": list,   # Redundancy issue list
    "internal_duplicates": int,  # Internal duplicate line count
    "high_severity_count": int,  # High severity issue count
    "sections": list,            # Section analysis results
    "memory_size_before": int,   # Pre-compaction size
    "memory_size_after": int,    # Post-compaction size
    "rotated": bool,             # Whether any rotation occurred
    "rotated_count": int,        # Number of rotated files
}
```

---

## MCP Tool Mapping

```jsonc
memory_compact({
  "workspace": "auto",
  "dry_run": false,
  "aggressive": false,
  "max_memory_kb": 15
})
```

- `dry_run=true`: analyze only, no writes (default behavior)
- `auto` is implicitly enabled at MCP layer via `dry_run=false`
- `aggressive`: passed through directly at MCP layer
