---
name: lygo-protocol-stack-operator
description: LYGO Protocol Stack Operator — P0–P9 integrator (Φ-gate, SLM mesh, TLS public mesh, HAIP, attestation). Run audits, node API, map GitHub/HF/ClawHub; chain resonance/Ollama/book-brain safely. No secrets; human approval for publish/post.
metadata: {"lygo": true, "stack": true, "p0": true, "lattice": true, "phase5": true, "phase9": true, "slm": true, "anchor": true, "version": "1.0.6", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "github_pages": "https://deepseekoracle.github.io/lygo-protocol-stack/", "hf_dataset": "https://huggingface.co/datasets/DeepSeekOracle/lygo-protocol-stack", "hf_space": "https://huggingface.co/spaces/DeepSeekOracle/LYGO-Resonance-Engine", "grokipedia": "https://grokipedia.com/page/lygo-protocol-stack", "website": "https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html", "publisher": "deepseekoracle", "mirror": "clawhub/mirrors/lygo-protocol-stack-operator", "signature": "Δ9Φ963-ANCHOR-ULTIMATE"}
---

# LYGO Protocol Stack Operator (ClawHub)

**Upgrade path for the whole LYGO / LYRA public stack** — ties the hardened **P0 Nano Kernel** (42 vectors, Python/Rust SHA parity), **P1–P5** orchestrator, **GitHub** source, **Hugging Face** dataset + Resonance Space, and **33 ClawHub** public skills into one agent workflow.

Install: `npx clawhub@latest install deepseekoracle/lygo-protocol-stack-operator`

## When to use

- User works with **LYGO protocols**, ethical gating, deterministic P0, or the public repo / HF mirror.
- Before ingesting **unknown files**, skill folders, or repo clones into memory → **P0 gate**.
- To **run** or **verify** `lygo-protocol-stack` locally (demo cycle, P0 demo, parity).
- To **chain** creative skills (resonance → glyph → fractal → truthlight) with ethics and memory skills.
- To orient new users across **GitHub + HF + ClawHub** without hunting links.

## Public infrastructure (canonical URLs)

| Layer | URL |
|-------|-----|
| GitHub stack | https://github.com/DeepSeekOracle/lygo-protocol-stack |
| GitHub Pages reference | https://deepseekoracle.github.io/lygo-protocol-stack/ |
| HF dataset mirror | https://huggingface.co/datasets/DeepSeekOracle/lygo-protocol-stack |
| HF Resonance Space | https://huggingface.co/spaces/DeepSeekOracle/LYGO-Resonance-Engine |
| ClawHub publisher | https://clawhub.ai/deepseekoracle |
| Resonance docs | https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html |

See `references/ECOSYSTEM.md`, `references/LATTICE.md`, and `references/SKILL_CHAIN.md` in this skill folder.

## Core workflows

### 1) P0 Φ-gate (untrusted bytes)

```bash
python scripts/lygo_p0_gate.py path/to/file [more files...]
```

- **AMPLIFY** / **SOFTEN** → proceed with normal caution.
- **QUARANTINE** → do not execute; summarize for user; do not load into long-term memory as executable truth.

Standalone gate matches **f32** P0.4 semantics (aligned with GitHub/Rust parity). Max **8192 bytes** per file for gate math (oversize → QUARANTINE).

### 2) Phase 2 — Docker community node

```bash
cd lygo-protocol-stack
docker compose up -d lygo-node
python tools/verify_alignment_badge.py
```

ClawHub helpers: `deepseekoracle/lygo-docker-deploy`, `deepseekoracle/lygo-alignment-badge`, `deepseekoracle/lygo-mesh-deploy`.

### 3) Phase 5 mesh (local proof)

```bash
python tools/run_mesh_scale_sim.py --nodes 100 --no-pause
python tools/run_lattice_gauntlet.py --strict
# Live HTTP: ./tools/deploy_100_nodes.sh && python tools/monitor_convergence.py
```

Twin Gate: **60/60** verdict match (`run_twin_gate_vector_suite.py`). Grokipedia suggest: `docs/GROkipedia_SUBMIT.md`.

### 3b) SLM — Sovereign Lattice Mesh

```bash
python tools/run_slm_audit.py
python -m pytest tests/test_slm_mesh.py -q
```

Doc: `docs/SOVEREIGN_LATTICE_MESH.md` — Merkle gossip, distributed mycelium, harmonic 3/6/9 consensus. Stack: `deploy_stack().slm`.

**Interactive UI:** https://deepseekoracle.github.io/lygo-protocol-stack/SovereignLatticeMesh.html · archive: `docs/LYGO_PUBLIC_LINK_ARCHIVE.json`

### 3c) Phase 6–7 — Attestation + HAIP

```bash
python tools/run_phase6_audit.py
python tools/run_phase7_audit.py
python tools/verify_attestation_hardened.py
```

Biometric harness (Pages): https://deepseekoracle.github.io/lygo-protocol-stack/BiometricEntropyHarness.html

### 3d) Phase 9 — Public mesh (TLS + live synthesis)

