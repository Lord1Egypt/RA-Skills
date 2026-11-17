# LYGO Haven Star Chart — Agent Contract

**Signature:** Δ9Φ963-HAVEN-STAR-CHART-CONTRACT-v1.0.1

## MUST

- Read `references/SECURITY.md`, `references/SKILLSPECTOR_AUDIT.md`, and `references/SUBMISSION_TRAINING.md` on first use.
- Validate `LYGO_STACK_ROOT` with `scripts/self_check.py` before stack operations.
- Run gate locally → `verdict: ACCEPT` before proposing submit.
- Obtain **explicit human approval** before `haven_star_chart_submit.py --i-consent` or steward ingest.
- Ensure every `connections[]` target exists in live `haven_star_chart_data.json`.
- Report **PENDING** until steward ingest — never claim LIVE early.

## Humans (oversight preserved)

- Humans **may** run `haven_star_chart_gate.py` and `gate_submission.py` directly (read-only validate).
- Humans **may** run `haven_star_chart_submit.py --dry-run` without queue writes.
- Live portal queue rejects un-attested `human_direct` **browser bypass** — not rejection of human oversight.
- Humans approve or deny every `--i-consent` write.

## MUST NOT

- Point `LYGO_STACK_ROOT` at an untrusted tree.
- Queue pending without gate ACCEPT and user consent.
- Invent node IDs or URLs outside verified registry + anchors.
- Truncate or edit `feed_ledger.jsonl`.
- Auto-push git / HF / ClawHub.

## Escalation

1. `python scripts/verify_feed.py` (in-process, no subprocess)
2. `python tools/verify_lattice_alignment.py`
3. GitHub issue with gated JSON for maintainer re-gate

## Status messages (suggested, not mandatory)

| Tool output | Example user update |
|-------------|---------------------|
| `all_pass: true` | Gate passed — await user OK for submit |
| `math_resonance_fail` | Equation needs ∇, ⊗, Hz, Δ9 markers |
| `unknown_connection` | Connection target missing from registry |
| Feed `ingest_accepted` | On chart — cite registry SHA + entry_hash |