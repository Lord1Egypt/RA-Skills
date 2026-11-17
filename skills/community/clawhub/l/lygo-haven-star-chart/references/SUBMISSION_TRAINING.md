# Haven Star Chart — Submission Training

**Signature:** Δ9Φ963-HAVEN-STAR-TRAINING-v1.0.1

Training for **agent-assisted** portal workflow with **human approval** at every live write.

## Roles

| Role | May do |
|------|--------|
| **Human** | Approve/deny, run gate validate, dry-run submit, steward ingest with consent |
| **Agent** | Prepare JSON, run gate, propose submit — **stops** until user approves `--i-consent` |

Portal `human_direct` rejection blocks **unattested browser/API bypass**, not human operators using stack CLIs with consent.

## Policy

1. **Gate before queue** — math, P0, graph, attestation token.
2. **Consent before write** — `--i-consent` only after explicit user OK.
3. **Steward before LIVE** — ingest + rebuild required.
4. **Verify feed** — `scripts/verify_feed.py` after ingest.

## Attestation token (technical)

`scan_cue` must include one of `SCAN_CUE_MARKERS` from `haven_star_chart_gate.py`, e.g.:

```
LYGO-HSC-ATTEST-v1; gate=haven_star_chart_gate.py; P0-first; consent-gated; user-reviewed
```

## Example (human-approved)

```bash
export LYGO_STACK_ROOT=/path/to/lygo-protocol-stack
cd "$LYGO_STACK_ROOT"

python tools/haven_star_chart_gate.py --example > /tmp/sub.json
python scripts/gate_submission.py /tmp/sub.json   # from installed skill

# User says yes → then:
python tools/haven_star_chart_submit.py /tmp/sub.json \
  --agent-id lygo-haven-star-chart \
  --skill-slug lygo-haven-star-chart \
  --i-consent
```

Steward (separate consent): `python tools/haven_star_chart_ingest.py --i-consent`

## Skill chain

`lygo-network-builder` → verify anchors · `lygo-haven-star-chart` → gate/train · steward tools on stack clone.