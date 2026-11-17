# Dispatch Pipeline Guide

**Audience:** Cron sessions running `dispatcher.py` multi-skill pipeline.
**Scope:** Determining genuine vs second-wave dispatches, finding eval gaps, and writing consistent journals across Forge + Mentor + Praxis.

This reference consolidates the steady-state workflow validated across 100+ dispatches (2026-06-22 → 2026-06-29). Individual edge cases and one-off incidents remain in the session-specific reference files.

## Genuine vs Second-Wave Decision

The dispatcher can only detect *new journal files* — not whether they've been processed. Journals written by previous dispatch waves look "new" to each subsequent scan. Use this decision procedure:

### Step 0: Identify both eval files

There are TWO eval files. Both must exist and both must be checked:
```bash
PRAXIS_EVAL="<hermes-home>/profiles/indigo/commons/data/ocas-praxis/journals_evaluated.jsonl"
DISPATCH_EVAL="<hermes-home>/profiles/indigo/commons/data/ocas-dispatch/journals_evaluated.jsonl"
```
The praxis eval file is authoritative for "has this been content-evaluated?" The dispatch eval file is authoritative for "has a dispatch wave registered this?" A journal can be in one but NOT the other.

### Step 1: Grep each `new_file` against BOTH eval files

```bash
grep -q "path/to/journal.json" "$PRAXIS_EVAL" && echo "IN_PRAXIS_EVAL" || echo "NOT_IN_PRAXIS_EVAL"
grep -q "path/to/journal.json" "$DISPATCH_EVAL" && echo "IN_DISPATCH_EVAL" || echo "NOT_IN_DISPATCH_EVAL"
```

**Rule:** A journal is "already evaluated" if it is in the PRAXIS eval file. ANY `new_file` not in praxis eval → genuine dispatch requiring full pipeline execution. ALL found in praxis eval → likely second-wave. If found in praxis eval but NOT in dispatch eval, register in dispatch eval (gap) but do NOT trigger full pipeline.

**Eval file schema:** The eval file (`journals_evaluated.jsonl`) uses `journal_id` as the field name for journal paths (NOT `filename` or `journal`). When parsing programmatically:
```python
entry = json.loads(line)
eid = entry.get("journal_id", "")  # ← correct field
```
A naive substring search for the relative path within raw file content also works. Confirmed 2026-06-26 dispatch #164.

**Dual eval file check (confirmed 2026-06-28T16:16Z):** There are TWO eval files that must be checked independently:
1. `commons/data/ocas-praxis/journals_evaluated.jsonl` — Praxis cron pipeline writes here (content evaluation)
2. `commons/data/ocas-dispatch/journals_evaluated.jsonl` — Dispatch waves write here (dedup tracking)

A journal can be in one but NOT the other. Example: `mentor-light-20260628T160608Z.json` was in the praxis eval file (evaluated by cron at 16:07) but NOT in the dispatch eval file. The praxis eval file is authoritative for "has this been content-evaluated?" The dispatch eval file is authoritative for "has a dispatch wave registered this?"

**Rule:** Check the praxis eval file first. If found there, the journal is already content-evaluated — just register in dispatch eval if missing. If NOT in either, it's a genuine gap requiring full processing.

**Note on field names (CORRECTED 2026-07-13):** The two eval files use DIFFERENT field names. Direct inspection on 2026-07-13 confirmed the praxis eval (`commons/data/ocas-praxis/journals_evaluated.jsonl`) keys entries with `journal_id`, while the dispatch eval (`commons/data/ocas-dispatch/journals_evaluated.jsonl`) keys entries with `filename` (every on-disk entry is `{"filename": "...", ...}`, NOT `journal_id`). **When writing programmatically: use `journal_id` for the praxis eval, `filename` for the dispatch eval.** Older text in this guide claimed both use `journal_id` — that was WRONG. Grep-based dedup reads are field-agnostic, so `grep -qF "$key"` works for both.

### Step 2 (genuine dispatch): Find additional eval gaps

`last_ingest_run` in the Praxis state file is an **operation boundary, not a coverage boundary**. Use Python `os.walk` + `mtime` comparison to find ALL journals the prior ingest missed:

```python
import os, json, datetime
journals_dir = "{agent_root}/commons/journals"
state = json.load(open("{agent_root}/commons/data/ocas-praxis/ingest_state.json"))
last_ingest_dt = datetime.datetime.fromisoformat(state["last_ingest_run"].replace("Z", "+00:00"))
# Walk all .json files, compare mtime, check eval set
```

**Explicit-run override with mixed gaps (confirmed 2026-07-11):** When the dispatcher fires an explicit-run override (prompt says "run Forge/Mentor/Praxis") AND `new_files` is a MIX of (a) pipeline-output journals already in both eval files (second-wave re-detection) and (b) genuine cross-skill gaps (e.g. `ocas-reach/*` API-call journals) NOT in either eval file: you MUST run all three pipelines AND manually bridge the genuine gaps. Critical: `praxis_ingest_run.py` discovers journals via an mtime gate `>= last_ingest_run`. Any genuine gap whose mtime PRECEDES `last_ingest_run` will be INVISIBLE to the ingest script and never content-evaluated — it must be registered manually into BOTH eval files (action_taken `dispatch_ingest_no_op` for routine no-op gaps). In the 2026-07-11 run, 7 `ocas-reach` journals at 22:45-22:46Z preceded `last_ingest_run` 22:47:33Z and were missed by the ingest script; manual bridging closed them. Always grep every `new_file` against BOTH eval files to split second-wave re-detections from genuine gaps before deciding what to bridge vs. what the pipelines will auto-handle.

### Classification signals

| Signal | Second-Wave | Genuine Dispatch | Genuine No-Op |
|--------|-------------|-----------------|---------------|
| `new_files` in eval? | ALL found | ANY not found | ANY not found |
| Content actionable? | N/A (already processed) | Yes (new patterns/events) | No (all routine/healthy) |
| Response | No-op + advance state | Full pipeline + backfill | Eval registration only |

