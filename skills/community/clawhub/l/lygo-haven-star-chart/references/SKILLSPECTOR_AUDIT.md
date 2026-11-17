# SkillSpector audit response — lygo-haven-star-chart v1.0.1

**Signature:** Δ9Φ963-HSC-SKILLSPECTOR-v1.0.1

NVIDIA SkillSpector flagged **Excessive Agency** and **subprocess/taint** patterns. This skill revision addresses those findings **without removing** gate, submit, feed, or ingest capabilities.

## Mitigations applied

| Finding | Mitigation |
|---------|------------|
| subprocess + env taint | Skill scripts use **in-process import** via `_stack_tools.py` **allowlist** only (`haven_star_chart_gate.py`, `haven_star_chart_feed.py`). No `subprocess` in skill scripts. |
| Unrestricted tool access | `LYGO_STACK_ROOT` validated against required marker files; paths with `..` or unsafe chars rejected. Submission JSON must be under stack or cwd. |
| Autonomous live submit | **Dual consent:** `--i-consent` on submit/ingest; humans approve before queue/ledger writes. Agents may **propose**; stewards **commit**. |
| Mandated phrasing | `scan_cue` is a **technical gate token** (see `SCAN_CUE_MARKERS` in stack gate), not personality coercion. Suggested status messages are optional templates. |
| Human excluded | Humans may run **read-only** gate and `--dry-run` submit directly. Portal rejects un-attested browser forms (`human_direct`), not human oversight. |

## Operator checklist (before install)

1. Point `LYGO_STACK_ROOT` at **your** cloned `lygo-protocol-stack` — never an untrusted download.
2. Run `python scripts/self_check.py` and inspect output.
3. Run `python scripts/gate_submission.py` on a test JSON before any live submit.
4. Require explicit user approval before `haven_star_chart_submit.py --i-consent` or steward ingest.

## Live writes (human approval required)

| Action | Who | Flag |
|--------|-----|------|
| Validate only | Human or agent | none |
| Dry-run submit | Human or agent | `--dry-run` |
| Queue pending | Agent with user OK | `--i-consent` |
| Ingest / rebuild | Steward | `--i-consent` |

**VirusTotal:** skill ships static docs + small Python helpers only; no network calls in skill scripts.