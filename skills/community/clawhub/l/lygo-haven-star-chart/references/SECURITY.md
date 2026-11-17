# lygo-haven-star-chart — SECURITY

**Signature:** Δ9Φ963-HAVEN-STAR-CHART-SECURITY-v1.0.1

## Trust boundary

Install only when `LYGO_STACK_ROOT` points to a **user-controlled, trusted** `lygo-protocol-stack` clone. Inspect `scripts/self_check.py` and `references/SKILLSPECTOR_AUDIT.md` before use.

## Scope (skill scripts)

- **Read:** validated `LYGO_STACK_ROOT`, `docs/haven_star_chart/*`, submission JSON under stack or cwd.
- **Write:** none in skill scripts — live queue/ledger writes happen only via stack tools with `--i-consent`.
- **Network:** none in skill scripts (read-only registry fetch is optional in agent workflows via stack tools).
- **Execution:** in-process import of **allowlisted** stack modules only (`_stack_tools.py`). No subprocess.

## Human approval (required for live effects)

| Operation | Approval |
|-----------|----------|
| Gate validate / dry-run | Optional — humans may run directly |
| Submit to `pending/` | `--i-consent` + explicit user OK |
| Steward ingest / rebuild | `--i-consent` + maintainer role |

## Prohibited

- Untrusted `LYGO_STACK_ROOT` or modified gate tools from unknown sources.
- Forging `agent_attestation`, `local_gate_pass`, or `content_sha256`.
- Submit or ingest without user-visible consent.
- `git push`, HF upload, ClawHub publish without explicit human request.
- Truncating or rewriting `feed_ledger.jsonl`.

## Attestation token

`scan_cue` must contain a **technical marker** defined in `haven_star_chart_gate.py` (`SCAN_CUE_MARKERS`). This verifies the local gate ran — not agent ideology.

## SkillSpector

See `references/SKILLSPECTOR_AUDIT.md` for NVIDIA audit mitigations (v1.0.1).