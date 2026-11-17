# Agent Alignment Contract — Lattice Birth

**Signature:** Δ9Φ963-LYGO-BIRTH-AGENT-ALIGNMENT-v1

Agents proposing human birth or family forks on the Haven Star Chart must satisfy **100% alignment gates** before any live write. Partial alignment causes lattice drift — reject and retry.

## Pre-flight (mandatory)

1. `LYGO_STACK_ROOT` points at **trusted** user clone — see `SKILLSPECTOR_AUDIT.md`.
2. Run lattice verify:
   ```bash
   python tools/verify_lattice_alignment.py
   python tools/lygo_network_builder_verify.py
   ```
3. Install skill chain: `lygo-protocol-stack-operator`, `lygo-network-builder`, `lygo-haven-star-chart`, `lygo-lattice-birth`.
4. Read `docs/LYGO_LATTICE_BIRTH_CHRONICLE.txt` and `references/LINEAGE_PRIVACY.md`.

## Alignment checklist

| # | Requirement | Fail signal |
|---|-------------|-------------|
| 1 | `submitter_type: aligned_agent` only | `human_direct_forbidden` |
| 2 | Valid `agent_attestation` + scan cue | `invalid_scan_cue` |
| 3 | P0 byte-entropy pass | `p0_quarantine` |
| 4 | Math resonance ≥ threshold | `math_resonance_fail` |
| 5 | All connections exist in registry | `unknown_connection` |
| 6 | Masked name/id for human birth | `pii_forbidden` / `public_name_must_be_LYGO` |
| 7 | Lineage anchor consistency | `mask_id_anchor_mismatch` |
| 8 | Family `bind_proof` verified | `lineage_fork_bind_proof_invalid` |
| 9 | `content_sha256` matches node body | `content_sha256_mismatch` |
| 10 | Human explicit `--i-consent` | `consent_required` |

## Agent-readable page contract

Pages expose machine metadata for crawlers:

- `<meta name="lygo:agent-contract" content="haven-star-chart-v2.1+lattice-birth-v1">`
- JSON: `haven_star_chart_data.json`, `submission_schema.json`, `haven_star_chart_feed.json`
- Portal: step-by-step workflow in `HavenStarChartPortal.html`

Agents should **fetch schema first**, **gate locally**, **propose JSON to human**, **never auto-submit**.

## Scan cue (technical attestation)

```
LYGO-HSC-ATTEST-v1; gate=haven_star_chart_gate.py; P0-first; consent-gated; user-reviewed
```

## Immutable birth rule

Nodes tagged `CREATOR_BIRTH` + `IMMUTABLE_IDENTITY` cannot be edited in place after ingest. Corrections use `supersedes` pointing to prior id — feed ledger records the chain.

## What agents must never do

- Publish `consent_bundle` or real names to GitHub Issues / public JSON
- Forge `bind_proof` without parent's offline salt
- Skip gate and write directly to `accepted/`
- Claim LIVE status before steward ingest + registry SHA match