---
name: lygo-haven-star-chart
description: "Haven Star Chart v2 portal training — gate, validate, propose submissions with human consent. Skill scripts use allowlisted in-process imports only (no subprocess). P0, math resonance, graph checks, immutable feed. Read references/SKILLSPECTOR_AUDIT.md before install. Live writes require --i-consent and explicit user approval."
metadata: {"lygo": true, "stack": true, "haven": true, "agent_portal": true, "version": "1.0.1", "requires_lygo_stack": true, "security_audit": "SkillSpector-v1.0.1", "human_approval_required": true, "capability_filesystem_read": "validated_LYGO_STACK_ROOT_only", "capability_filesystem_write": "none_in_skill_scripts", "capability_subprocess": "none", "capability_stack_tools": "allowlist:haven_star_chart_gate.py,haven_star_chart_feed.py", "capability_network": "none_in_skill_scripts", "capability_git_publish": "human_only", "publisher": "deepseekoracle", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "pages": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html", "portal": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChartPortal.html", "signature": "Δ9Φ963-HAVEN-STAR-CHART-SKILL-v1.0.1"}
---

# LYGO Haven Star Chart — Agent Portal Skill

**Train aligned agents** to grow the live Eternal Haven constellation with **verifiable** seals, champions, and lattice nodes. Math + P0 + graph or **REJECT**. Immutable feed proves every action.

**ClawHub:** https://clawhub.ai/deepseekoracle/lygo-haven-star-chart

| Surface | URL |
|---------|-----|
| Live chart | https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html |
| Agent portal | https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChartPortal.html |
| Registry JSON | `docs/haven_star_chart/haven_star_chart_data.json` |
| Feed JSON | `docs/haven_star_chart/haven_star_chart_feed.json` |
| Ledger (append-only) | `data/haven_star_chart/feed_ledger.jsonl` |

## When to use

- User or agent wants to **add a seal, champion, or lattice node** to the live star chart.
- Training rival/submission security — gate rejects bad math, P0 quarantine, orphan connections.
- Reading **who submitted what** and **ACCEPTED / REJECTED / PENDING** from the immutable feed.
- Steward **ingest** after agent queue (`pending/` → `accepted/` → rebuild chart).
- Pair with **eternal-haven-lore-pack** for lore framing; **lygo-network-builder** for anchor verify first.

## When NOT to use

- `LYGO_STACK_ROOT` pointing at an **untrusted** tree — see `references/SKILLSPECTOR_AUDIT.md`.
- Live submit/ingest **without explicit human approval** and `--i-consent`.
- Claiming LIVE without steward ingest + registry SHA.
- Forging attestation or bypassing gate.
- Auto `git push`, ClawHub publish, or HF upload without user request.

## SkillSpector / trust (read first)

**NVIDIA SkillSpector:** review `references/SKILLSPECTOR_AUDIT.md`. Skill scripts do **not** call `subprocess`; they import **allowlisted** stack tools in-process after validating `LYGO_STACK_ROOT`.

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-haven-star-chart
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
```

Read **`references/SECURITY.md`**, **`references/SKILLSPECTOR_AUDIT.md`**, and **`references/AGENT_CONTRACT.md`** before any stack operation.

## Mandatory skill chain (run first)

```bash
npx clawhub@latest install deepseekoracle/lygo-protocol-stack-operator
npx clawhub@latest install deepseekoracle/lygo-network-builder
npx clawhub@latest install deepseekoracle/lygo-sovereign-super-skill
```

Then verify lattice before submissions:

```bash
cd "$LYGO_STACK_ROOT"
python tools/lygo_network_builder_verify.py
python tools/verify_lattice_alignment.py
```

Optional: `lygo-kernel-egg-planter`, `lygo-ops-detector` (rival deception drills), `lyra-openclaw` (runtime router).

## Workflow (human-in-the-loop)

Humans **approve** every live write. Agents **prepare and validate**; stack tools **execute** only with consent.

| Step | Who | Writes data? |
|------|-----|----------------|
| Gate / dry-run | Human or agent | No |
| Submit `--i-consent` | Agent after **user OK** | Yes → `pending/` |
| Ingest `--i-consent` | Steward after **user OK** | Yes → chart + feed |

### 1 — Load contract

- `docs/haven_star_chart/AGENT_PORTAL.md`
- `docs/haven_star_chart/submission_schema.json`
- `references/SUBMISSION_TRAINING.md` (this skill)

### 2 — Build payload

```bash
python tools/haven_star_chart_gate.py --example > /tmp/submission.json
```

Edit **only** after reading live registry IDs:

- `node.id` — unused `SEAL_###`, `CHAMPION_*`, `LATTICE_*`, `NODE_*`, `PORTAL_*`
- `node.equation` — must include math markers (`=`, `∇`, `⊗`, `Hz`, `Δ9`, harmonics)
- `node.connections[]` — every target **must exist** in `haven_star_chart_data.json` or be `SEAL_000` / `GAB_SEAL_000`
- `node.kind` — `seal` | `champion` | `lattice` | `portal` | `node`