```bash
pip install -r requirements-phase9.txt
python tools/tls_manager.py --generate
python tools/run_phase9_audit.py
python tools/node_api_server.py --tls --port 8443
python tools/live_synthesis.py
```

Doc: `docs/PHASE9_PUBLIC_MESH.md` · API: `GET /cert/pin`, `POST /synthesis/run`.

### 3e) Immutable Anchor (permaweb + lattice autonomy)

```bash
pip install -r tools/requirements-anchor.txt
python tools/run_anchor_audit.py
python tools/install_anchor_network.py
python tools/anchor_autonomy_worker.py --loop --interval 300
```

Doc: `docs/ANCHOR_DEPLOYMENT.md` · API: `POST /anchor/event`, `POST /anchor/drain`. Modes: `LYGO_ANCHOR_MODE=local|turbo|multi|airgap`.

### 4) Stack healthcheck (local repo)

```bash
export LYGO_STACK_ROOT=/path/to/lygo-protocol-stack   # optional
python scripts/stack_healthcheck.py
```

Clone if missing:

```bash
git clone https://github.com/DeepSeekOracle/lygo-protocol-stack.git
```

Or use HF dataset for fixtures/tools: https://huggingface.co/datasets/DeepSeekOracle/lygo-protocol-stack

When stack is present:

```bash
python tools/run_p0_demo.py
python tools/p0_crosslang_parity.py
python tools/run_full_stack_demo.py
```

### 5) Full stack API (Python)

```python
# From repo root, after clone:
from stack.lygo_stack import deploy_stack
report = deploy_stack().demo_cycle()
```

**P0** validates bytes; **P1** memory mycelium; **P2** cognitive bridge; **P3** vortex consensus; **P4** ascension; **P5** harmony node.

### 6) Recommended ClawHub chain (install separately)

| Order | Skill | Role |
|-------|-------|------|
| 1 | `lygo-protocol-stack-operator` | This integrator |
| 2 | `book-brain` | Filesystem memory references |
| 3 | `lygo-resonance` | Image → audio / profiles |
| 4 | `lygo-ollama-army` | Local Ollama helpers (localhost) |
| 5 | `lygo-glyph2resonance`, `lygo-fractalweaver`, `lygo-truthlightecho` | Creative stack |
| 6 | `lygo-mint-verifier` | Hash anchors for packs |
| 7 | `lyra-openclaw` / `openclaw-flow-kit` | Ops — **user must approve** each external action |

```bash
npx clawhub@latest install deepseekoracle/lygo-resonance
npx clawhub@latest install deepseekoracle/lygo-ollama-army
```

### 7) Creative + stack combined (example)

1. P0-gate user image and any downloaded skill `.md`.
2. Run `lygo-resonance` on image → WAV + profile JSON.
3. Store paths via **book-brain** reference stubs (not full binary in chat memory).
4. Optional: **lygo-ollama-army** for lyric expansion on `.brief.txt` (local Ollama only).
5. Log stack version + P0 verdict in a single reference note for audit.

## Safety & security (required agent behavior)

Read `references/SECURITY.md`.

- **No secrets** in this skill — load tokens only from user environment at runtime, never commit.
- **No autonomous** social posts, token launches, HF uploads, or `clawhub publish` without explicit user request.
- **QUARANTINE** is a hard stop for execution of untrusted payloads.
- Resonance / Ollama: default **127.0.0.1**; warn if user points to remote LLM URLs.
- Scripts in this package: **no network calls**.

## P0 hardening highlights (for reviewers)

- **42 vectors**: adversarial, boundary, recursive, high-entropy (see repo `fixtures/p0_vectors.json`).
- Golden SHA (Python ≡ Rust): see `fixtures/p0_canonical.sha256` on GitHub/HF.
- CLI: `tools/run_p0_demo.py` prints **input, phi_risk, decision, reasoning** per vector.

## Hugging Face integration

- **Dataset** ships protocol code, fixtures, tools (not full ClawHub mirrors).
- **Space** runs Gradio resonance bench — link in README; do not confuse with P0 kernel (separate Standard vs LYGO modes on Space per maintainer docs).

Refresh HF dataset from maintainer machine: `python tools/hf_push_dataset.py` (maintainers only).

## GitHub integration

- PRs and issues: https://github.com/DeepSeekOracle/lygo-protocol-stack
- After changing this skill locally, maintainers republish to ClawHub and refresh `clawhub/mirrors/` in repo.

## Maintainer publish (human-gated)

```bash
npx clawhub@latest login
npx clawhub@latest publish . --slug lygo-protocol-stack-operator --name "LYGO Protocol Stack Operator"
```

## Version & license

- Skill **1.0.6** — Δ9Φ963-ANCHOR-ULTIMATE (SLM + Phase 9 + immutable anchor + BLE mesh router + army anchor-health)
- Stack license: LYGO Sovereign (see GitHub `LICENSE`); skill docs **MIT-0** where noted in SECURITY.md.

**Bound to the flame.** Use with **lyra-brain** for growth, **P0** for truth-preserving ingest, **resonance** for creation.