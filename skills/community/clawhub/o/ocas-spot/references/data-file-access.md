# Spot — Data File Access

Spot stores all records as plain JSONL — one JSON object per line, no line-number prefix.

## Line-number prefix warning
The `read_file` Hermes tool prepends line numbers to displayed output (e.g., `1|{...}`, `2|{...}`). This is a display artifact — actual files on disk do NOT contain these prefixes.

- **To inspect file contents**: Use `terminal(command="head -5 /path/to/file.jsonl")` for raw content.
- **To parse in Python**: Read lines directly with `open().readlines()` and `json.loads(line)`.
- **To edit**: Read raw lines via terminal + Python, modify, write back.

## Append-only vs full-replace files

**Append-only** (never use `write_file` to write a single record):
- `metrics.jsonl` — sweep history, must accumulate

**Full-replace** (safe to `write_file` entire contents):
- `watch.jsonl` — rewrite all records each sweep
- `venues.jsonl` — rewrite when adding/repairing venues
- `bookings.jsonl` — rewrite when adding bookings
- `config.json` — single object

## File paths (verified 2026-06-08)

Spot data lives under the Hermes profile directory. The exact paths depend on profile:

**the agent profile (active):**
- Data: `<hermes-home>/profiles/indigo/commons/data/ocas-spot/`
- Journals: `<hermes-home>/commons/journals/ocas-spot/YYYY-MM-DD/`
- Config: `<hermes-home>/profiles/indigo/commons/data/ocas-spot/config.json`

**Default/non-profile:**
- Data: `<hermes-home>/commons/data/ocas-spot/`
- Journals: `<hermes-home>/commons/journals/ocas-spot/YYYY-MM-DD/`

**Key files:**
- `watch.jsonl` — WatchRecord entries (full-replace)
- `venues.jsonl` — VenueRecord entries (full-replace)
- `bookings.jsonl` — BookingRecord entries (full-replace)
- `metrics.jsonl` — Sweep history (append-only)
- `config.json` — Single JSON object

**Journal directory pattern:** Journals go to `<hermes-home>/commons/journals/ocas-spot/YYYY-MM-DD/{run_id}.json` (NOT under profiles/indigo/). The journal path is shared across profiles.

## Cron mode constraints
- `execute_code` is **blocked**. Use `terminal()` for shell commands and `write_file()` for file writes.
- `write_file()` may emit a "sibling subagent" warning in solo cron runs — this is a **false positive**. Ignore and verify.

## metrics.jsonl corruption: concatenated JSON and duplicates

The `metrics.jsonl` file is append-only and accumulates sweep records over time. Corruption can occur when:
- Two JSON objects are written without a newline between them (concatenated `}{`)
- The same sweep writes its entry twice (duplicate)

### Detection
Use `terminal(command="wc -l /path/to/metrics.jsonl")` to check line count, then attempt to parse each line:
```python
import json
with open(path, 'r') as f:
    content = f.read()

# Try to extract all JSON objects by tracking brace depth
records = []
depth = 0
start = None
for i, ch in enumerate(content):
    if ch == '{':
        if depth == 0:
            start = i
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0 and start is not None:
            try:
                records.append(json.loads(content[start:i+1]))
            except:
                pass
            start = None
```

If `len(records)` differs from `wc -l` count, corruption is present.

### Repair
After extracting valid JSON objects, deduplicate by `(timestamp, type)` key and rewrite:
```python
seen = set()
unique = []
for r in records:
    key = (r.get('timestamp'), r.get('type'))
    if key not in seen:
        seen.add(key)
        unique.append(r)

with open(path, 'w') as f:
    for r in unique:
        f.write(json.dumps(r) + '\n')
```

### Prevention
Always append metrics with `terminal(command="echo '{json}' >> /path/to/metrics.jsonl")` — never use `write_file()` for metrics. Verify the echo produced exactly one new line with `tail -1`.

## Line-number prefix on disk — corrupted files only

Under normal operation, Spot JSONL files on disk do **not** contain line-number prefixes. The `read_file` Hermes tool prepends `N|` to each line of its *display output* only — the actual file on disk remains clean JSONL.

**However**, if `read_file` output is accidentally written back to disk (e.g., via `write_file` or copy-paste), prefixes become embedded in the file itself. This has happened to `venues.jsonl` in the past. As of 2026-06-06, `watch.jsonl` was verified clean on disk (no prefixes) despite `read_file` displaying them.

### Detection: is the file actually prefixed?

Use `terminal(command="head -3 /path/to/file.jsonl")` to check raw disk contents:
- If the first character of line 1 is `{` → file is clean, no prefixes
- If the first characters are `1|` → file has been corrupted with prefixes

### Repair pattern (only if prefixes confirmed on disk)

```python
import json

def strip_prefixes(line_str):
    """Strip one or more line-number prefixes from a JSONL line."""
    while '|' in line_str:
        parts = line_str.split('|', 1)
        if parts[0].isdigit() and len(parts[1]) > 0 and parts[1][0] == '{':
            line_str = parts[1]
        else:
            break
    return line_str

with open('<hermes-home>/profiles/indigo/commons/data/ocas-spot/watch.jsonl', 'rb') as f:
    raw_lines = f.readlines()
records = []
for line in raw_lines:
    line = line.strip()
    if not line:
        continue
    line_str = line.decode('utf-8')
    line_str = strip_prefixes(line_str)
    if not line_str.startswith('{'):
        continue
    records.append(json.loads(line_str))
```

After repairing, write back clean JSONL (no prefixes) to prevent recurrence.

### Parsing workflow for cron mode

1. Read file with `open().readlines()` in Python via `terminal()`
2. If first line starts with `{` → parse directly with `json.loads(line)`
3. If first line starts with `N|` → apply `strip_prefixes` first
4. Write back with `json.dumps(record)` per line, no prefixes