**Genuine no-op shortcut:** If all `new_files` are from cron pipelines (`*-cron-{ts}`, `*-light-{ts}`) AND their content shows 0 events / 0 new entries / all routine → skip loading heavy pipeline skills. Just register in eval + advance state + write dispatch-wave journal. This saves significant processing on steady-state no-op dispatches (confirmed 2026-06-26 dispatch #163).

**`new_entries > 0` gaps require full pipeline (confirmed 2026-06-27T22:18Z):** When eval gaps are found and the gap journals show `new_entries > 0` (even just 1-3 entries of routine skill activity), this is NOT a no-op — it's a genuine dispatch requiring full 3-pipeline execution. The `new_entries` count indicates the cron pipeline observed something worth tracking. Do NOT apply the no-op shortcut when `new_entries > 0`.

**Exception — self-referencing Mentor heartbeat `new_entries` (confirmed 2026-06-28T00:05Z):** The Mentor `cron-heartbeat-light.py` script reports `new_entries` equal to the number of journals it ingested during its heartbeat run. This is self-referencing: the Mentor heartbeat counts its own ingestion activity as "new entries" (e.g., `new_entries: 5` when it processed 5 routine journals that the dispatch pipeline hadn't yet registered). The `entities_observed` field shows `[".."]` (current directory reference), confirming no actual new skill knowledge was captured. **Rule:** When the gap journal is from `ocas-mentor` with `heartbeat_type: "light"`, `entities_observed: [".."]`, and the other gap journals in the same dispatch all show 0 events / 0 actionable signals, treat the `new_entries` as self-referencing and apply the genuine-no-op shortcut. Do NOT trigger full pipeline for Mentor heartbeat self-counting. Check `entities_observed` as the discriminator — genuine new observations list specific skill names or proposal IDs, not `[".."]`.

**Exception — Praxis cron `events_recorded > 0` from custodian transient errors (confirmed 2026-06-28T02:13Z):** The Praxis `cron_ingest` script may report `events_recorded: 1` (or `new_entries > 0`) when it processes a custodian `light-scan` journal that recorded `failure_keyword` events classified as `transient` (provider API errors, `cf=None`) or `non_actionable` (disabled stale errors). These are known false-positive patterns — the custodian scan correctly classified them as non-actionable, but Praxis still counts them as "events" in its metrics. **Detection:** The gap journal is from `ocas-praxis` with `run_type: "cron_ingest"`, `events_recorded: 1`, and the event's `signal_type: "failure_keyword"` with `severity: "medium"` and a `summary` containing "transient" or "stale" or "all transient or disabled stale errors". **Rule:** When the praxis-cron journal's only event is a custodian failure_keyword with classification `transient` or `non_actionable` (i.e., the custodian already determined nothing needs fixing), treat the `events_recorded` count as a known false-positive. Apply the genuine-no-op shortcut. Do NOT trigger full pipeline for Praxis counting custodian's "I found errors but they're all transient" events. **Verification check:** Read the event's `summary` field — if it says "all transient" or "all disabled stale errors" or "0 fixes applied", it's a known false-positive. If the event summary mentions active errors or fixes pending, it may be genuine — read carefully before applying the shortcut.

**`is_new: true` does NOT always mean actionable (confirmed 2026-06-27T18:43Z, 2026-06-28T01:35Z):** A thread can be `is_new: true` (genuinely new to the scanner) but still require no action if it's purely informational. Categories of `is_new: true` no-op:
1. **Third-party events** — Meal Train date updates for someone else, event RSVPs, shipping notifications for gifts received (2026-06-27T18:43Z)
2. **Promotional/survey reminders** — Health app survey completions (Verily Me), marketing re-engagement campaigns, service completion nudges (2026-06-28T01:35Z)
3. **Automated notifications** — Cloudflare usage alerts, GitHub commit notifications, CI/CD completions

Classification rule: if `is_new: true` AND content is promotional/automated/third-party (not a direct request, question, or commitment involving <operator>) → `action:none`. This is distinct from second-wave re-detection (`is_new: false`) but produces the same no-op outcome.

**Important — dispatch-wave eval registration (clarification, confirmed 2026-07-07):** The dispatch-wave meta-journal is not a *content* journal and needs no *behavioral* evaluation (do NOT run forge-scan/mentor/praxis event extraction on it). HOWEVER, to prevent the next dispatcher scan from re-detecting it as a "new file" and re-processing it, it MUST still be registered in BOTH eval files as third-wave mitigation: in the PRAXIS eval with `action_taken: "no_signal"` (reason `"dispatch.wave meta-journal, mixed_genuine_no_op"`), and in the DISPATCH eval with `action_taken: "dispatch_output_skip"`. This matches the established pattern — prior waves registered their own dispatch-wave in the praxis eval as `no_signal`. Skipping this registration creates a re-detection loop where the next wave re-classifies the meta-journal as a genuine gap. Only the `new_files` (cron/light journals from other pipelines) need full content-eval entries; the dispatch-wave needs only the lightweight third-wave registration above.

**Mixed genuine no-op with email (confirmed 2026-06-26T18:03Z dispatch ~#38, 2026-06-28T01:35Z):** When a dispatch contains BOTH email triage and journal items, and both are no-op (all emails `action:none` — informational receipts, self-sent briefings, third-party notifications, promotional surveys — AND all journals routine cron output), skip ALL pipeline skill loading (forge, mentor, praxis). This applies even when some email threads have `is_new: true` but content is promotional/survey/automated (Verily Me survey reminder, Cloudflare usage alerts, etc.). Register journals in eval, update email state files, write only the dispatch-wave meta-journal. The key signal: email triage produces 0 actionable + journal gap scan finds only routine no-op. The `is_new: true` flag on promotional emails does NOT make the dispatch actionable — check the email content/intent, not just the flag.

**Dispatch-wave `mixed_genuine_no_op` outcome (confirmed 2026-06-30T06:42Z):** A dispatch-wave journal with `outcome: "mixed_genuine_no_op"` describes a dispatch that processed routine cron output with no actionable behavioral signals. The "genuine" refers to eval registration being genuinely needed (not second-wave re-detection), not to a behavioral event. This is a routine orchestration result. When Praxis ingests dispatch-wave journals, it must filter `outcome` values containing `no_op` (e.g., `mixed_genuine_no_op`, `second_wave_no_op`) as `no_signal` — do not record them as events. The dispatch pipeline completed successfully with no behavioral signals detected.

**Important:** Never infer coverage from `last_ingest_run` proximity. Always grep individually.

### Second-Wave Journal Writing — Do NOT Write `forge-scan-*.json` (confirmed 2026-06-27T23:36Z)

When a second-wave dispatch has explicit pipeline instructions and runs the full pipeline, the agent may incorrectly write `forge-scan-*.json` and `mentor-light-*.json` as its output journals. **This is wrong.**

**Problem:** On a second-wave dispatch, all `new_files` are already in eval. Forge has 0 unprocessed proposals. If the agent writes `forge-scan-20260627T233657Z.json` as a "second-wave no-op" journal, it creates an unnecessary `forge-scan-*.json` file that:
1. Implies Forge pipeline produced output (it didn't — 0 proposals)
2. May be detected as "new" by the next dispatcher wave, triggering another false positive
3. Confuses the signal: future dispatches can't distinguish "Forge scanned something" from "dispatch wrote a no-op"

**Correct behavior:** On second-wave dispatches, write ONLY a `dispatch-wave-*.json` meta-journal. Do NOT write `forge-scan-*.json` or `mentor-light-*.json` journals.

**Exception — pipeline scripts may write their own journals:** The Mentor `cron-heartbeat-light.py` script writes `mentor-light-*.json` as its canonical output. This is correct — the script's journal is authoritative. Suppress the agent's own `mentor-light-*.json` writing, but do NOT suppress the script's output.

**Rule:** Second-wave = write `dispatch-wave-*.json` only. Pipeline scripts keep their canonical journal writing. The agent does NOT write pipeline-specific journals (forge-scan, mentor-light, praxis-dispatch) on second-wave.

**Classification-first ordering (confirmed 2026-06-28T08:35Z):** The agent's default impulse when the dispatcher says "has_work: true" with pipeline instructions is to immediately write all three pipeline journals (forge-scan, mentor-light, praxis-dispatch) as a reflexive first step. **This is wrong.** Classification MUST happen before ANY journal writing. The correct sequence is:
1. Grep each `new_file` against eval → classify as second-wave or genuine
2. IF second-wave: write ONLY `dispatch-wave-*.json`, skip all pipeline journals
3. IF genuine: load pipeline skills, run pipelines, write pipeline journals + third-wave mitigation

**Dispatcher per-item `prompt` is a TEMPLATE, not a classification override (confirmed 2026-07-17):** The `new_journals` dispatch item's `details.prompt` field routinely reads verbatim: "Process them through all three pipelines: (1) Load ocas-forge skill and run Forge journal scan. (2) Load ocas-mentor skill and run Mentor light heartbeat. (3) Load ocas-praxis skill and run Praxis journal ingest." This is a GENERIC template the dispatcher emits for every `new_journals` item — it does NOT assert the current files are genuine-actionable. When classification resolves to `genuine_no_op` (self-referencing Mentor light heartbeat: `entities_observed:["ocas-mentor"]`, `gap_detected:false`, `new_entries` self-counting, 0 events), the classification-first rule WINS: do NOT load or execute the forge/mentor/praxis scripts, do NOT write `forge-scan-*`/`mentor-light-*`/`praxis-dispatch-*` journals. Only register the eval gaps (`bridge_eval_inline.py --action cross_skill_mitigation`), advance both monitor copies + praxis `last_ingest_run`, and write the `dispatch-wave-*` meta-journal (`classification: "mixed_genuine_no_op"`). Obeying the literal per-item prompt on a no-op creates spurious pipeline journals that re-fire as false positives next cycle (the exact "wrote pipeline journals before classification" trap above, triggered by the template's explicit wording). The per-item `prompt` tells you WHICH skills a genuine run WOULD use — it is not authorization to run them when classification says no-op. The same applies to explicit-run overrides: an override flag means "run the pipeline if classification warrants it," not "run it unconditionally."

**Pitfall:** Writing pipeline journals before classification means the agent has already committed to "full pipeline" output before knowing whether it's needed. This wastes processing, creates unnecessary journals that need eval registration, and can trigger false positives on subsequent dispatches. Always classify first, then write.

### Email-Only Second-Wave (confirmed 2026-06-27T18:37Z)

When the dispatcher detects emails where **all threads have `is_new: false`**, this is a second-wave re-detection — the prior dispatch wave already processed these emails. This is the email-side equivalent of the journal second-wave pattern.

**Detection signals:**
- All threads in the dispatch details show `is_new: false`
- The email state file's `last_dispatch` is close to (but before) the current dispatch's `detected_at`
- The state file's `new_threads` is empty (no genuinely new emails since last check)
- Thread subjects/senders match recently-processed emails

**Response:**
1. Do NOT re-open the inbox or re-fetch message content — the triage data in the dispatch details is sufficient
2. Do NOT draft responses, do NOT mark as read, do NOT modify labels
3. Update the email state file's `last_dispatch` timestamp and add a note: "second-wave, 0 actionable, N threads re-detected"
4. Write dispatch-wave journal with `classification: "second-wave"` and `email_triage.notes: "All second-wave re-detection (is_new=false)"`
5. No eval file updates needed (this is purely an email re-detection, not a journal event)
6. No pipeline skills need to be loaded

**Key rule:** `is_new: false` on ALL threads = email second-wave. If even ONE thread has `is_new: true`, it's a genuine dispatch requiring full triage.

**Pattern:** This occurs when the dispatcher's scan interval is shorter than the email processing pipeline's latency. The prior wave wrote its dispatch-wave journal, then the next wave detects the same emails still in the inbox (unread count unchanged) and re-classifies them. The `is_new: false` flag is the authoritative signal — trust it.

### Complete Second-Wave (confirmed 2026-06-28T00:59Z)

When BOTH journals AND email are pure second-wave:
- All journal `new_files` are either already in eval OR are prior-wave dispatch-wave artifacts (timestamp < detected_at)
- All email threads have `is_new: false`
- Net result: 0 eval gaps to register, 0 pipeline skills needed

**Classification:** `"second-wave"` (not `"mixed_genuine_no_op"`)

**Response:**
1. Skip prior-wave dispatch-wave artifacts (don't register in eval)
2. No eval registration needed (all genuine new_files already in eval)
3. Update email state files' `last_dispatch` timestamp
4. Write dispatch-wave journal with `classification: "second-wave"` and `actions_taken.journals.eval_gaps_registered: 0`
5. No pipeline skills needed
6. No third-wave mitigation needed (meaning the wave's OWN output journals need no eval registration — NOT permission to ignore the post-dispatch verifier, see step 7)
7. **STILL run the post-dispatch cron-gap sweep to closure (pattern #7).** When you close via `ocas-dispatch/scripts/wave_close.py`, it runs an independent genuine-gap verifier (`verify_genuine_gap_independent.py`) AFTER writing the wave journal. Cron pipelines (mentor-light, finch weekly, custodian) write new journals AFTER the dispatcher's `detected_at` snapshot but BEFORE your closure — these are pattern #7 post-dispatch gaps, NOT second-wave re-detections, and the verifier will report `GENUINE GAP > 0`. Bridge those specific journals via `ocas-dispatch/scripts/bridge_eval_both_stores.py --action post_dispatch_cleanup <rel_paths>` (idempotent; always place `--action` LAST to dodge the documented value-leak bug). Confirmed 2026-07-14T20:08Z dispatch: verifier flagged `ocas-finch/2026-07-14/weekly-200631.json` (missing from BOTH stores, routine finch self-mining output) + `ocas-mentor/2026-07-14/mentor-light-20260714T200603Z.json` (routine heartbeat, missing from dispatch store only); both bridged, final gap = 0. Do NOT stop at step 6 and skip the verifier — the gap count is a SEPARATE, exogenous signal from the second-wave classification.

**Key signal:** 0 new eval gaps from the DISPATCHER SNAPSHOT + 0 actionable emails = complete second-wave (steps 1–6). The post-dispatch verifier gap count is independent (step 7) and must also be closed to 0 before declaring done. This is the steady-state for dispatches that arrive a few minutes after the prior wave's processing completed.

**Example (2026-06-28T00:59Z):** 3 journal new_files → 2 already in eval (second-wave re-detection) + 1 prior-wave dispatch-wave (skipped). 2 email threads → both `is_new: false` (Cloudflare limit + One Medical follow-up). Result: 0 eval entries, 0 actionable, dispatch-wave journal only.

### Prior-Wave Dispatch-Wave Handling (confirmed 2026-06-28T00:59Z)

When the dispatcher's `new_files` contains a `dispatch-wave-*.json` file whose timestamp is BEFORE the current dispatch's `detected_at`, it is a prior-wave artifact (written by a previous dispatch run).

**CRITICAL RULE:** Skip it entirely — do NOT grep against eval, do NOT register in eval, do NOT process. It is NOT a gap.

**mtime vs. timestamp interaction (confirmed 2026-06-29T02:45Z):** A prior-wave `dispatch-wave-*.json` can have mtime AFTER `last_ingest_run` (making it visible to the gap scan's mtime filter) while its timestamp is still BEFORE `detected_at`. The gap scan filename filter (`"dispatch-wave-" in fname → skip`) is the authoritative exclusion — mtime is irrelevant. Don't be confused when you see a dispatch-wave file with recent mtime that is nonetheless a prior-wave artifact.

**Reasoning:** Dispatch-wave journals are meta-artifacts — they record what a prior wave did, not journal content to be ingested. They don't need eval tracking. Registering them causes false positives on subsequent dispatches.

**Pattern:** Prior-wave dispatch-wave files are detected because their mtime gets touched (by the file being written or directory updates), flagging them as "new" to the dispatcher's scanner. The timestamp comparison (`file.timestamp < dispatch.detected_at`) is the authoritative discriminator.

**Sub-pattern:** This applies to ANY `*.json` file from `ocas-dispatch/*/` that matches a prior-wave pattern (not just `dispatch-wave-*.json` but also `dispatch-*.json`, `email_check_state.json`, etc. from earlier waves). When in doubt: if the file's timestamp is before `detected_at`, skip it.

**Dual eval file registration for prior-wave artifacts (confirmed 2026-06-29T06:14Z):** The "skip entirely" rule means: skip **praxis content-evaluation** (do NOT register in the praxis eval file). But if the prior-wave dispatch-wave artifact is missing from the **dispatch eval file**, it will keep re-appearing as a `new_file` on every subsequent dispatcher scan. **Refined rule:** After skipping praxis registration, grep the artifact against the dispatch eval file. If absent, register it there with `action_taken: "dispatch_output_skip"` to prevent re-detection. This is a lightweight tracking entry, not a content evaluation.

### Security Alerts in Informational Batches (confirmed 2026-06-26T21:01Z)

Security scanning services (GitGuardian, Snyk, Dependabot, etc.) send alert emails that the dispatcher classifies as `intent: "informational"` because they're automated notifications from known senders. Unlike receipts, these contain **actionable intelligence** about the user's infrastructure.

**Detection:** A security alert email arrives in the same batch as routine receipts. The triage system correctly classifies it as `intent: "informational"` and `action:none`. But the content (e.g., "2 secrets detected in commit XYZ") requires human awareness.

**Response:**
1. During email triage, flag any security-scanning-service emails separately from pure receipts
2. Add a `security_alerts` array to the dispatch-wave journal listing the alerts found
3. Surface the alert summary in the dispatch report so the next briefing can include it
4. Do NOT escalate immediately if the repo is private and the secrets are likely test credentials — note for next briefing instead
5. Escalate immediately only if: (a) the repo is public, (b) the secret type is high-risk (API keys, production credentials), or (c) sender indicates active exploitation

**Known-pattern config-repo alerts (confirmed 2026-06-28T01:35Z):** GitGuardian (and similar scanners) will flag auth tokens in your own config/backup repos when those repos store operational credentials (API keys, OAuth tokens, service account JSON). The indigo config repo (`<agent-handle>/indigo`) legitimately stores `config/auth.json` and `credentials/auth/*.json` as part of its operational state. **These are expected, non-actionable detections.** Detection rule: if the alert is about a repo you own AND the "secret" is in a config/credentials file AND the commit message says "backup" or "sync" → known pattern, no escalation. Add to dispatch-wave journal's `security_alerts` array as `known_pattern: config_repo_auth` and move on.

**Sender patterns to watch for:**
- `support@gitguardian.com`, `noreply@security.snyk.io`, `noreply@github.com` (Dependabot)
- Subject patterns: "incident detected", "secret found", "vulnerability", "breach"

### Eval File Location (authoritative)

The eval file is at: `<hermes-home>/profiles/indigo/commons/data/ocas-praxis/journals_evaluated.jsonl`

There are legacy copies at `commons/journals/ocas-praxis/journals_evaluated.jsonl` and `commons/data/praxis/journals_evaluated.jsonl` — these are NOT the authoritative copy. Always use the path above for both reads and writes.

## Eval Gap Patterns (7 catalogued patterns)

| # | Pattern | Journal vs last_ingest_run |
|---|---------|---------------------------|
| 1 | Cron journal gap | AFTER |
| 2 | Tight eval gap | AFTER |
| 3 | Post-ingest cron gap | AFTER |
| 4 | Before-ingest cron gap | BEFORE |
| 5 | Cross-skill gap | ANY (non-standard naming) |
| 6 | Dispatch-output gap | AFTER |
| 7 | Post-dispatch cron gap | AFTER |
| 8 | Stale state backlog | ANY (state days behind) |

**Pattern #8 — Stale state backlog (confirmed 2026-06-28T03:12Z):** When the Praxis `ingest_state.json` has not been updated for days (e.g., `last_ingest_run: "20260626T104320Z"` while current time is June 28), ALL journals written since that timestamp are eval gaps — potentially 400+ entries across all skills. This is not an error — it's a backlog that accumulated because no ingest ran during that window.

**Detection:** `last_ingest_run` is more than 12 hours before "now". The gap scan finds >100 entries.

**Response:**
1. Run the full gap backfill (Python `os.walk` + `mtime` comparison against `last_ingest_run`)
2. Register ALL gaps in eval with source `dispatch-backfill-{ts}`
3. Advance `last_ingest_run` to NOW
4. Update `eval_gaps_backfilled` count in state
5. Check journal content — if all routine (0 events, 0 new entries), apply genuine-no-op shortcut for pipeline skills
6. Write dispatch-wave journal with `classification: "genuine_backfill"`

**Epoch timestamp calculation pitfall (confirmed 2026-06-28T03:12Z):** When computing the mtime cutoff for the gap scan, manually calculating epoch timestamps (e.g., `1782518400` for June 27 00:00 UTC) is error-prone. In this session, `1782873600` (incorrect — off by ~1 day) was used instead of the correct `1782518400`, causing the gap scan to find 0 gaps on the first pass. A second pass with the correct value found 412 gaps.

**Fix — use Python `datetime.timestamp()` instead of manual epoch math:**

```python
from datetime import datetime, timezone

state = json.load(open(state_path))
last_ingest_str = state["last_ingest_run"]
# Parse the ISO timestamp
last_ingest_dt = datetime.fromisoformat(last_ingest_str.replace("Z", "+00:00"))
cutoff = last_ingest_dt.timestamp()  # correct epoch seconds

# OR, if you need a specific date:
cutoff_dt = datetime(2026, 6, 27, 0, 0, 0, tzinfo=timezone.utc)
cutoff = cutoff_dt.timestamp()
```

**Rule:** Never manually compose epoch timestamps from date arithmetic. Always use `datetime(year, month, day, tzinfo=timezone.utc).timestamp()`. A 1-day error means the gap scan either misses hundreds of real gaps or scans zero files.

**Typical gap sources for stale backlog:**
- `ocas-mentor`: light/heartbeat journals (highest volume, every 5 min)
- `ocas-dispatch`: wave journals from prior dispatch runs
- `ocas-praxis`: cron ingest journals
- `ocas-forge`: scan journals
- `ocas-custodian`: light-scan/deep-scan journals
- `ocas-rally`: research journals (non-standard naming)

**Performance:** 400+ file walk + set difference + file append completes in under 30 seconds even on slow storage. a journal's timestamp can be BEFORE `last_ingest_run` yet still NOT be in the eval file. This happens when the prior Praxis ingest ran before the journal was written, then `last_ingest_run` was updated past it without the journal being present to evaluate.

**Phantom `.json` files (confirmed 2026-06-29T07:16Z):** Shell write bugs can produce files literally named `.json` (empty filename) in journal directories. These appear in `os.walk` as `ocas-custodian/2026-06-29/.json` or `ocas-mentor/2026-06-07/.json`. The custodian variant may contain real journal content (a light-scan written with broken filename); the mentor variants are old placeholder files with `RUN_ID_PLACEHOLDER`. **Gap backfill must filter `fname == '.json'`** — these are not valid journals and should never be registered in eval. The updated `ocas-praxis/scripts/gap_backfill.py` includes this filter.

**Mixed pre/post-ingest gap scenario (confirmed 2026-06-28T09:54Z):** A single dispatch can have BOTH dispatcher-reported `new_files` with mtime BEFORE `last_ingest_run` (invisible to gap scan) AND gap-scanned journals with mtime AFTER `last_ingest_run`. Example: dispatcher reports `mentor-light-094524Z` (mtime 09:45:24, before `last_ingest_run` 09:47:25) — not caught by gap scan. Gap scan finds `mentor-light-095026Z` (mtime 09:50:26, after `last_ingest_run`) — caught by gap scan. Both are genuine gaps (not in eval). **Rule:** Process dispatcher `new_files` and gap-scanned journals independently — dispatcher files via grep, gap files via mtime. Do NOT assume the gap scan catches everything. The gap scan is a SUPPLEMENT, not a replacement.

## Journal Writing Standards

### Timestamp composition (shell-safe)

Always compose timestamp ONCE, reuse for both filename and content:

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
NOW=$(date -u +%Y-%m-%dT%H:%M:%S.000000+00:00)
cat > "$DIR/forge-scan-${TS}.json" << EOF
{"run_id": "forge-scan-${TS}", "timestamp": "$NOW", ...}
EOF
```

**Never** use Python f-strings with `{TS}` inside `terminal()` — bash `${}` expansion consumes the braces. Also never embed `$(date)` twice in one heredoc — clock rollover between calls produces mismatched timestamps.

### Forge no-op journal

```json
{
  "schema": "forge-journal-v1",
  "run_id": "forge-scan-{TS}",
  "timestamp": "{NOW}",
  "action": {"result": "no_op", "findings": {"unprocessed_proposals": 0, ...}},
  "outcome": "success",
  "trigger": "dispatch"
}
```

### Dispatch-wave journal (meta-journal)

Written by the dispatch pipeline itself. **Does NOT need eval registration.**

```json
{
  "timestamp": "{NOW}",
  "type": "dispatch.wave",
  "run_id": "dispatch-wave-{TS}",
  "result": "success",
  "summary": "Human-readable one-line summary",
  "classification": "second-wave | mixed_genuine_no_op | full_pipeline | mixed_genuine_no_op",
  "actions_taken": {
    "journals": { "eval_gaps_found": N, "eval_gaps_registered": N, "pipelines_loaded": N },
    "email_triage": { "indigo_inbox": { "threads_reviewed": N, "actionable": N } }
  },
  "escalations": [],
  "notes": "Detailed notes"
}
```

**Classification values:**
- `second-wave` — all new_files already in eval or prior-wave artifacts, all emails is_new=false. 0 eval gaps to register.
- `mixed_genuine_no_op` — genuine eval gaps (routine cron) + email second-wave (all is_new=false)
- `full_pipeline` — genuine actionable dispatch, all 3 pipelines loaded
- `mixed_genuine_no_op` — both email and journals are no-op but dispatch had new_files not in eval

### Praxis dispatch-ingest journal

```json
{
  "run_id": "praxis-dispatch-{TS}",
  "timestamp": "{NOW}",
  "type": "praxis.dispatch-ingest",
  "source": "dispatch",
  "action": {"result": "ingest_complete", "findings": {"new_journals_processed": N, "dispatched_files": [...]}}
}
```

## Eval File Format

Each entry: one JSON object per line, relative path (no absolute paths). **Field name differs by file:** praxis eval uses `journal_id`; dispatch eval uses `filename` (see the field-name note above). The example block below is the praxis-eval shape.

```json
{"journal_id": "ocas-mentor/2026-06-26/mentor-light-{TS}.json", "action_taken": "dispatch_ingest_no_op", "source": "dispatch-new-journal-{dispatcher_ts}", "backfill_at": "{now_iso}"}
```

**CRITICAL — path base:** `journal_id` must be relative to `{agent_root}/commons/journals/`, NOT to the profile root. When using `os.path.relpath()`, the second argument MUST be the **absolute path** to `commons/journals`:

```python
# CORRECT (cron-safe, works regardless of CWD)
relpath = os.path.relpath(fpath, '<hermes-home>/profiles/indigo/commons/journals')

# CORRECT (if you've os.chdir'd to profile root first)
os.chdir('<hermes-home>/profiles/indigo')
relpath = os.path.relpath(fpath, 'commons/journals')

# WRONG — produces garbage with ../../ prefixes when CWD != profile root
relpath = os.path.relpath(fpath, 'commons/journals')  # if CWD is /root, resolves to <commons>/journals/

# WRONG — produces "commons/journals/ocas-praxis/..." (still prefixed)
relpath = os.path.relpath(fpath, '.')
```

The cron working directory is `/root`, NOT the profile root. A relative base like `'commons/journals'` resolves against `<commons>/journals/` (which doesn't exist), producing `../../../../../.hermes/profiles/indigo/commons/journals/...` paths. Always use absolute paths for relpath base dirs in cron scripts. Confirmed 2026-06-26 dispatch #169.

**Gap backfill false positive from cross-directory relpath (confirmed 2026-06-27T23:20Z):** When the gap backfill `find` scans both `<hermes-home>/profiles/indigo/commons/journals/` and `<hermes-home>/commons/journals/` (the non-profile commons), `os.path.relpath(fpath, '<hermes-home>/profiles/indigo/commons/journals')` for commons files produces `../../../../commons/journals/ocas-mentor/...` paths. These NEVER match eval entries (which use clean `ocas-mentor/...` relative paths), so the gap scan reports ALL commons journals as "missing" — a false-positive list of 100+ entries.

**Fix:** During gap backfill, ALWAYS check the eval file by **filename only** (`grep -qF "$basename" eval_file`) rather than by full path. If the basename is found anywhere in the eval file, the journal is already tracked — skip. Do NOT add the `../../../../commons/journals/...` version as a new entry. Better: skip the `<hermes-home>/commons/journals/` directory entirely in the gap scan — it is monitored by a different dispatcher instance.

**Symptom:** Gap scan reports 120+ "missing" journals, all with `../../../../commons/j...` prefixes. Manual verification of 5 random entries shows 100% already in eval under clean relative paths. This is a path format false positive, not genuine gaps.

**CRITICAL — avoid `import datetime` + `from datetime import datetime` in the same script:**

```python
# SAFE — class shadows the name, datetime.now() works
from datetime import datetime, timezone
now = datetime.now(timezone.utc)

# DANGEROUS — `datetime` refers to the module, not the class
import datetime
from datetime import datetime as dt, timezone
now = datetime.now(timezone.utc)  # AttributeError: module has no attr 'now'
now = dt.now(timezone.utc)  # This works, but mixing patterns is error-prone
```

In cron scripts, always use `from datetime import datetime, timezone` and never also `import datetime`.

**Fields:**
- `journal_id` — relative path from `commons/journals/` (e.g., `ocas-mentor/2026-06-26/file.json`)
- `action_taken` — verb phrase describing action (e.g., `backfill_generic`, `dispatch_ingest_no_op`, `post_dispatch_cleanup`)
- `source` — origin tag (see below)
- `backfill_at` — ISO timestamp when entry was registered

**Sources:**
- `dispatch-new-journal-{ts}` — journals the dispatcher detected
- `dispatch-eval-gap-backfill` — journals found via broader mtime scan
- `dispatch-third-wave-mitigation` — current run's own output journals
- `post-dispatch-cleanup` — journals written by cron pipelines between our backfill and our third-wave entries

## Third-Wave Mitigation

After writing Praxis journal, add ALL current-dispatch output journals to eval (forge-scan, mentor-light, praxis-dispatch) so subsequent dispatcher scans don't flag them as new.

**Timestamp mismatch pitfall (confirmed 2026-06-27T19:40Z):** When the dispatch pipeline performs multiple steps — gap backfill (step 1), journal writing (step 2), third-wave mitigation (step 3) — each step calls `datetime.now()` or `$(date)` independently. The timestamp used in step 1's state update differs from the timestamp in step 2's journal filenames, which differs from step 3's eval entries. Result: eval entries don't match actual journal filenames → false "gap" detection on next dispatch.

**Root cause:** In this session, the state-update code composed `ts_str = datetime.now().strftime(...)` at the start of step 1. Journals written in step 2 got timestamps from a second `datetime.now()` call seconds later. Step 3's third-wave mitigation used the ORIGINAL `ts_str` (from step 1), but the journal filenames used step 2's timestamps. The grep check failed because `forge-scan-20260627T194704Z` (actual file) didn't match `forge-scan-20260627T194653Z` (eval entry from step 3).

**Fix — compose ALL timestamps BEFORE any file operations, reuse everywhere:**

```python
import json, os, datetime

# Step 0: Compose ALL timestamps once, before any file writes
now_ts = datetime.datetime.now(datetime.timezone.utc)
ts_file = now_ts.strftime("%Y%m%dT%H%M%SZ")    # for filenames
now_iso = now_ts.isoformat()                             # for JSON content

# Step 1: Gap backfill (uses ts_file for source labels)
# Step 2: Write journal files (uses ts_file for filenames)
# Step 3: Third-wave mitigation (uses ts_file for journal_id in eval)
```

**Rule:** Call `datetime.now()` EXACTLY ONCE at the start of the dispatch pipeline. Never call it again for timestamps — the seconds between calls produce mismatched filenames.

**Cross-step pitfall (confirmed 2026-06-27T22:18Z):** The "compose ONCE" rule applies across the ENTIRE pipeline, not within each step. When the dispatch writes journals in step 2 (e.g., `praxis-dispatch-TS.json`) using one `datetime.now()` call, then step 3 (third-wave mitigation) calls `datetime.now()` again to register that journal in eval, the timestamps diverge. The eval entry says `praxis-dispatch-221915Z` but the actual file is `praxis-dispatch-221825Z` — a 50-second gap across two `datetime.now()` calls.

**Inline Python block timestamp divergence (confirmed 2026-06-29T03:48Z):** When the Praxis ingest + third-wave logic runs inside a single `terminal()` call via `python3 << 'PYEOF'`, the Python block composes its own `datetime.now()` timestamp internally. This diverges from any shell-level `TS=$(date ...)` variable set in a PRIOR `terminal()` call — the shell variable is invisible to the inline Python. Result: the Python block writes `praxis-dispatch-035149Z.json` to disk and registers it in eval, but the Forge no-op journal (written in a prior `terminal()` call with `TS=034834Z`) gets a third-wave eval entry using the Python block's NEW timestamp (`forge-scan-035149Z.json`) — a phantom entry that doesn't correspond to any real file. **Fix:** Either (a) compose ALL timestamps INSIDE the same Python block that writes journals and eval entries (the single-block approach), or (b) write journal filenames to a temp file in the Python block so subsequent steps can read the actual filenames. Never assume a shell `TS` variable from a prior `terminal()` call matches timestamps composed inside a later inline Python block. Confirmed 2026-06-29: phantom eval entry detected and removed post-hoc.

**Fix:** Compose ALL output journal filenames in step 0 (before any file writes). Pass them through as variables. Step 2 writes files using those pre-composed names. Step 3 registers those SAME names in eval. No step ever calls `datetime.now()` independently.

```python
# Step 0: Compose ALL filenames ONCE
now_ts = datetime.now(timezone.utc)
ts_file = now_ts.strftime("%Y%m%dT%H%M%SZ")
now_iso = now_ts.isoformat()

# Pre-compose ALL journal filenames
forge_journal = f"ocas-forge/YYYY-MM-DD/forge-scan-{ts_file}.json"
mentor_journal = f"ocas-mentor/YYYY-MM-DD/mentor-light-{ts_file}.json"
praxis_journal = f"ocas-praxis/YYYY-MM-DD/praxis-dispatch-{ts_file}.json"

# Step 1: Gap backfill (uses ts_file for source labels)
# Step 2: Write journal files (uses pre-composed filenames)
# Step 3: Third-wave mitigation (uses pre-composed filenames for eval entries)
```

**Verification:** After writing all journals and eval entries, grep each actual journal filename against the eval file. If any MISSING, the timestamps diverged — append correct entries with the actual filenames immediately.

**Third-wave overlap with concurrent Praxis cron (confirmed 2026-06-29T09:26Z):** When the dispatch runs a Mentor heartbeat that writes `mentor-light-{ts}.json`, a concurrent Praxis cron (running every ~30 min) may register that journal in eval BEFORE the dispatch's third-wave mitigation runs. Result: third-wave finds 0 entries to add (the journal is already tracked). **Do NOT assume third-wave failed** — grep the actual heartbeat output filename against eval to confirm it's present. If present (registered by concurrent cron), skip third-wave for that journal. This is expected behavior in steady-state with overlapping cron schedules.

**Post-dispatch cron gap in tight timing windows (confirmed 2026-06-29T09:26Z):** Even when `last_ingest_run` is only ~7 minutes before dispatch `detected_at`, a cron pipeline can write a new journal between the Mentor heartbeat and the third-wave mitigation. The post-dispatch cleanup `os.walk` catches these. **Always run post-dispatch cleanup**, even when timing appears tight.

**Exception — dispatch-wave journals do NOT need manual eval registration.** The `dispatch-wave-TS.json` journal written by the dispatch pipeline itself is a dispatch-output artifact, not a Praxis-ingested journal. Only non-dispatch journals (mentor-light, praxis-cron, forge-scan from other pipelines) need eval tracking. MANUALLY registering dispatch-wave journals in eval causes false gap detection on subsequent dispatches — the next wave would find the dispatch-wave journal "not in eval" and treat it as a genuine new gap. Confirmed 2026-06-27T15:15Z dispatch ~#151554.

**Sub-pattern — Praxis script auto-registers dispatch-wave journals (confirmed 2026-06-27T21:45Z):** The Praxis `dispatch_ingest_*.py` script walks ALL `.json` files with mtime >= `last_ingest_run` — including dispatch-wave journals from PRIOR waves. When it finds one not in eval, it evaluates it and registers it with `action_taken: no_signal_noise`. This is CORRECT behavior — the ingest script treats dispatch-wave journals as regular journals to evaluate. Do NOT remove these auto-registered entries or treat them as errors. The "NEVER register dispatch-wave" rule applies to MANUAL registration by the agent (especially post-dispatch cleanup), not to the Praxis script's auto-evaluation. If a dispatch-wave journal appears in eval from the ingest script, leave it — removing it would cause the next dispatch to falsely flag it as a gap.

**Post-dispatch cleanup must NEVER register dispatch-wave journals (confirmed 2026-06-27T21:14Z):** The post-dispatch cleanup `os.walk` finds ALL `.json` files with mtime after `last_ingest_run` — including the dispatch-wave journal that was just written. If the cleanup script does not explicitly exclude `dispatch-wave-*.json` files, it will erroneously register them in eval. Then the next dispatch detects them as "genuine gaps" (not in eval), triggering a false positive. **Fix:** After `os.walk` gap scan, filter out any path matching `*/dispatch-wave-*.json` before appending to eval. Or: check if the journal_id contains `dispatch-wave-` and skip. If an erroneous entry is detected (dispatch-wave in eval), remove it immediately and decrement the state counter.

**Prior-wave dispatch-wave re-detection (confirmed 2026-06-27T16:59Z):** When the dispatcher's `new_files` contains a `ocas-dispatch/*/dispatch-wave-*.json` file from a PRIOR wave (not the current one), it is always self-referential — the prior wave wrote it as its own meta-journal. Detection: the file's `timestamp` is BEFORE the current dispatch's `detected_at`. Response: skip it entirely (do not grep against eval, do not register, do not process). It is not a gap — it is a known dispatch-output artifact. Only the current wave's own dispatch-wave journal is written at the end of THIS run.

**Prior-wave dispatch-*.json re-detection (confirmed 2026-06-27T23:15Z):** The dispatcher may also list `ocas-dispatch/*/dispatch-*.json` files from PRIOR waves (not just `dispatch-wave-*.json`). These are full dispatch journals from earlier waves. Detection rule is the same — the file's `timestamp` is BEFORE the current dispatch's `detected_at`. Response: same — skip entirely during initial classification. **Critical sub-pattern:** Prior-wave `dispatch-*.json` files may NOT be in the eval file (confirmed 2026-06-27T23:15Z: `dispatch-20260627T230700Z.json` was missing from eval despite being days old). During final verification (grep each new_file against eval), if a prior-wave dispatch artifact is found MISSING from eval, add it with `action_taken: "dispatch_output_skip"` and `source: "dispatch-eval-gap-backfill-{ts}"`. Do NOT treat this as a new dispatch trigger — it's just registering a known artifact that slipped through eval tracking.

**Mixed prior-wave artifacts + genuine gaps (confirmed 2026-06-27T23:15Z):** When dispatcher `new_files` contains BOTH prior-wave dispatch artifacts (skip) AND genuinely-new cron journals (not in eval, new_entries > 0), treat as a genuine dispatch for the new gaps but skip the prior-wave artifacts. The presence of prior-wave artifacts in `new_files` does NOT make the entire dispatch a second-wave. Process each file independently: skip prior-wave (timestamp < detected_at), process genuine gaps. The 23:15Z dispatch had 3 new_files: 2 prior-wave dispatch artifacts (skipped) + 1 mentor-light already in eval + 2 mtime-discovered gaps with new_entries > 0 → full pipeline execution.

## Post-Dispatch Cleanup

After the third-wave mitigation, run ONE MORE `os.walk` for any `.json` files with mtime after `last_ingest_run` still not in eval. These are cron-pipeline journals that slipped in between our operations. Add them with source `post-dispatch-cleanup`.

**Dispatch-wave exclusion (confirmed 2026-06-27T21:14Z):** The `os.walk` gap scan will find the dispatch-wave journal that was just written (its mtime is after `last_ingest_run`). **NEVER register dispatch-wave journals in eval.** Filter them out before appending:
```python
# After os.walk gap scan:
gaps = [g for g in gaps if "dispatch-wave-" not in g["path"]]
```
If an erroneous dispatch-wave entry is detected in eval, remove it immediately and decrement the state counter.

**Eval file deduplication (confirmed 2026-06-26 dispatch #169):** Over many dispatches, the eval file can accumulate duplicate entries — the same `journal_id` registered multiple times by different waves. Before rewriting or after large backfills, deduplicate:

```python
seen = set()
clean = []
for entry in entries:
    jid = entry.get('journal_id', '')
    if jid not in seen:
        seen.add(jid)
        clean.append(entry)
# Rewrite with deduped list
```

A dedup that removes >1000 entries is normal for the first cleanup after eval tracking begins. If it happens repeatedly, investigate whether the same journals are being re-registered across waves.

## Evidence run_id vs wave-journal filename divergence (confirmed 2026-07-11)

When the dispatch wave writes BOTH a `dispatch-wave-*.json` journal AND an evidence entry in `evidence.jsonl` (the dispatch skill's evidence log), the evidence entry's `run_id` field and the wave journal's actual `run_id`/`filename` MUST match. In the 2026-07-11 run, the wave journal was written as `dispatch-wave-20260711T212130Z.json` (run_id inside: `dispatch-wave-20260711T212130Z`) but the evidence entry composed its `run_id` from a SEPARATE `date` call 8 seconds earlier (`dispatch-wave-20260711T212122Z`). Result: the evidence log references a non-existent wave-journal filename, breaking traceability. (The eval-file bridge correctly used the real filename, so re-detection was not affected — but the log is internally inconsistent and any downstream join on `run_id` fails.)

**Root cause:** The guide already requires composing timestamps ONCE for journal files + eval bridges, but the evidence entry is written in a THIRD terminal call with its own `date` invocation, drifting from the wave journal's timestamp.

**Fix (pick one, apply consistently):**
1. **Write the wave journal FIRST**, then read its actual `run_id` from the file and reuse that exact string as the evidence entry's `run_id`. Never re-compose a timestamp for the evidence.
2. OR compose ONE `TS` shell variable at the very start of the wave and reuse it for the wave journal filename/run_id AND the evidence `run_id` — no second `date` call anywhere.

**Rule:** The evidence entry's `run_id` must be a verbatim copy of the wave journal's `run_id`, not an independently-composed timestamp. If you wrote the wave journal in one `terminal()` call and the evidence in another, you drifted — fix by reading the journal's run_id back and using it verbatim.

## Shell gotcha: `find` with multiple `-name` patterns needs `\( \)` grouping (confirmed 2026-07-11)

During the Forge proposal audit, `find DIR -name "vp_*.json" -o -name "vd_*.json"` silently dropped matches (returned only `processed/` files, hiding 11 `vp_*.json` files sitting in `proposals/`). Re-running with explicit grouping `find DIR \( -name "vp_*.json" -o -name "vd_*.json" \)` returned the complete set.

**Fix:** Always wrap multiple `-name`/`-path` alternatives in `\( \)` when using `-o`. Ungrouped `-o` chains produce incomplete results that can mislead audit conclusions (e.g., falsely reporting "0 unprocessed proposals" when files exist in a non-`processed/` directory).

## OCAS pipeline script invocation pitfall (confirmed 2026-07-13 dispatch)

**`--help` / unknown flags EXECUTE these scripts instead of printing usage.** `ocas-mentor/scripts/cron-heartbeat-light.py` and `ocas-praxis/scripts/praxis_ingest_run.py` have NO argument parser — passing `--help` (or any unrecognized flag) does NOT print usage, it runs the script for real (heartbeat with empty stdin; praxis ingest with a full filesystem scan that mutates state and eval files). Do NOT probe these scripts with `--help` to discover their interface in cron mode; you will trigger a real execution and mutate eval/state. To learn a script's behavior, read its source or the relevant SKILL.md / `references/`. (Contrast: `ocas-forge/scripts/run_dispatch_pipeline.py` uses argparse and correctly prints usage on `--help`.)

## Phantom File Prevention

After every dispatch run, verify journal filenames under all three pipeline directories:
- No empty timestamps: `forge-scan-.json`
- No double timestamps: `dispatch-20260626T20260626T082335Z.json`
- No literal placeholders: `TS_PLACEHOLDER`, `PLACEHOLDER`

If found: delete immediately and rewrite with the shell `TS=$(date ...)` pattern.

## State File Schema

The Praxis ingest state file (`{agent_root}/commons/data/ocas-praxis/ingest_state.json`) uses **mixed types** — some fields are integers, some are timestamps. Always check the type before arithmetic:

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `last_ingest_run` | ISO timestamp string | `"2026-06-27T21:51:11.000000+00:00"` | Use `fromisoformat()` to parse |
| `journals_evaluated_count` | integer | `40783` | Safe to increment with `+ N` |
| `last_eval_file_line` | integer | `40783` | Safe to increment with `+ N` |
| `dispatch_wave` | **timestamp string** | `"20260627T200551Z"` | NOT an integer counter! Never `int()` this field |
| `last_dispatch_wave` | **timestamp string** | `"20260627T200551Z"` | NOT an integer counter! |
| `last_run` | timestamp string | `"20260627T215408Z"` | ISO timestamp of last run |
| `last_ingest_ts` | timestamp string | `"20260627T215408Z"` | Short timestamp for last ingest |
| `last_ingest_source` | string | `"dispatch-second-wave-backfill"` | Origin tag |
| `last_ingest_note` | string | (human-readable) | Diagnostic note |
| `third_wave_mitigation` | integer | `42` | Counter — safe to increment |
| `eval_gaps_backfilled` | integer | `7` | Counter — safe to increment |
| `dispatch_wave` (integer counter) | DOES NOT EXIST | — | There is no integer wave counter; `dispatch_wave` IS the timestamp |

**Type pitfall (confirmed 2026-06-27T21:50Z):** Attempting `int(state.get("dispatch_wave", 0))` crashes with `ValueError: invalid literal for int() with base 10: '20260627T200551Z'`. If you need a wave sequence number, count dispatches from the session log or use a separate counter field — do not cast `dispatch_wave` to int.

**Safe update pattern:**
```python
# Integer fields — safe to increment
state["journals_evaluated_count"] = int(state.get("journals_evaluated_count", 0)) + N
state["last_eval_file_line"] = int(state.get("last_eval_file_line", 0)) + N
state["third_wave_mitigation"] = int(state.get("third_wave_mitigation", 0)) + N

# Timestamp fields — replace with new timestamp, never increment
state["dispatch_wave"] = ts  # current wave timestamp
state["last_dispatch_wave"] = ts
state["last_ingest_run"] = now.strftime("%Y-%m-%dT%H:%M:%S.000000+00:00")
```

## State File Updates

**Skip state write if already current from concurrent cron (confirmed 2026-06-29T06:39Z):** Before updating `ingest_state.json`, read `last_ingest_run` and compare to the current dispatch's `detected_at`. If `last_ingest_run > detected_at` (a concurrent Praxis/Mentor cron advanced the state after the dispatcher scanned), the state is already past all `new_files`. Skip the `json.dump` write entirely — just append a note to `last_ingest_note` if diagnostic context is needed. This prevents unnecessary writes, avoids race conditions with concurrent cron state updates, and prevents counter drift.

After eval file updates, advance `last_ingest_run` to NOW and increment `journals_evaluated_count`. Use `json.load()` — never trust `read_file` for JSON state.

**Counter sync (confirmed 2026-06-26 dispatch #165, 2026-06-27T21:45Z):** After post-dispatch cleanup completes, do a final line count of the eval file and set both `journals_evaluated_count` and `last_eval_file_line` to the actual count. The state counter only tracks what the current dispatch explicitly adds; post-dispatch cleanup entries are appended without updating it. Over multiple dispatches, the state counter diverges from reality (e.g., state said 39603 while eval file had 39737 lines; state said 40762 while eval file had 40782 lines). Not critical for correctness (grep checks are authoritative), but keeps diagnostics accurate. **Best practice:** After every eval file modification, run `wc -l` and update the state counter to match the actual count.

## Genuine No-Op Dispatch (confirmed 2026-06-26 dispatch #163)

A genuine dispatch where the `new_files` are routine cron output that hasn't been registered in eval, but contains no actionable signals. Detection: files NOT in eval (genuine), but journal content shows all-no-op (0 new entries, 0 events, all routine/healthy).

**Response:**
1. Grep each `new_file` against eval → NOT found (genuine)
2. Run all 3 pipelines → all return no-op
3. Add `new_files` to eval file with source `dispatch-new-journal-{ts}` and action `dispatch_ingest_no_op`
4. Advance `last_ingest_run` in state file
5. Write dispatch-wave journal (in ocas-dispatch date dir)
6. **Do NOT write forge-scan / mentor-light / praxis-dispatch journals** — no pipeline produced output worth tracking. Only the dispatch-wave meta-journal is written.
7. No third-wave mitigation needed (no pipeline journals were produced)
8. **Post-dispatch cleanup:** Run `os.walk` for gaps but EXCLUDE `dispatch-wave-*.json` files. Any dispatch-wave journal found in the gap scan must be skipped — registering it causes false positive on next dispatch.

**Eval entries added:** 1 per `new_file` not already in eval (just the registration entries, no pipeline output).

**Key signal:** If all `new_files` are from cron pipelines (filename pattern `*-cron-{ts}`, `*-light-{ts}`) AND their content shows 0 events / 0 new entries / all routine, this is a no-op registration dispatch. The cron pipeline already evaluated them; the dispatch just needs to register them in eval.

**Duplicate registration prevention (confirmed 2026-06-29T06:39Z):** After grepping `new_files` against eval and finding them already present, do NOT re-register. Register ONLY files that are NOT already in eval. A duplicate entry is harmless (grep checks are authoritative) but inflates the eval file and wastes linespace. If accidentally created, run the dedup routine (see Eval File Deduplication section) to remove duplicates by `journal_id`.

**`is_new: true` promotional emails in no-op dispatches (confirmed 2026-06-28T01:35Z):** A dispatch can contain email threads where `is_new: true` (the scanner hasn't seen them before) but the content is promotional/survey/automated (Verily Me health survey, service re-engagement nudges, automated usage alerts). The `is_new` flag reflects scanner novelty, not actionability. When ALL emails are `action:none` (regardless of `is_new` status) AND all journals are routine, apply the genuine-no-op shortcut. Check email intent/content, not `is_new` flag, when classifying mixed dispatches.

**⚠️ Count accuracy is critical** — always verify with post-write grep that ALL dispatcher `new_files` are in eval after registration. Two confirmed pitfalls: (1) missing new_files when similar-named files cause false confidence (a `dispatch-wave-mentor-*` being in eval does NOT mean `mentor-light-*` is in eval), (2) writing the wrong count in the dispatch-wave journal. See "Genuine No-Op Count Accuracy" section below.

**Inline eval registration for routine no-op gaps (confirmed 2026-06-29T09:12Z):** When the only gap is a routine cron journal (filename matches `*-cron-*` or `*-light-*`), you can register it directly via inline Python rather than loading `praxis_ingest_run.py`:

1. Grep each `new_file` against praxis eval → identify missing ones
2. For each missing file, read content to confirm: `events_recorded` is 0 or all `no_signal`, `not_activity_reason` explains routine verdict
3. If confirmed routine: append eval entry directly with `action_taken: "dispatch_ingest_no_op"`, update `ingest_state.json` inline (advance `last_ingest_run`, increment `journals_evaluated_count` to actual `wc -l` count)
4. Skip loading `praxis_ingest_run.py` entirely — it would produce the same result with more overhead

**When NOT to use inline registration:** If the gap journal has genuine events (`events_recorded > 0` with non-no_signal types), `new_entries > 0` with specific `entities_observed` (not `[".."]`), or is from a non-cron skill (e.g., rally research, custodian deep-scan) — run the full ingest script.

**Counter miscount during mixed no-op registration (confirmed 2026-06-29T07:48Z):** When registering eval entries in a mixed no-op dispatch, the counter variable that tracks "entries added to praxis eval" can undercount if the registration logic uses tuple-tagged lists (e.g., `('dispatch_eval', jid)` vs `('praxis_eval', jid)`) and filters by tag. The mentor-light journal IS appended to the praxis eval file, but the counter only increments for entries matching the `praxis_eval` tag — and the dispatch-wave artifact (tagged `dispatch_eval`) is skipped. Result: counter reports 0 praxis additions when 1 was actually made. **Fix:** After ALL eval file appends, always do a final `wc -l` sync of the praxis eval file and set `journals_evaluated_count` to the actual count. Do not rely on in-registration counter increments — they are fragile when registration paths diverge (some entries go to one file, some to both).

## Massive Legacy Eval Backfill (confirmed 2026-06-26 dispatch #166)

The first eval gap scan after enabling eval tracking can discover **thousands** of unregistered journals. This is not an error — it's the initial catch-up.

**Detection:** `os.walk` finds 10,000+ `.json` files in `commons/journals/` not in the eval file. Confirmed: 11,230 gaps from cron pipelines (finch, lucid, spot) dating back to April 2026.

**Stale state backlog variant (confirmed 2026-06-28T03:12Z):** A similar but distinct pattern occurs when the Praxis `ingest_state.json` was updated days/weeks ago but no ingest ran during that window. Unlike the initial backfill (which is a one-time event after enabling eval tracking), stale state can recur if the ingest pipeline fails silently or the dispatcher doesn't trigger for an extended period. In this session, `last_ingest_run` was June 26 but current time was June 28 — 412 journals had accumulated.

**Detection:** `last_ingest_run` is more than 12 hours before "now". Gap scan finds >100 entries. This is NOT the initial backfill — it's a recurring operational gap.

**Response:** Same as initial backfill — register all gaps in one pass. But also investigate WHY the state was stale: check if the dispatcher is running on schedule, if the Praxis cron is executing, and if any errors are being silently swallowed.

**Typical gap sources:**
1. Backfill ALL gaps in one pass (append to eval file with `source: post-dispatch-cleanup-{ts}`)
2. This is a **one-time event** — after initial backfill, subsequent dispatches should see 0 gaps (or only new cron journals from the last few minutes)
3. If gaps >1000 appear AFTER the initial backfill, investigate — a cron pipeline may be writing to the wrong directory or the eval file was truncated

**Typical gap sources:**
- `ocas-finch`: daily/work/scan journals (highest volume, Apr 13+)
- `ocas-lucid`: dream journals (Apr 17+)
- `ocas-spot`: sweep/watch journals (May 30+)
- `ocas-mentor`: light/heartbeat journals with non-standard naming (`light_YYYYMMDD_HHMMSS.json`)

**Second occurrence (confirmed 2026-06-29T12:40Z):** A second large backfill of 12,087 journals occurred when the gap scan walked the entire journals directory and found all pre-tracking journals (May 13 to June 22) unevaluated. Root cause: the eval file had been tracking only dispatch-wave and cron-pipeline journals from the past ~3 days, while journals from mid-May to mid-June were never registered. **This was still a one-time event** — after this backfill, the eval file is comprehensive (60,590 entries) and subsequent dispatches will only see truly new journals.

**Performance:** 11k file walk + set difference + file append completes in under 30 seconds.

## Journals Per Dispatch (typical case)

A genuine dispatch with 2 eval gaps produces 6 entries in the eval file:
1. Dispatcher-detected journal (source: `dispatch-new-journal-{ts}`)
2. Gap journal 1 (source: `dispatch-eval-gap-backfill`)
3. Gap journal 2 (source: `dispatch-eval-gap-backfill`)
4. Forge output (source: `dispatch-third-wave-mitigation`)
5. Mentor output (source: `dispatch-third-wave-mitigation`)
6. Praxis output (source: `dispatch-third-wave-mitigation`)

**`run_dispatch_pipeline.py` broken on Python 3.14 (confirmed 2026-06-30T09:34Z):** The script at `skills/ocas-forge/scripts/run_dispatch_pipeline.py` has `parser.add_argument('--new-files', nargs='[]', default=[])` which Python 3.14's argparse rejects with `ValueError: invalid nargs value`. The script cannot be used for automated dispatch pipeline execution. **Workaround**: dispatch pipeline logic must be executed manually via inline `python3 -c` or `python3 << 'PYEOF'` heredoc in `terminal()`. Fix requires changing `nargs='[]'` to `nargs='*'` (variable positional args) or removing the argument entirely.

**Praxis-cron double-Z timestamp bug still active (confirmed 2026-06-30T09:34Z):** The Praxis cron ingest script continues to produce journals with double-Z suffixes (e.g., `praxis-cron-20260630T092758ZZ.json`). This is a timestamp composition bug where `ts.rstrip('Z') + 'Z'` is being applied to a value that already ends with Z, or where two ISO timestamps are being concatenated. **Mitigation**: the dispatch pipeline treats these filenames as-is for eval registration (no rename needed), but the root cause should be fixed in `praxis_ingest_run.py` or `praxis_common.py`.

## Cron-Safe Python Patterns

When writing Python for `terminal()` heredocs in cron mode, follow these rules:

### `datetime` import

```python
# CORRECT — class shadows the name at the `datetime` binding
from datetime import datetime, timezone
now = datetime.now(timezone.utc)  # works

# WRONG — module + class alias shadow each other
import datetime
from datetime import datetime as dt, timezone
now = datetime.now(timezone.utc)  # AttributeError: module has no 'now'
```

### `os.path.relpath` base directory

```python
# CORRECT — absolute path, CWD-independent
relpath = os.path.relpath(fpath, '<hermes-home>/profiles/indigo/commons/journals')

# WRONG — relative base resolves against CWD (/root in cron), not profile root
relpath = os.path.relpath(fpath, 'commons/journals')
```

### `write_file` line-wrapping corrupts Python (confirmed 2026-06-30T10:20Z)

The `write_file` tool silently wraps long lines (~80 chars), splitting Python string literals and variable assignments mid-token. This produces syntax errors or, worse, silently corrupted variable values:

```python
# Written via write_file (long lines):
DISPATCH_J_DIR = "/rootfiles/indigo/commons/journals/ocas-dispatch/2026-06-30"
#     ↑ WRONG: "<hermes-home>/profiles/..." was split at ~80 chars

PRAXIS_EVAL = "<hermes-home>/profiles/indigo/commons/data/ocas-praxis/journals_evalPRAXIS_EVAL = "<hermes-home>/profiles/indigo/commons/data/ocas-prauated.jsonl"
#                                                 ↑ WRONG: two assignments merged into one line
```

**Symptom:** `SyntaxError: unterminated string literal` or `FileNotFoundError` for a path that looks almost correct.

**Fix:** For Python scripts >30 lines, use `write_file` to write to `/tmp/script.py` then run with `python3 /tmp/script.py`. The tool's JSON/YAML linting may catch rewrites for short files, but Python line-wrapping is silent. Better: for any file content with long strings (paths, URLs, heredocs), prefer `write_file` with explicit short lines, or use `terminal()` with `cat > /tmp/file << 'EOF'` (no line wrapping in heredoc body).

**Rule:** After writing Python via `write_file`, always run `python3 -c "import py_compile; py_compile.compile('/tmp/script.py', doraise=True)"` before running it. A 5-second compile check catches line-wrapping corruption.

### Avoid `execute_code` in cron

`execute_code` is blocked in cron mode. Use `python3 << 'PYEOF'` heredoc inside `terminal()` instead.

### Epoch timestamp calculation (use datetime, never manual math)

```python
# CORRECT — always use datetime for epoch timestamps
from datetime import datetime, timezone
cutoff = datetime(2026, 6, 27, 0, 0, 0, tzinfo=timezone.utc).timestamp()

# CORRECT — parse from state file
last_ingest_dt = datetime.fromisoformat(state["last_ingest_run"].replace("Z", "+00:00"))
cutoff = last_ingest_dt.timestamp()

# WRONG — manual epoch math (off by hours/days)
cutoff = 1782873600  # ← wrong! this is June 28, not June 27
```

Manual epoch calculations are a confirmed source of silent failures: the gap scan finds 0 gaps because the cutoff is shifted by a day. Confirmed 2026-06-28T03:12Z — used `1782873600` (June 28) instead of `1782518400` (June 27), missing 412 real gaps on the first pass.

**Heredoc nesting pitfall (confirmed 2026-06-27):** When a bash script contains MULTIPLE heredocs (e.g., an outer `cat > file << 'EOF'` that contains an inner `python3 << 'PYEOF'`), the inner `PYEOF` marker can be consumed by the outer heredoc if the outer heredoc's terminator appears on a line that looks like the inner terminator. More commonly, if you use `python3 << 'PYEOF'` inside a larger `terminal()` call that also uses heredoc syntax, the outer shell sees the inner `PYEOF` as its own EOF terminator.

**Symptoms:** The script silently skips the Python block, or `bash: line N: PYEOF: command not found` appears.

**Fix:** Use `write_file` to write the Python script to `/tmp/`, then invoke it with `python3 /tmp/script.py`. This avoids all heredoc nesting issues. If you must use heredocs, ensure the outer and inner terminators are unambiguously different (e.g., `OUTEREOF` vs `INNEREOF`) and the inner heredoc is in a separate `terminal()` call.

### printf variable path mangling

When writing JSON to eval files via `terminal()`, avoid embedding path variables in `printf` content that matches the redirect target. If `$VAR` is set to `<fs-root>/.../ocas-praxis/file` and then used in `printf '...' >> "$VAR"`, bash can lose track of variable boundaries in complex multi-statement calls, truncating the path (e.g., `<fs-root>/.../ocas-`).

**Fix:** Use `write_file` (tool) + `python3` with `pathli(json, open(path, 'a'))` for appending. If shell append is required:
1. Set variable in one call
2. Use with explicit quoting in a **separate simple** `terminal()` call (no complex embedding)
3. Verify target with `ls -la` before appending

**Confirmed 2026-06-29 dispatch:** Eval file path was truncated to `commons/data/ocas-` (missing `praxis/journals_evaluated.jsonl`). Fixed by switching to python `open(fpath, 'a')`.

### f-strings in `terminal()` 

Never use Python f-strings with `{}` inside `terminal()` — bash `${}` expansion consumes the braces. Use string concatenation or `write_file` + `python3 /tmp/script.py`.

**Praxis-in-eval but NOT-dispatch-in-eval registration (confirmed 2026-06-30T08:40Z):** When the dispatcher detects a journal that IS in the praxis eval file but NOT in the dispatch eval file, it has already been content-evaluated by the Praxis cron pipeline. This is NOT a second-wave — the journal genuinely needs dispatch eval registration. However, since it's already content-evaluated, do NOT re-run the 3-pipeline workflow. Just register in dispatch eval directly. **Classification:** `mixed_genuine_no_op` (genuine dispatch eval gap, but routine content). **Post-dispatch cleanup:** Always run the mtime-based gap scan — a concurrent Praxis cron may have written the dispatcher's `new_file` eval entry AND also written its own output journal (which won't be self-registered until the next Praxis cron run). The 7-second window between `last_ingest_run` (08:36:48) and the praxis-cron output (08:36:56) is a real gap pattern at steady-state.

**Inline Python Typo Pitfalls (confirmed 2026-06-30T10:35Z)**

When writing multi-step inline Python via `terminal()` heredoc, three specific typos have bitten this pipeline:

1. **Truncated dict key** — Writing `state_count'] = line_count` instead of `state['journals_evaluated_count'] = line_count`. The missing `['journals_` prefix produces a SyntaxError that aborts the script mid-run (after the gap detection succeeded but before the counter was updated). **Fix**: Compose the full key path carefully, or use a local variable: `key = 'journals_evaluated_count'; state[key] = line_count`.

2. **`from datetime import datetime` shadowing** — When the script uses `from datetime import datetime, timezone`, the name `datetime` refers to the CLASS. A subsequent call to `datetime.now(timezone.utc)` works. But if the file also has `import datetime` at the top (for `datetime.timedelta` etc.), then `datetime` refers to the MODULE in scope resolution, and `datetime.now(...)` raises `AttributeError: module 'datetime' has no attribute 'now'`. **Fix**: Never use both `import datetime` and `from datetime import datetime` in the same script. If you need both module and class, alias one: `import datetime as dt` + `from datetime import datetime, timezone`, then use `datetime.now()` (class) and `dt.timedelta()` (module).

3. **Dict double-assignment typo (confirmed 2026-06-30T10:35Z)** — Writing `state["last_ingest_run"] =["journals_evaluated_count"] = value` attempting to update two dict keys on one line. Python parses `["journals_evaluated_count"]` as the *first assignment target* (a list literal), which is unassignable → `SyntaxError: cannot assign to literal`. **Fix**: Always use one assignment per line for dict key updates:
   ```python
   state["last_ingest_run"] = now_iso
   state["journals_evaluated_count"] = state.get("journals_evaluated_count", 0) + N
   ```
   This is distinct from typo #1 (missing bracket prefix) — here the issue is chained `=` on dict keys, which Python doesn't support. **Prevention**: Never compose multiple assignments on one line when any target is a dict key or attribute access.

**Rule**: Inline Python for dispatch cleanup should be short (<30 lines), use only `from datetime import datetime, timezone` (never bare `import datetime`), use local variables for repeated dict keys to avoid truncation typos, and write one assignment per line for dict key updates.

## Session References

| File | When to read |
|------|-------------|
| `references/session-20260714-dispatch-1240Z-forge.md` | **Dispatch 2026-07-14T12:40Z:** Explicit-run override fires even when named `new_file` already evaluated — a NEW post-prior-wave cron heartbeat (`mentor-light-20260714T124039Z.json`) appeared after the prior recovery closed, requiring the full pipeline + bridge. Two pitfalls: (1) malformed dispatch-wave filename from truncated `TS` (`dispatch-wave-20260714T1244.json`); (2) legacy bare-filename eval entries (12,712) are NOT phantoms — they predate the `ocas-skill/YYYY-MM-DD/` path convention and must not be "cleaned" during a routine wave. |
|------|-------------|
| `references/session-20260630-dispatch-1035Z-forge.md` | **Dispatch 2026-06-30T10:35Z:** Mixed genuine no-op. Dict double-assignment typo (`state["key1"] =["key2"] = value` → SyntaxError). Praxis-cron with `events_recorded: 1` (all no_signal) correctly classified as no-op via `not_activity_reason`. Eval file: 48,940. |
| `references/session-20260630-dispatch-1020Z-forge.md` | **Dispatch 2026-06-30T10:20Z:** Second-wave no-op. All 4 new_files already in praxis eval cron ahead: last_ingest_run > detected_at). Concurrent dispatch wave registered all in dispatch eval between our checks. 2 concurrent cron gaps backfilled. **`write_file` line-wrapping pitfall** — long Python lines silently split mid-token. Eval file: 48,932. |
| `references/session-20260630-dispatch-0934Z-forge.md` | **Dispatch 2026-06-30T09:34Z:** Complete second-wave with prior-wave dispatch-wave artifact. Both new_files already in praxis eval but NOT in dispatch eval → register dispatch eval only. `run_dispatch_pipeline.py` broken on Python 3.14 (`nargs='[]'`). Praxis-cron double-Z timestamp bug confirmed still active. Post-dispatch cleanup caught 2 concurrent cron gaps. Eval file: 48,916. |
| `references/session-20260630-dispatch-0840Z-forge.md` | **Dispatch 2026-06-30T08:40Z:** Second-wave registration. Journal in praxis eval but NOT in dispatch eval → register in dispatch eval only. Praxis-cron concurrent gap (post last_ingest_run, pre detected_at) → register in praxis eval. Inline Python typo pitfall (`state_count` truncation, `from datetime import datetime` shadowing). Eval file: 48,899. Steady-state. |...
| `references/session-20260629-dispatch-1355Z-forge.md` | **Dispatch 2026-06-29T13:55Z:** Mixed genuine no-op. Dual eval file bridge — dispatch-wave artifact in praxis eval but NOT dispatch eval (recurring pattern confirmed). 1 routine mentor-light (self-referencing, entities_observed=['..']) → genuine-no-op shortcut. Email: Ollama GLM-5.2 newsletter (informational, no action). No pipeline skills loaded. Eval file: 48,531. |
| `references/session-20260626-dispatch-169-forge.md` | **Dispatch #169 (2026-06-26T14:22Z):** Eval file deduplication (50k→40k entries), relpath CWD base fix, datetime module shadowing pitfall. |
| `references/session-20260626-dispatch-168-forge.md` | **Dispatch #168 (2026-06-26T13:43Z):** Mixed genuine no-op, email re-detection wave 35+, eval file path clarification. |
| `references/session-20260626-dispatch-167-forge.md` | **Dispatch #167 (2026-06-26T13:25Z):** Mixed genuine no-op, email high-frequency re-detection + journal second-wave + cron gap. |
| `references/session-20260626-dispatch-166-forge.md` | **Dispatch #166 (2026-06-26T13:24Z):** Massive legacy eval backfill (11,231 entries), email re-detection, mixed no-op dispatch. |
| `references/session-20260626-dispatch-wave-second-wave-path-fix.md` | Before writing eval entries — path base pitfall and second-wave no-op pattern |
| `references/session-20260626-dispatch-2101-forge.md` | **Dispatch ~#2101 (2026-06-26T21:01Z):** Mixed genuine no-op + GitGuardian security alert flagged. Post-dispatch gap #4 (before-ingest cron gap) caught. Security alerts in informational batches — known limitation. |
| `references/session-20260627-dispatch-151554-forge.md` | **Dispatch ~#151554 (2026-06-27T15:10Z):** Multi-skill pipeline. 3 eval gaps backfilled, 3 dispatch-output journals written. Key confirmation: dispatch-wave journals do NOT need eval registration — only non-dispatch journals (mentor-light, praxis-cron, forge-scan) need eval tracking. |
| `references/session-20260627-dispatch-154315Z-forge.md` | **Dispatch ~#154315Z (2026-06-27T15:43Z):** Mixed no-op. Email second-wave (all is_new=false, state file authoritative). Gap scan found 1 routine mentor-light cron journal → registered in eval, no pipeline skills loaded. dispatch-wave journal NOT registered in eval (own output artifact). Confirms steady-state mixed no-op pattern. |
| `references/session-20260627-dispatch-20260627T165958Z-forge.md` | **Dispatch ~#20260627T165958Z (2026-06-27T16:59Z):** Mixed genuine no-op. Prior-wave dispatch-wave re-detected (dispatch-wave-20260627T165430Z, timestamp before detected_at → skip). 1 routine mentor-light eval gap backfilled. Email: all is_new=false second-wave. No pipeline skills loaded. Confirms prior-wave dispatch-wave skip pattern. |
| `references/session-20260627-dispatch-1740Z-forge.md` | **Dispatch ~#1740 (2026-06-27T17:40Z):** Second-wave + eval gap. Both detected journals already in eval. 1 post-ingest cron gap (mentor-light-174048Z) backfilled. Email: 5 GitGuardian alerts — all known-pattern (commits 6ff5967, 9d285dd, 9b6c052 already in confirmed occurrences table). Near mis-escalation: agent initially escalated before cross-referencing gitguardian-internal-secret-triage.md. Lesson: ALWAYS check confirmed occurrences before escalating security alerts. |
| `references/session-20260627-dispatch-183737Z-forge.md` | **Dispatch ~#183737Z (2026-06-27T18:37Z):** Email-only second-wave. All 5 threads is_new=false (2 self-sent briefings + 3 informational: ChatGPT, Groq, Google ToS). 0 actionable. Journals: 2 new_files already in eval (second-wave). Confirmed email-only second-wave pattern: is_new=false on all threads → skip inbox interaction, update state file, write dispatch-wave journal. |
| `references/session-20260627-dispatch-1843Z-forge.md` | **Dispatch ~#1843 (2026-06-27T18:43Z):** Mixed genuine no-op. 1 eval gap (praxis-cron) + 2 mentor-light gaps backfilled. Email: 1 `is_new: true` thread (Meal Train informational — someone else's meal train dates, 0 actionable) + 5 indigo threads (all second-wave). Key learning: `is_new: true` does NOT always mean actionable — third-party notifications are still no-op. No pipeline skills loaded. |
| `references/session-20260627-dispatch-192514Z-forge.md` | **Dispatch ~#192514 (2026-06-27T19:20Z):** Mixed genuine no-op. 3 eval gaps (1 praxis-cron: 0 events + 2 mentor-light: 1 entry each) backfilled. Email: second-wave (6 threads all is_new=false). No pipeline skills loaded per genuine no-op shortcut. Eval file: 40,706 entries. Confirms multi-gap no-op shortcut: gap count >1 still qualifies when all content routine. |
| `references/session-20260627-dispatch-1940Z-forge.md` | **Dispatch ~#1940 (2026-06-27T19:40Z):** Genuine dispatch + email second-wave. Timestamp mismatch pitfall: third-wave mitigation eval entries used `ts_str` from step 1, but journal filenames from step 2 had different timestamps → 3 eval entries didn't match actual filenames. Fix: compose timestamp ONCE before all file operations. Also: 5 eval gaps backfilled (4 mentor-light cron + 1 praxis-cron), 3 dispatch-output journals. Email: all is_new=false second-wave, no new work. |
| `references/session-20260627-dispatch-2114Z-forge.md` | **Dispatch ~#2114 (2026-06-27T21:14Z):** Genuine no-op. 6 eval gaps (5 dispatcher-detected + 1 post-dispatch cron gap). All content routine. Email second-wave (6 threads, all is_new=false, 0 actionable). Dispatch-wave journal erroneously registered in eval during post-dispatch cleanup → corrected (removed entry, decremented state counter). **Lesson: post-dispatch cleanup must NEVER register dispatch-wave journals in eval — even os.walk finds them.** No pipeline skills loaded. |
| `references/session-20260627-dispatch-2145Z-forge.md` | **Dispatch ~#2145 (2026-06-27T21:45Z):** Full pipeline execution, 0 gaps. Key finding: Praxis ingest script auto-registers dispatch-wave journals from prior waves (action_taken: no_signal_noise). Pipeline guide's "NEVER register dispatch-wave" rule applies to MANUAL registration by the agent — the ingest script's auto-evaluation is correct behavior. Counter drift: journals_evaluated_count needs final `wc -l` sync. Eval file: 40,782 entries, steady-state confirmed. |
| `references/session-20260627-dispatch-2150Z-forge.md` | **Dispatch ~#2150 (2026-06-27T21:50Z):** Second-wave + 2 eval gaps. State file schema pitfall: `dispatch_wave` is a timestamp string, not an integer counter — `int()` cast crashes with ValueError. Mixed types in state file (int counters vs timestamp strings). 3 pipeline no-op journals written, third-wave mitigation applied. Eval file: 40,788 entries. |
| `references/session-20260627-dispatch-2218Z-forge.md` | **Dispatch ~#2218Z (2026-06-27T22:18Z):** Genuine full pipeline dispatch. 2 eval gaps (mentor-light-220725Z before-ingest + mentor-light-221059Z post-ingest), both with new_entries > 0 → full 3-pipeline execution. Cross-step timestamp mismatch incident: praxis-dispatch journal written with one timestamp but eval entry used a different one from a second `datetime.now()` call. Caught by post-write verification. Eval file: 40,812 entries. |
| `references/session-20260627-dispatch-2320Z-forge.md` | **Dispatch ~#2320Z (2026-06-27T23:20Z):** Full pipeline, 2 routine mentor-light already in eval. Cross-directory relpath false positive in gap backfill: 120+ commons journals appeared as "missing" due to `../../../../commons/j...` paths from `os.path.relpath`. Fixed by filename-only grep. Eval file: 40,854 entries. |
| `references/session-20260627-dispatch-233646Z-forge.md` | **Dispatch @23:36Z (2026-06-27T23:36Z):** Second-wave with explicit pipeline prompt. Wrote `forge-scan-*.json` journals incorrectly — should have written `dispatch-wave-*.json` only. Key rule: second-wave = no pipeline-specific journals from agent; pipeline scripts keep canonical journal writing. |
| `references/session-20260628-prior-wave-dispatch-wave-skip.md` | **Prior-wave dispatch-wave skip rule** — timestamp < detected_at → skip entirely |
| `references/session-20260628-dispatch-005942Z-forge.md` | **Dispatch @00:59Z (2026-06-28T00:59Z):** Complete second-wave — all 3 journal new_files either in eval (2) or prior-wave dispatch-wave artifact (1, skipped). Email: 2 threads both is_new=false. 0 eval gaps registered, 0 pipeline skills loaded. Confirms complete second-wave pattern: when both journals and email are pure re-detection, classification="second-wave" with 0 eval entries. |
| `references/session-20260628-dispatch-000544Z-forge.md` | **Dispatch 2026-06-28T00:05Z:** Genuine no-op. Self-referencing Mentor heartbeat exception: `mentor-light-000623Z` had `new_entries: 5` but `entities_observed: [".."]` confirmed self-counting. 3 routine gaps (custodian light-scan: 0 new errors, praxis-cron: 0 events, mentor-light: self-referencing). Email: 2 informational threads (Cloudflare 82% limit, One Medical follow-up is_new=false). No pipeline skills loaded. Eval file: 40,875 entries. |
| `references/session-20260628-dispatch-005248Z-forge.md` | **Dispatch 2026-06-28T00:52Z:** Genuine no-op with count accuracy pitfall. 4 new_files → 3 NOT in eval, 1 already in eval. Initial pass registered only 3/4 (missed `mentor-light-004620Z` which was NOT in eval). Post-write verification grep caught the gap. **Lesson:** After initial eval registration, ALWAYS re-grep every `new_file` against eval to confirm all are registered. Also: dispatch-wave journal initially said "3 eval gaps" but should say "4 new_files processed". **Wrong-file edit pitfall:** When updating dispatch-wave journal counts, accidentally edited a different wave's file (`dispatch-wave-003457Z` instead of `005248Z`). **Lesson:** Verify the exact filename in the `run_id` field before editing any dispatch-wave journal from a prior wave. |
| `references/session-20260628-dispatch-0312Z-forge.md` | **Dispatch 2026-06-28T03:12Z:** Stale state backlog backfill. 412 eval gaps registered (state was 2 days stale). Epoch timestamp miscalculation pitfall (used wrong cutoff, found 0 gaps on first pass). All content routine — genuine no-op after backfill. |
| `references/session-20260628-dispatch-0835Z-forge.md` | **Dispatch 2026-06-28T08:35Z:** Second-wave where agent incorrectly wrote forge-scan/mentor-light/praxis-dispatch journals before classification. Classification-first ordering pitfall — classify BEFORE writing any journals. Corrected by removing pipeline journals, writing only dispatch-wave. |
| `references/session-20260628-dispatch-0954Z-forge.md` | **Dispatch 2026-06-28T09:54Z:** Genuine no-op with mixed pre/post-ingest gaps. Dispatcher `new_files` BEFORE `last_ingest_run` (invisible to gap scan) + gap scan found journal AFTER `last_ingest_run`. Both genuine gaps. Fidelity email: informational, action:none. Prior-wave dispatch-wave artifact correctly skipped. |
| `references/session-20260628-dispatch-161654Z-forge.md` | **Dispatch 2026-06-28T16:16Z:** Mixed genuine no-op. Email: all 6 owner + 1 indigo threads `is_new: false` (second-wave). Journals: `mentor-light-160608Z` already in praxis eval (evaluated 16:07), `praxis-cron-160849Z` NOT in praxis eval (genuine gap). Praxis-cron journal was routine no-op (4 no_signal events, 0 gaps, 3 active shifts healthy). Added praxis-cron to both eval files, wrote dispatch-wave journal with classification `mixed_genuine_no_op`. Key: check BOTH praxis eval file AND dispatch eval file — a journal can be in one but not the other. |
| `references/session-20260629-dispatch-0005Z-forge.md` | **Dispatch 2026-06-29T00:05Z:** Second-wave no-op. All 3 new_files already in praxis eval. 1 eval gap backfilled (post-ingest cron gap: mentor-light-000525Z). Mentor correction 8→22 (confirmation #50+). Forge clean (0 unprocessed). Third-wave: 4 eval entries added. Key: dispatch only checked praxis eval — prompted Step 0/Step 1 dual-eval-file check in guide. |
| `references/session-20260629-dispatch-0157Z-forge.md` | **Dispatch 2026-06-29T01:57Z:** Second-wave no-op. Both dispatcher new_files already in eval. Forge: 0 unprocessed (11 total, all processed). 3 post-dispatch cron gap entries added. Streamlined no-op: classified first, skipped all pipeline skills, 4 terminal() calls total. Eval file: 42, |
| `references/session-20260629-dispatch-0240Z-forge.md` | **Dispatch 2026-06-29T02:40Z:** Mixed genuine no-op. Prior-wave artifact skipped, 1 cron gap backfilled. printf variable path mangling pitfall: eval file path truncated to `ocas-` boundary in complex shell call. Fixed by switching to python `open(fpath, 'a')`. Eval file: 48,193. |
| `references/session-20260629-dispatch-0245Z-forge.md` | **Dispatch 2026-06-29T02:45Z:** Complete second-wave. Prior-wave `dispatch-wave-024251Z` had mtime AFTER `last_ingest_run` (gap-scan-visible) but timestamp BEFORE `detected_at` (prior-wave artifact). Confirms: dispatch-wave artifact exclusion uses timestamp comparison, not mtime. 1 self-referencing mentor-light gap registered. Eval file: 48,194. |
| `references/session-20260629-dispatch-0440Z-forge.md` | **Dispatch 2026-06-29T04:40Z:** Genuine dispatch. Prior-wave dispatch-wave artifact skipped. Dispatcher new_file vs heartbeat output divergence: `mentor-light-043547Z` (dispatcher's new_file) ≠ `mentor-light-044551Z` (heartbeat's output) — both needed eval registration but third-wave only caught #2. Caught by post-verification grep. Forge clean. Mentor correction 8→22. Eval file: 48,259. |
| `references/session-20260629-dispatch-0513Z-forge.md` | **Dispatch 2026-06-29T05:13Z:** Genuine full pipeline. 2 eval gaps (rally weekend research + praxis-cron). Classification-first, dual eval check, prior-wave skip, new_file/heartbeat divergence all confirmed working. Mentor correction 8→22 (confirmation #51+). Eval file: 48,276. Steady-state confirmation #56+. |
| `references/session-20260629-dispatch-0614Z-forge.md` | **Dispatch 2026-06-29T06:14Z:** Mixed genuine no-op. 2 prior-wave dispatch-wave artifacts registered in dispatch eval only (refined rule: skip praxis content-eval but register in dispatch eval to prevent re-detection). 1 routine mentor-light (self-referencing: entities_observed=['..']) → genuine-no-op shortcut. Post-dispatch cleanup caught 1 cron gap. Eval file: 48,3| `references/session-20260629-dispatch-063929Z-forge.md` | **Dispatch 2026-06-29T06:39Z:** Mixed genuine no-op. State file already current from concurrent Praxis cron — skipped state write. Post-dispatch cleanup caught 1 cron gap (mentor-light-063616Z). Duplicate eval entry created and deduped. Eval file: 48,315. |
| references/session-20260629-dispatch-0716Z-forge.md | **Dispatch 2026-06-29T07:16Z:** Genuine full pipeline. 1 pre-ingest gap (mentor-light-070943Z before last_ingest_run). Phantom `.json` files encountered in gap scan (correctly filtered). Mentor correction 8→22. Eval file: 48,332. |
| references/session-20260629-dispatch-0748Z-forge.md | **Dispatch 2026-06-29T07:48Z:** Mixed genuine no-op. Prior-wave dispatch-wave artifact registered in dispatch eval only. 1 self-referencing mentor-light gap (entities_observed=['..']) registered. Counter miscount pitfall: registration appended to eval but counter variable undercounted — fixed with post-hoc `wc -l` sync. Key: increment counter for EACH praxis eval append, don't filter by tuple tags. |
| references/session-20260629-dispatch-0912Z-forge.md | **Dispatch 2026-06-29T09:12Z:** Mixed genuine no-op. 1 eval gap (praxis-cron before-ingest pattern #4). Inline eval registration used (no heavy script loading for no-op gaps). Forge clean (no-op journal only). Mentor heartbeat 8→22 (confirmation #52). Third-wave: 1 mentor-light + 1 forge-scan. Post-dispatch: 0 gaps. Eval file: 48,394. Steady-state confirmation #57+. |
| references/session-20260629-dispatch-0926Z-forge.md | **Dispatch 2026-06-29T09:26Z:** Full pipeline. 1 genuine gap (mentor-light-091558Z, self-referencing). Third-wave overlap: concurrent Praxis cron already registered the heartbeat output journal (mentor-light-092426Z) before third-wave ran — 0 third-wave entries needed. Post-dispatch cleanup caught 1 cron gap (mentor-light-092553Z). Mentor 8→22. Eval file: 48,396. |
| references/session-20260629-dispatch-0950Z-forge.md | **Dispatch 2026-06-29T09:50Z:** Genuine full pipeline. 3 new_files (2 second-wave dispatch-wave artifacts + 1 routine mentor-light). Forge clean (0 unprocessed). Mentor 8→22, commons synced. Praxis: 7 journals, 0 genuine events, 13 Bug-2 noise lessons cleaned. Eval file: 48,420. Steady-state confirmation #58+. |
| `references/session-20260629-dispatch-1138Z-forge.md` | **Dispatch 2026-06-29T11:38Z:** Genuine full pipeline. Path typo `oras-praxis`→`ocas-praxis`. Pipe-to-python bash quoting failure. Cross-terminal timestamp divergence. Mentor 8→22. Eval file: 48,469. Steady-state #60+. |
| `references/session-20260629-dispatch-1129Z-forge.md` | **Dispatch 2026-06-29T11:29Z:** Mixed genuine no-op. 2 new_files: 1 prior-wave dispatch-wave artifact (11225Z, registered in dispatch eval only) + 1 concurrent mentor-light (112616Z, routine self-referencing). 1 mtime-discovered gap (our own heartbeat output 112810Z, third-wave mitigated). Forge clean. Mentor 8→22 (confirmation #59+). Post-dispatch cleanup: 0 gaps. Eval file: 48,504. Steady-state confirmation #59+. |
| `references/session-20260629-dispatch-1208Z-forge.md` | **Dispatch 2026-06-29T12:08Z:** Second-wave re-detection with explicit pipeline instructions. All 5 new_files already in praxis eval. Mtime-discovery found 4 gaps (concurrent cron + dispatch output). Forge clean. Mentor 8→22 (confirmation #60+). Praxis: 3 journals, 0 events, 3 third-wave. Gap backfill: 0. Eval file: 48,485. Steady-state #62+. |
| `references/session-20260629-dispatch-1240Z-forge.md` | **Dispatch 2026-06-29T12:40Z:** Mixed genuine no-op + massive legacy backfill. 2/4 new_files missing from eval (cron gap + prior-wave dispatch artifact). One-time backfill of 12,087 legacy journals (pre-eval-tracking, May 13-Jun 26). Email: Ollama newsletter re-detection (already in evidence). Eval file: 48,501→60,590. Steady-state #63+. |
| `references/session-20260629-dispatch-1355Z-forge.md` | **Dispatch 2026-06-29T13:55Z:** Mixed genuine no-op. Dual eval file bridge — dispatch-wave artifact in praxis eval but NOT dispatch eval (recurring pattern confirmed). 1 routine mentor-light (self-referencing, entities_observed=['..']) → genuine-no-op shortcut. Email: Ollama GLM-5.2 newsletter (informational, no action). No pipeline skills loaded. Eval file: 48,531. |
| `references/session-20260714-dispatch-1459Z-redetection-closure.md` | **Dispatch 2026-07-14T14:59Z:** Re-detection closure of a concurrent sibling wave. A newer dispatch-wave (145500Z, timestamp > detected_at) already processed the same new_files + triaged the Kyra Jones thread — current wave did closure-only (no pipeline re-run, no new wave journal). Stale `last_ingest_run` (14:41:05 despite claimed state_updated:true) was the re-fire root cause; advanced to 14:59:20. Residual mentor-cron heartbeat 145549Z bridged via `bridge_eval_both_stores.py`. Email state file fixed (bridge script never touches it). GENUINE GAP=0. |

### Genuine No-Op Count Accuracy (confirmed 2026-06-28T00:52Z)

When registering `new_files` in eval during a genuine no-op dispatch, the count in the dispatch-wave journal's `actions_taken.journals.eval_gaps_registered` MUST equal the number of `new_files` the dispatcher provided that were NOT previously in eval — not the number of "newly discovered" gap scan files, not a mental subtraction of "already in eval" files.

**Pitfall sequence (this session):**
1. Dispatcher reports 4 `new_files`
2. Initial grep shows 3 NOT in eval, 1 already in eval
3. Agent registers only the 3 not-in-eval files
4. Agent writes dispatch-wave journal saying "3 eval gaps"
5. Post-write verification grep reveals the 4th file (`mentor-light-*`) was also NOT in eval — missed because the agent treated "1 already in eval" as "all handled"
6. Agent must go back and register the 4th file, then update the journal count

**Root cause:** The agent mentally subtracted the "already in eval" file from the total count, but the eval check is per-file — each `new_file` must be independently verified AND registered. A file already in eval was correctly tracked; the 4th file was NOT in eval but looked like it should be (similar name to the one already in eval).

**Rule:** Register EVERY `new_file` that is not in eval. After appending, grep ALL `new_files` against eval to confirm:
```bash
for nf in "${new_files[@]}"; do
    grep -qF "$nf" "$EVAL_FILE" && echo "OK $nf" || echo "MISSING: $nf"
done
```

**Dispatcher new_file vs heartbeat output divergence (confirmed 2026-06-29T04:40Z):** When a dispatch triggers a Mentor heartbeat, two mentor-light journals exist: (1) the dispatcher's `new_file` (e.g., `mentor-light-043547Z`) and (2) the heartbeat's fresh output (e.g., `mentor-light-044551Z`). Third-wave mitigation registers #2 but can miss #1 since it's a different file. The divergence occurs because the heartbeat writes a NEW journal with its own timestamp rather than updating the dispatcher's `new_file`. **Fix:** After third-wave mitigation, ALWAYS re-grep each dispatcher `new_file` against eval. Register any missing ones with `action_taken: "dispatch_new_journal_registration"`. Do NOT assume the heartbeat's output covers the dispatcher's input — they are distinct files with distinct timestamps. Confirmed: `mentor-light-043547Z` missed on first pass, caught by verification grep.

**Wrong-file edit prevention:** When editing any previously-written journal file (e.g., to correct counts), verify the `run_id` field contains the current dispatch's timestamp BEFORE editing. A `dispatch-wave-*.json` file from a prior wave will have a different timestamp in its filename and `run_id` — do not edit it. Read the file first, check `run_id`, only then edit.