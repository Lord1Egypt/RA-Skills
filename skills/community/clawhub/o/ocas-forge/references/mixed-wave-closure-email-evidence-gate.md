# Mixed-Wave Re-Detection Closure — Email Evidence Gate (added 2026-07-17)

## Why this exists
`closure_closeout_check.py` gate [3] reports GREEN when the dispatch-owned
email state files carry `verified_second_wave: True`. That flag is **NOT proof
of work**. Observed 2026-07-14: a prior wave wrote `verified_second_wave: True`
in the state file but `commons/data/ocas-dispatch/evidence.jsonl` held ZERO
records for the dispatch threads — the emails were never actually triaged, yet
the wave looked closed. Closing on the flag alone silently drops genuine email
work forever (re-fire is suppressed once state advances).

## Mandatory pre-close step for ANY mixed-wave closure (new_journals + new_emails)
Before re-affirming `verified_second_wave` or advancing `last_ingest_run` /
monitor `latest_mtime`, verify the evidence store on disk:

```bash
python3 skills/ocas-dispatch/scripts/verify_evidence_threads.py \
    --evidence commons/data/ocas-dispatch/evidence.jsonl \
    <thread_id_1> <thread_id_2> ...
```

Per-thread outcome:
- `in_evidence(structured)  action=none`  -> genuinely triaged, OK to close.
- `in_evidence(structured)` with NO trailing `action=` token -> logged but
  never classified. Treat as a gap: append a structured
  `triage_decisions[].action` record (per `ocas-dispatch`
  `references/cron-triage-workflow.md`), then close.
- `NOT_IN_EVIDENCE` -> genuine Path B gap. Triage the thread fresh from dispatch
  metadata (do NOT skip), then close.

## Authoritative evidence path
`commons/data/ocas-dispatch/evidence.jsonl` — NOT the `owner/` subdir copy
(stale, hours behind) and NOT `commons/data/mentor/evidence.jsonl`
(summary-only, no structured `triage_decisions`). The verifier defaults to the
dispatch-level file.

## Full hard-gate context
See `ocas-dispatch` `references/email-evidence-verification-gap.md` and
`references/cron-triage-workflow.md`. The dispatch skill's rule is absolute:
"a prior wave journal claim of verified_in_evidence is NOT proof — grep
evidence.jsonl before trusting second-wave email classification."

## What the 2026-07-17 closure confirmed
A re-detection fire carried 10 <operator> threads (all `is_new: false`; monitor
heuristically flagged 3 high-priority). The verifier showed all 10 genuinely
present with `action=none` tokens — including the high-priority ones correctly
downgraded on inspection (DoorDash order = transactional confirmation;
Consulting reply = <operator> already responded; Profound screener = cron autonomous
override, non-deadline/legal). The prior wave had truly done the work; the flag
was honest, so advance + close was correct. The gate exists to catch the case
where it ISN'T — never close a mixed wave on the flag alone.

## Worked example — 2026-07-22 13:45Z closure (priority-80 security sign-in)
A re-detection fire carried 14 <operator> threads (all `is_new: false`), including
`<thread-id>` "New sign-in to your OpenAI account" flagged by the monitor
heuristic as `priority: 80` / `intent: action_required`. The thread carried
22 prior evidence lines, all `action: none`. Running `verify_evidence_threads.py`
returned `in_evidence(structured)  action=none` for all 10 wave threads.
Verdict: the downgrade is LEGITIMATE, not a dropped escalation — the sign-in is
ChatGPT iOS from San Francisco (PDT), consistent with <operator>'s own device +
location. Reason recorded in evidence: "security notification; no reply
required." Because the structured `action=none` token is durable in
`evidence.jsonl`, every subsequent re-detection wave re-verifies it and does NOT
re-escalate — this is exactly the false-re-escalation the gate exists to
prevent. Lesson: a provider "new sign-in" notice is a distinct category from a
security-SCAN alert (GitGuardian/Snyk in the dispatch SKILL.md Security Alerts
section); when the access source matches the owner's own device/location,
`action: none` is correct and the gate confirms it.
