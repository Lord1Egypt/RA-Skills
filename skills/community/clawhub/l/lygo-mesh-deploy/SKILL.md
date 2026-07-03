---
name: lygo-mesh-deploy
description: LYGO mesh deploy — Phase 5 epidemic gossip, SLM Merkle/mycelium/consensus routes, Phase 9 TLS HTTPS node API. Local cluster scripts + pin gossip before wide-area.
metadata: {"lygo": true, "stack": true, "phase": 5, "slm": true, "phase9": true, "version": "1.0.1", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "pages": "https://deepseekoracle.github.io/lygo-protocol-stack/", "signature": "Δ9Φ963-PHASE9-PUBLIC-MESH"}
---

# lygo-mesh-deploy

**Phase 5** wide-area mesh tooling (local HTTP proof before TLS wide-area).

## When to use

- Prove epidemic badge gossip converges in **&lt;20 rounds** (live) or **&lt;10 rounds** (sim).
- Operate community mesh alongside Docker `lygo-node` on **8787**.

## Commands

```bash
git clone https://github.com/DeepSeekOracle/lygo-protocol-stack.git
cd lygo-protocol-stack

# Stochastic proof (100 nodes, no HTTP)
python tools/run_mesh_scale_sim.py --nodes 100 --fanout 2 --no-pause

# Live HTTP cluster (Linux/macOS)
./tools/deploy_100_nodes.sh
python tools/monitor_convergence.py --nodes 100 --wait-health 180
python tools/deploy_mesh_cluster.py stop

# Windows
pwsh tools/deploy_100_nodes.ps1
python tools/monitor_convergence.py
```

## Node API (per peer)

| Method | Path |
|--------|------|
| GET | `/badge`, `/gossip`, `/health`, `/gossip/root`, `/slm/snapshot`, `/cert/pin` |
| POST | `/gossip/badge`, `/gossip/scatter`, `/gossip/sync`, `/gossip/pin`, `/mycelium/store`, `/consensus/vote` |

HTTPS (Phase 9):

```bash
python tools/tls_manager.py --generate
python tools/node_api_server.py --tls --port 8443
```

## Safety

- Public internet: use **TLS + pin gossip** (`docs/PHASE9_DEPLOYMENT_GUIDE.md`); operator sign-off required.
- No autonomous wide-area deploy without explicit operator sign-off.

**Install:** `npx clawhub@latest install deepseekoracle/lygo-mesh-deploy`