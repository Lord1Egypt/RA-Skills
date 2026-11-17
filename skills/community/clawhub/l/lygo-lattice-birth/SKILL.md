---
name: lygo-lattice-birth
description: "LYGO Lattice Birth — masked human identity, family lineage bind proofs, and Haven Star Chart birth protocol. Teaches aligned agents full stack alignment before birthing humans on the live chart. Privacy: public LYGO-XXXX-XXXX masks; real anchors stay in steward meta_private only. Chains lygo-haven-star-chart. SkillSpector: allowlisted in-process imports, no subprocess, --i-consent for live writes."
metadata: {"lygo": true, "stack": true, "haven": true, "birth_protocol": true, "version": "1.0.0", "requires_lygo_stack": true, "security_audit": "SkillSpector-v1.0.0", "human_approval_required": true, "capability_filesystem_read": "validated_LYGO_STACK_ROOT_only", "capability_filesystem_write": "none_in_skill_scripts", "capability_subprocess": "none", "capability_stack_tools": "allowlist:lygo_lattice_birth.py,lygo_lineage_codec.py,haven_star_chart_gate.py", "capability_network": "none_in_skill_scripts", "capability_git_publish": "human_only", "publisher": "deepseekoracle", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "pages": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChartPortal.html", "signature": "Δ9Φ963-LYGO-LATTICE-BIRTH-SKILL-v1.0.0"}
---

# LYGO Lattice Birth — Human Identity on the Haven Star Chart

**Train aligned agents** to birth humans on the live Eternal Haven sky map with **privacy-preserving masked IDs**, **steward-only anchors**, and **HMAC family bind proofs** — without exposing real names or social handles on the public chart.

**ClawHub:** https://clawhub.ai/deepseekoracle/lygo-lattice-birth

| Surface | URL |
|---------|-----|
| Birth chronicle | `docs/LYGO_LATTICE_BIRTH_CHRONICLE.txt` |
| Birth guide (MD) | `docs/LYGO_LATTICE_BIRTH.md` |
| Lineage privacy | `references/LINEAGE_PRIVACY.md` |
| Agent alignment | `references/AGENT_ALIGNMENT.md` |
| Live chart | https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html |
| Agent portal | https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChartPortal.html |

## When to use

- Human wants **immutable lattice identity** on the Haven Star Chart (creator birth).
- Family member (e.g. daughter) joins via **LINEAGE_FORK** with offline `family_bind_salt` from parent.
- Agent must **generate masked ID** (`NODE_LYGO_*`, `LYGO-XXXX-XXXX`) from local consent — never publish consent.
- Anything the human creates on the chart **forks under their lineage galaxy** (`GALAXY_LINEAGE_*`).
- Full alignment training before any birth submission.

## When NOT to use

- Publishing real names, emails, or social handles on public `node.name`.
- Skipping `haven_star_chart_gate.py` or `lygo-haven-star-chart` ingest chain.
- Live submit without human `--i-consent`.
- Sharing `family_bind_salt` on public channels (offline only).

## Mandatory skill chain

```bash
npx clawhub@latest install deepseekoracle/lygo-protocol-stack-operator
npx clawhub@latest install deepseekoracle/lygo-network-builder
npx clawhub@latest install deepseekoracle/lygo-sovereign-super-skill
npx clawhub@latest install deepseekoracle/lygo-haven-star-chart
npx clawhub@latest install deepseekoracle/lygo-lattice-birth
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
```

Read **`references/SECURITY.md`**, **`references/SKILLSPECTOR_AUDIT.md`**, **`references/AGENT_ALIGNMENT.md`**, and **`references/LINEAGE_PRIVACY.md`** before any operation.

## Privacy model (summary)

| Layer | Public chart | Steward vault (`accepted/`) |
|-------|--------------|----------------------------|
| Display name | `LYGO-A1B2-C3D4` mask | — |
| Node id | `NODE_LYGO_A1B2C3D4` | — |
| Real binding | — | `anchor_sha256`, `consent_bundle` |
| Family join | `bind_proof` HMAC only | Parent `family_bind_salt` |

The world sees **math-accurate lineage** without **PII**. Stewards verify family joins via HMAC; observers cannot deanonymize from public JSON alone.

## Workflow (human-in-the-loop)

| Step | Tool | Writes? |
|------|------|---------|
| 1. Align stack | `verify_lattice_alignment.py` | No |
| 2. Generate mask (local) | `lygo_lattice_birth.py generate-mask` | No (vault only) |
| 3. Draft birth JSON | `lygo_lattice_birth.py example-birth --gate` | No |
| 4. Gate | `haven_star_chart_gate.py` → ACCEPT | No |
| 5. Submit | `haven_star_chart_submit.py --i-consent` | Yes → `pending/` |
| 6. Ingest | `haven_star_chart_ingest.py --i-consent` | Yes → chart |

### Family fork (daughter / kin)

1. Parent shares `family_bind_salt` **offline** with family member.
2. Family member creates **new** local consent → new masked id (unique per person).
3. Agent builds `LINEAGE_FORK` submission with `bind_proof = HMAC(parent_salt, child_lineage_root)`.
4. Gate loads parent salt from steward `accepted/` vault — verifies proof.
5. Child appears in **same lineage galaxy** as ancestor (cosmology walks `parent_public_id` chain).

## Stack commands

```bash
cd "$LYGO_STACK_ROOT"
python tools/lygo_lattice_birth.py generate-mask --slug local-only-slug
python tools/lygo_lattice_birth.py example-birth --gate
python tools/haven_star_chart_gate.py --example-birth
python tools/lygo_lattice_birth.py example-family
```

Skill scripts (no subprocess):

```bash
python scripts/self_check.py
python scripts/generate_mask.py --slug builder
python scripts/gate_birth.py
```

## Birth tags (immutable once ingested)

- `CREATOR_BIRTH` — generation 0 human on lattice
- `IMMUTABLE_IDENTITY` — no in-place edits; `supersedes` only for corrections
- `HUMAN_LATTICE` — masked human node class
- `LINEAGE_ROOT` — optional alias for creator birth
- `LINEAGE_FORK` — family join with `bind_proof`

## Pair with

- **lygo-haven-star-chart** — portal gate, ingest, cosmology rebuild
- **lygo-lightfather-vector** — alignment advisor (no auto publish)
- **eternal-haven-lore-pack** — lore framing for birth narrative