# Dispatch-Triggered Incremental Scan — 2026-06-27 (updated)

**Trigger:** Dispatcher fires `taste_new_data` with signal count changes. Runs as part of a multi-skill dispatch wave.

## Command Pattern

```bash
cd <hermes-home>/profiles/indigo/commons/data/ocas-taste && /usr/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py scan-incremental 24
```

Output: JSON with `signals_created`, `cancellations`, `services_scanned`, plus detailed `extractions` array.

**Confirmed working:** 2026-06-25 (six runs):
- First run: token repair (timezone suffix on both accounts) → 599 messages processed, 1 signal (Lavash/DoorDash).
- Second run (12h later): 2 signals (Next Level VG + Lavash, both DoorDash). Token repair still required (timezone suffix reappears).
- Third run (dispatch #63, 2026-06-25T02:45Z): token repair again (both accounts timezone suffix) → 2 signals (Next Level VG $76.66 + Lavash $64.60). Confirms timezone suffix reappears on every OAuth refresh — repair is mandatory, not one-time.
- Fourth run (multi-skill dispatch wave #71, ~04:24Z): token repair (both accounts timezone suffix again) → 2 signals (Next Level VG $76.66 + Lavash $64.60). **Combined repair + scan in single `terminal()` call succeeded** — chained with `&&` in one invocation to avoid OAuth refresh race condition.
- Fifth run (dispatch #73, 2026-06-25T05:13Z): token repair (both accounts timezone suffix — 6th+ consecutive scan requiring repair) → 2 signals (Next Level VG $76.66 + Lavash $64.60). All pipelines clean.
- Sixth run (dispatch #108, 2026-06-25T16:16Z): token repair (both accounts timezone suffix — 7th+ consecutive) → 1 signal (Next Level VG $76.66). Three-category dispatch (email + journals + taste). Email: 0 escalations. Journals: all clean. Taste: 1 signal.
- Seventh run (dispatch wave, 2026-06-27T17:15Z): token repair (both accounts timezone suffix — pattern holds 12+ days running) → 0 signals. Three-category dispatch (email + journals + taste). Email: all 5 threads informational/self-sent. Journals: pre-existing wave journal resolved. Taste: 0 new signals across 9 services.

## Integration with Dispatch

When the dispatcher fires a `taste_new_data` item:
1. **Pre-scan token repair** (REQUIRED) — run the combined repair script before every scan (see SKILL.md "Pre-scan token repair checklist"). Two failure modes: timezone suffix (`+00:00`/`Z`) and float expiry. Both hit simultaneously on 2026-06-25. Timezone suffix reappears on every refresh — always repair before scanning.
2. **Chain repair + scan in a SINGLE `terminal()` call** — see OAuth Race Condition pitfall below. Do NOT run repair as one call and scan as a separate call.
3. `cd <hermes-home>/profiles/indigo/commons/data/ocas-taste && /usr/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py scan-incremental 24`
4. Verify output `signals_created` count
5. Write Taste journal: `<hermes-home>/profiles/indigo/commons/journals/ocas-taste/YYYY-MM-DD/taste-scan-{ts}.json`
   - Journal structure: `{"run_id": "taste-scan-{ts}", "run_type": "dispatch_scan", "timestamp": "...", "profile": "indigo", "summary": "...", "metrics": {"signals_created": N, "cancellations": N, "services_scanned": [...], "extractions_processed": N}, "signals": [{"service": "...", "venue": "...", "total": "...", "type": "..."}]}`
6. **Taste runs independently** — Even if email and journal pipelines are second-wave re-detections or no-ops, still run the Taste scan. Signals are independent.
7. If 0 signals created and dispatch reported changes, log potential false positive in evidence

## Pitfall: OAuth Token Refresh Race Condition

**Symptom:** You run the token repair script in one `terminal()` call, then run the taste scan in a separate `terminal()` call. The scan fails with `"unconverted data remains: +00:00"` even though you just repaired the token.

**Root cause:** The `google_auth.py` helper (imported by `taste_scan.py`) triggers an OAuth token refresh on initialization. This refresh re-adds the `+00:00` timezone suffix to the `expiry` field — undoing your repair. If repair and scan are separate `terminal()` calls, the OAuth refresh happens between them.

**Concrete example (2026-06-25 dispatch #111):**
```
# Call 1: Repair succeeded
python3 -c "..." && echo "Repaired"  # → Repaired: <user-google-email>

# Call 2: Scan failed
cd ... && /usr/bin/python3 taste_scan.py scan-incremental 24
# → Error with <user-google-email>.json: unconverted data remains: +00:00
# → Initialized Gmail and Calendar with <agent-email>.json  (wrong account!)
# → 0 signals (the agent's account has no consumption emails)
```

**Fix:** Chain repair and scan in a SINGLE `terminal()` call with `&&`:
```bash
python3 -c "<repair script>" && cd <hermes-home>/profiles/indigo/commons/data/ocas-taste && /usr/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py scan-incremental 24
```

**Why this matters:** When the scan silently falls back to the agent's account (which has zero consumption emails), it reports 0 signals with no obvious error. You might think there's genuinely nothing new and skip the scan. The only way to detect the failure is to check which account the scan output says it initialized with — always verify `"Initialized Gmail and Calendar with <user-google-email>.json"` in the output.

## Post-Scan Dedup (REQUIRED After Every Dispatch Scan)

**Problem:** Multiple dispatch waves re-scanning the same 24h window create duplicate signals. The built-in `taste_signals_dedup.py` uses a strict key (exact signal_id or near-identical timestamps) and does NOT catch dispatch-wave duplicates which have different `signal_id` and `created_at` values but identical `(venue_name, event_date[:10], extraction_source)`.

**Confirmed 2026-06-25:** 36 duplicate "Next Level VG" signals accumulated from repeated dispatch waves. `taste_signals_dedup.py` found 0 duplicates (strict key missed them). Manual dedup with key `(venue_name, event_date[:10], extraction_source)` removed 74 duplicates (4777 → 4703).

**Dedup script (run after every dispatch-triggered scan):**
```bash
cd <hermes-home>/profiles/indigo/commons/data/ocas-taste && /usr/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/dispatch_taste_dedup.py
```

> ⚠️ **Do NOT run `dispatch_taste_dedup.py` here.** It keys on `event_date[:10]`, but Styx signals (from the daily Styx delta) carry `date`, not `event_date`. Every Styx signal collapses to key `(venue_name, None, 'styx')` and ALL-BUT-ONE per venue is deleted (confirmed live 2026-07-22: deleted 47 of 49; reaffirmed 2026-07-23 Styx coexists in `signals.jsonl`). `safe_taste_dedup.py` keys on `event_date or date` and refuses to write if the Styx count would drop.

**Path clarification:** `safe_taste_dedup.py` lives under `skills/ocas-taste/scripts/`. Always use the absolute path (a relative invocation from the data dir fails with `FileNotFoundError`).

Or inline (if the script isn't available) — note the Styx-safe key `(venue_name, date10, extraction_source)` where `date10 = (event_date or date)[:10]`:
```bash
cd <hermes-home>/profiles/indigo/commons/data/ocas-taste && python3 -c "
import json
signals = []
with open('signals.jsonl') as f:
    for line in f:
        if line.strip():
            signals.append(json.loads(line))
print(f'Before: {len(signals)} signals')
def date10(s):
    d = s.get('event_date') or s.get('date') or ''
    return d[:10] if d else ''
seen = set()
deduped = []
removed = 0
for s in signals:
    key = (s.get('venue_name',''), date10(s), s.get('extraction_source',''))
    if key in seen:
        removed += 1
        continue
    seen.add(key)
    deduped.append(s)
styx_before = sum(1 for s in signals if s.get('extraction_source')=='styx')
styx_after = sum(1 for s in deduped if s.get('extraction_source')=='styx')
print(f'Removed: {removed} duplicates')
print(f'After: {len(deduped)} signals  STYX: {styx_before} -> {styx_after}', 'OK' if styx_before==styx_after else 'CORRUPTED!')
assert styx_before == styx_after, 'Styx signals lost - abort'
shutil.copy('signals.jsonl', f'/tmp/signals.pre-dedup.{time.strftime(\"%Y%m%dT%H%M%SZ\")}.jsonl')
with open('signals.jsonl', 'w') as f:
    for s in deduped:
        f.write(json.dumps(s) + '\n')
"
```

**When to skip:** If `signals_created` is 0 AND the scan found no new extractions, dedup is unnecessary (but harmless to run).

## Key Details

- **Python runtime:** Must use `/usr/bin/python3` (system Python 3.14 with googleapiclient installed). NOT `<hermes-venv>/bin/python3.13` (path does not exist).
- **Script location:** `<hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py`
- **Data directory:** `<hermes-home>/profiles/indigo/commons/data/ocas-taste`
- Script handles its own auth and dedup (internal dedup only catches exact-match duplicates, not dispatch-wave re-scans)
- Output goes to stdout as JSON; new signals written to `signals.jsonl` automatically
- **Manual dedup required after every dispatch wave** — the built-in dedup is insufficient for multi-wave scenarios