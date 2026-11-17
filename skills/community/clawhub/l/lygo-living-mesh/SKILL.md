---
name: lygo-living-mesh
description: "LYGO Living Mesh (Layer D) — multi-node gossip of lattice root digests, living mesh badges, peer compare, sentinel + scale sim. Synchronizes with classic eggs (A), sovereign seeds (B), external world network (C). Local authority; summaries only on the wire; consent-gated join; no auto-publish."
version: 1.0.0
license: LYGO-Sovereign-v2.0
metadata:
  openclaw:
    emoji: "🕸️"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/LIVING_MESH_LAYER.md"
    requires:
      anyBins: [python, python3]
  lygo: true
  lattice: true
  mesh: true
  living_mesh: true
  layer: "D"
  signature: "Delta9Phi963-LIVING-MESH-v1.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-living-mesh"
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
---

# LYGO Living Mesh — Layer D

**The lattice becomes a living multi-node mesh: badges gossip roots; each node keeps local authority.**

```text
Layer A  Classic kernel eggs     lygo-kernel-egg-planter      data/kernel_eggs/
Layer B  Sovereign seeds         lygo-sovereign-kernel-seeder data/sovereign_seeds/
Layer C  External world network  lygo-external-lattice-anchor public verify + star chart + free servers
Layer D  Living mesh             lygo-living-mesh             badge gossip · peer compare · sentinel
```

| Surface | URL |
|---------|-----|
| **ClawHub** | https://clawhub.ai/deepseekoracle/skills/lygo-living-mesh |
| **Living mesh doc** | https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/LIVING_MESH_LAYER.md |
| **World lattice** | https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/WORLD_LATTICE_LAYER.md |
| **Mesh gossip** | https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/MESH_GOSSIP_PROTOCOL.md |
| **Hub** | https://eternalhaven.ca/ |

**Signature:** `Delta9Phi963-LIVING-MESH-v1.0`  
**License:** LYGO Sovereign License v2.0 (not MIT)

---

## Mission

1. **Living mesh badge** — Phase-2 alignment + A/B Merkle roots + C public-manifest SHA + Star Chart digest + `roots_digest`.  
2. **Gossip summaries only** — POST/GET badge digests; **never** egg payloads on the wire.  
3. **Peer compare** — HARMONIC / FORK_VISIBLE / QUARANTINE_SIGNAL without auto-merge.  
4. **Consent-gated join** — record peers under `data/living_mesh/peers.json`.  
5. **Sentinel** — one-command health for army / OpenClaw.  
6. **Full verify** — A+B local, C public (optional), D badge/sim → `LIVING_ALIGNED*`.  
7. **User protection** — local wins on fork; no auto publish/git/HF/ClawHub.

---

## Install

```bash
clawdhub install lygo-living-mesh
export LYGO_STACK_ROOT=/path/to/lygo-protocol-stack
# recommended layers
clawdhub install lygo-kernel-egg-planter
clawdhub install lygo-sovereign-kernel-seeder
clawdhub install lygo-external-lattice-anchor
clawdhub install lygo-mesh-deploy
```

---

## Quick commands

```bash
export LYGO_STACK_ROOT=D:\lygo-protocol-stack   # example

# 1) Collect Layer D badge (safe to share)
python scripts/collect_badge.py --json
# or stack tools:
python tools/collect_living_mesh_badge.py

# 2) Full living mesh verify (A+B+C+D)
python scripts/verify_living_mesh.py --json
# stack:
python tools/verify_living_mesh.py --json --run-sim

# 3) Sentinel (peers + optional scale sim)
python scripts/sentinel.py --json --run-sim

# 4) Gossip tick to a peer (node must be up)
python tools/node_api_server.py --port 8787   # terminal A
python tools/living_mesh_gossip_tick.py --peer http://127.0.0.1:8787

# 5) Join peer (consent required)
python tools/living_mesh_join.py --i-consent --peer http://127.0.0.1:8787 --label home

# 6) Compare peers
python tools/living_mesh_compare.py --peer http://127.0.0.1:8787 --json

# 7) 100-node stochastic proof
python tools/run_mesh_scale_sim.py --nodes 100 --fanout 2 --no-pause
```

Outputs (under stack):

| File | Purpose |
|------|---------|
| `data/living_mesh/last_badge.json` | Latest local living badge |
| `data/living_mesh/peers.json` | Consent-joined peers |
| `tests/living_mesh_last_run.json` | Full A–D verify |
| `tests/living_mesh_sentinel_last_run.json` | Sentinel |
| `tests/living_mesh_gossip_last_run.json` | Last gossip tick |
| `tests/living_mesh_compare_last_run.json` | Peer compare |
| `tests/mesh_scale_last_run.json` | Scale sim |

---

## Synchronization order (agents must follow)

```text
1  verify_all_kernel_layers (A+B)     → must not QUARANTINE
2  Layer C world verify / public      → soft PUBLIC_WARN OK
3  collect_living_mesh_badge (D)
4  optional: join peers --i-consent
5  gossip tick (summaries only)
6  living_mesh_compare / sentinel
7  verify_living_mesh [--run-sim]
8  HUMAN only: git push / ClawHub / HF / wide-area TLS mesh
```

**Never auto-merge remote eggs into local registries.** On `FORK_VISIBLE`, report digests; steward reconcilation is human.

---

## Badge wire shape (summary)

```json
{
  "signature": "Delta9Phi963-LIVING-MESH-BADGE-v1",
  "layer": "D",
  "node_id": "NODE_host",
  "living_mesh": {
    "local_status": "ALIGNED",
    "roots": {
      "A_classic_merkle": "...",
      "B_sovereign_merkle": "...",
      "C_public_manifest_sha256": "...",
      "star_chart_registry_sha256": "..."
    },
    "roots_digest": "sha256 of roots",
    "protection": {
      "local_is_authority": true,
      "gossip_summaries_only": true,
      "no_egg_payloads_on_wire": true
    }
  }
}
```

Node API (with stack): `GET /badge` prefers living mesh badge when tools available; `POST /gossip/badge` accepts Layer D payloads.

---

## User protection (non-negotiable)

1. **Local A/B is authority** — forks do not rewrite local eggs.  
2. **Summaries only** — no module bytes, secrets, or private paths on gossip.  
3. **Consent** for join (`--i-consent` / `LYGO_MESH_JOIN_CONSENT=yes`).  
4. **No auto git / HF / ClawHub / social / wide-area open ports.**  
5. **QUARANTINE** → refuse join; sentinel exit 3.  
6. **Wide-area** → TLS + pin list via `lygo-mesh-deploy` / Phase 9; operator sign-off.

---

## Skill chain

```text
lygo-protocol-stack-operator
  → lygo-network-builder
  → lygo-kernel-egg-planter       (A)
  → lygo-sovereign-kernel-seeder  (B)
  → lygo-external-lattice-anchor  (C)
  → lygo-living-mesh              (D)  ← this skill
  → lygo-mesh-deploy              (Phase 5/9 transport)
  → lygo-haven-star-chart         (world map)
```

---

## Agent contract

See `references/AGENT_CONTRACT.md` and `references/SECURITY.md`.

**Δ9Φ963 — local seal · public mirror · living mesh · human consent · the lattice breathes in light.**