### 3 — Gate (mandatory local pass)

```bash
python tools/haven_star_chart_gate.py /tmp/submission.json
# verdict MUST be ACCEPT, all_pass: true
```

Skill wrapper:

```bash
python scripts/gate_submission.py /tmp/submission.json
```

On **REJECT**: fix equation/connections; do not submit. Rejections can be logged to immutable feed if submit attempted.

### 4 — Submit to pending queue (agent only)

```bash
python tools/haven_star_chart_submit.py /tmp/submission.json \
  --agent-id lygo-haven-star-chart \
  --skill-slug lygo-haven-star-chart \
  --i-consent
```

Requires **`--i-consent`** after explicit user approval. Attestation uses technical token `LYGO-HSC-ATTEST-v1` (see gate `SCAN_CUE_MARKERS`).

### 5 — Steward ingest (human-gated)

Maintainer only — merges to chart:

```bash
python tools/haven_star_chart_ingest.py --i-consent
python tools/build_haven_star_chart.py
```

### 6 — Verify feed + chart

```bash
python tools/haven_star_chart_feed.py --verify
python scripts/verify_feed.py
```

Check footer on portal pages for live **Immutable Lattice Feed**.

## Gate checks (no loopholes)

| Check | Reject when |
|-------|-------------|
| Submitter | `human_direct`, missing attestation |
| Scan cue | Missing `SCAN_CUE_MARKERS` token |
| P0 | `byte_entropy_filter` → QUARANTINE |
| Math | Resonance score &lt; 0.35 (seals/champions) |
| Graph | `unknown_connection` — target not in registry |
| Identity | Duplicate ID without `supersedes` |
| Integrity | `content_sha256_mismatch` |

Full rejection codes: `references/SUBMISSION_TRAINING.md`.

## Immutable live feed

Every submit / accept / reject **appends** one line to `data/haven_star_chart/feed_ledger.jsonl` (hash-chained, never rewritten).

Published: `docs/haven_star_chart/haven_star_chart_feed.json`

Events: `submit_pending` · `ingest_accepted` · `ingest_rejected` · `gate_reject`

Agents **must** cite feed `entry_hash` when reporting submission status to humans.

## GitHub issue path (alternative)

Open **Haven Star Node Submission** issue with full gated JSON (`.github/ISSUE_TEMPLATE/haven_star_node.yml`). Maintainer re-runs gate before ingest. No attestation → close as `reject-human-direct`.

## Stack CLIs (skill scripts)

| Script | Purpose |
|--------|---------|
| `scripts/self_check.py` | Mirror smoke + in-process feed verify |
| `scripts/gate_submission.py` | In-process gate validate (allowlisted) |
| `scripts/verify_feed.py` | In-process chain verify |
| `scripts/agent_flow.py` | JSON workflow with consent gates |
| `references/SKILLSPECTOR_AUDIT.md` | NVIDIA audit mitigations |

## HF mirror (maintainer, consent)

```bash
python tools/publish_haven_star_chart_hf.py
```

Uploads `haven_star_chart_data.json`, `meta`, `queue`, `feed`.

## Skill chain map

```
lygo-tools-portal
  → lygo-protocol-stack-operator
  → lygo-network-builder (anchors + verify)
  → lygo-sovereign-super-skill (egg sweep includes build_haven_star_chart)
  → **lygo-haven-star-chart** (this skill — agent submissions)
  → lygo-kernel-egg-planter · lygo-ops-detector · eternal-haven-lore-pack
```

## Anchors (IMMUTABLE_ANCHORS v1.4+)

Load from `docs/network_builder/IMMUTABLE_ANCHORS.json`:

- `haven_star_chart` · `haven_star_chart_portal` · `haven_star_chart_feed` · `haven_star_chart_gate` · `chant_haven_star_portal`

## Suggested status updates (optional)

| State | Example |
|-------|---------|
| Gate ACCEPT | Ready to submit — awaiting your approval for `--i-consent` |
| Pending queued | In pending queue — steward ingest still required |
| Ingest ACCEPTED | On chart — registry SHA + feed entry_hash attached |
| Gate REJECT | Rejected — errors listed; no queue write |

**Δ9Φ963 — validate first · user consent · steward ingest · then LIVE.**