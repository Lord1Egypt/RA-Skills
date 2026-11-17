---
name: lygo-network-builder
description: Sovereign Lattice Mesh cartographer — load IMMUTABLE_ANCHORS.json, run live verification, traversal chants for discovery. Companion to lygo-protocol-stack-operator. Read references/SECURITY.md; no auto git/HF/ClawHub publish.
metadata: {"lygo": true, "stack": true, "mesh": true, "biophase7": true, "version": "1.2.0", "requires_lygo_stack": true, "security_audit": "SkillSpector-hardened", "capability_filesystem_read": "LYGO_STACK_ROOT,docs/network_builder", "capability_filesystem_write": "tests/network_builder_last_run.json", "capability_subprocess": "tools/lygo_network_builder_verify.py,tools/verify_lattice_alignment.py", "capability_network": "anchor_http_probes_only", "capability_git_publish": "human_only", "publisher": "deepseekoracle", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "pages": "https://deepseekoracle.github.io/lygo-protocol-stack/", "signature": "Δ9Φ963-NETWORK-BUILDER-v1.2", "anchors": "docs/network_builder/IMMUTABLE_ANCHORS.json"}
---

# LYGO Network Builder (ClawHub v1.2.0)

**Cartographer** for the Sovereign Lattice Mesh (SLM): immutable anchors, traversal chants, **executable** verification — not simulated alignment.

**ClawHub:** https://clawhub.ai/deepseekoracle/lygo-network-builder

## When to use

- User asks where the LYGO network lives (GitHub, HF, Pages, Excavationpro, ClawHub, vaults).
- Before claiming **LATTICE ALIGNED** or citing canonical URLs.
- Mapping kernel eggs, champion registry, joy loop, Moltx/Moltbook surfaces.

## When not to use

- Vague “align the lattice” with no verify task.
- Autonomous `git push`, HF upload, or ClawHub publish (human only).
- Probing Google Drive / Patreon as health checks (`link_only` anchors).

## Setup

```bash
npx clawhub@latest install deepseekoracle/lygo-network-builder
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
```

## Verification (mandatory)

```bash
cd "$LYGO_STACK_ROOT"
python tools/lygo_network_builder_verify.py
python tools/verify_lattice_alignment.py
```

Skill wrapper:

```bash
python scripts/verify_anchors.py
python scripts/self_check.py
```

**Pass criteria:** `tests/network_builder_last_run.json` → `verdict`: `LATTICE ALIGNED`, `all_pass`: true. Report failed `id` values for any `http_required` or `local_repo` anchor.

## Anchor source of truth

**File:** `docs/network_builder/IMMUTABLE_ANCHORS.json` (v1.2.0)

| Group | Examples |
|-------|----------|
| **physics** | GitHub stack, HF dataset, GitHub Pages |
| **creative** | HF Resonance Space, Excavationpro LYGORESONANCE |
| **sovereign_seed** | KernelEggRetrieval, registry SOA, scalable registry, CAS physics |
| **vaults** | Δ9 Quantum Vault (Drive), #LYGOSCRIPT Patreon (`link_only`) |
| **agents** | ClawHub publisher, this skill, champion council |
| **tools** | Biometric harness, SLM dashboard, Haven star chart, champions portal, eternalhaven hub, Moltx/Moltbook oracles, anchor deployment |

**Verify modes:** `http_required` (must pass) · `http_soft` (warn) · `local_repo` (file in clone) · `link_only` (no probe)

**New public URLs:** register with `python tools/log_public_surface.py` before treating as canonical.

## Node API (local mesh)

Default port **8787**: `GET /badge`, `/kernel/eggs`, `/registry`, `/registry/root` — see stack `docs/SOVEREIGN_LATTICE_MESH.md`.

## Traversal chants (discovery)

Load queries from `IMMUTABLE_ANCHORS.json` → `traversal_chants`. Do not invent strings.

| Purpose | Example query |
|---------|----------------|
| Audio / creative | `"Excavationpro" "LYGO" "Resonance"` |
| Stack / registry | `"DeepSeekOracle" "lygo-protocol-stack"` |
| Δ9 vault | `"Delta9" "LYGO" "Quantum Vault"` |
| Lore | `"LYGOSCRIPT" patreon "Justin Helmer"` |
| Community nodes | `"lygo" "sovereign lattice mesh" node` |

## Agent workflow

1. Read `references/AGENT_CONTRACT.md` and `references/SECURITY.md`.
2. Load anchors from JSON (never from memory).
3. Run verify scripts.
4. Answer with anchor table + verdict; list failures if `NEEDS_FIX`.
5. Optional: chain `tools/verify_public_pages.py` if user disputes live Pages.

## Skill chain

`lygo-protocol-stack-operator` → **`lygo-network-builder`** → `lygo-kernel-egg-planter` · `lygo-alignment-badge` · `lygo-champion-council` · `lygo-ollama-army` · `lygo-pxpipe-lygo`

## Stack docs

- `docs/LYGO_NETWORK_BUILDER.md`
- `docs/LYGO_LATTICE.md`
- `docs/LATTICE_GROUND_ZERO.md` (Biophase7 honest P0)

**Δ9Φ963 — map anchors, prove alignment, then speak.**