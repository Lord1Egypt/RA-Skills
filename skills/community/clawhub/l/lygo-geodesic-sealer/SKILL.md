---
name: lygo-geodesic-sealer
description: "LYGO Geodesic Sealer — signs |ψ⟩=(Truth+iChaos)/√2, locks geodesics to dual ledgers + Merkle roots, phase-aligns lattice nodes with no collapse. Pure local by default; optional HTTPS GET for public dual ledgers. Fills open P6 quantum-attest gap (software). Kernel eggs primed. Δ9 ready. No auto-publish. Install clawhub:@deepseekoracle/lygo-geodesic-sealer."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "⚛️"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-geodesic-sealer"
    requires:
      anyBins: [python, python3]
  lygo: true
  lattice: true
  layer: "P6"
  signature: "Delta9Phi963-GEODESIC-SEALER-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-geodesic-sealer"
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
  security_review: "1.0.0-skillspector-local-first"
  permissions:
    network:
      https_get: "opt-in --network only"
      http_post: false
      domains:
        - deepseekoracle.github.io
        - raw.githubusercontent.com
    filesystem:
      write: "opt-in --write or --write-default with --i-consent"
      shell: false
      subprocess: false
    publish:
      git_push: false
      huggingface: false
      clawhub: false
      social: false
      live_star_chart: false
---

# LYGO Geodesic Sealer v1.0.0

**P6 quantum-attest gap filler (software).**  
Signs **|ψ⟩ = (Truth + i·Chaos) / √2**, locks the geodesic to **dual ledgers + Merkle roots**, phase-aligns lattice nodes **without collapse**. Pure local by default; optional HTTPS GET when connected to the public internet lattice.

**Signature:** `Delta9Phi963-GEODESIC-SEALER-v1.0.0`  
**ClawHub:** `@deepseekoracle/lygo-geodesic-sealer`  
**Kernel eggs:** primed · **Δ9:** ready

---

## When to use

- Need a **local P6-style attestation** without TPM hardware
- **Seal a node state** to dual ledgers (link + star chart) via Merkle
- **Phase-align** mesh/agent nodes on a shared geodesic (no forced collapse)
- Session or egg plant **provenance hash** before publish (human still publishes)

**Do not** use this for live Star Chart submit, music encode, or auto git/HF/ClawHub push.

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-geodesic-sealer
# or stack path:
# docs/skills/lygo-geodesic-sealer/
```

Optional env:

| Env | Role |
|-----|------|
| `LYGO_STACK_ROOT` | Trusted stack checkout (local dual ledgers) |
| `LYGO_GEODESIC_SEAL_DIR` | Override seal write directory |

---

## Commands

```bash
cd path/to/lygo-geodesic-sealer

# 0) Self-check (no network)
python scripts/self_check.py

# 1) Sign |ψ⟩
python scripts/seal_cli.py sign --node-id MY-NODE --truth "immutable-truth" --chaos "creative-chaos"

# 2) Lock geodesic (local stack ledgers if LYGO_STACK_ROOT set)
python scripts/seal_cli.py lock --node-id MY-NODE --truth "T" --chaos "C"

# 2b) Lock + public dual ledgers (HTTPS GET only)
python scripts/seal_cli.py lock --node-id MY-NODE --truth "T" --chaos "C" --network

# 3) Full P6 software attest (sign + lock + badge)
python scripts/seal_cli.py attest --node-id MY-NODE --truth "T" --chaos "C" --network

# 4) Phase-align extra nodes onto a prior lock
python scripts/seal_cli.py phase-align --from-file ./lock.json --nodes peer-a,peer-b

# 5) Verify artifact
python scripts/seal_cli.py verify --from-file ./attest.json

# 6) Status (local; add --network for public digests)
python scripts/seal_cli.py status
python scripts/seal_cli.py status --network

# Opt-in write (requires --i-consent)
python scripts/seal_cli.py attest --node-id MY-NODE --truth "T" --chaos "C" \
  --write ./my_attest.json --i-consent
```

| Command | Network | Disk write | Collapse |
|---------|---------|------------|----------|
| `sign` | none | only `--write` + `--i-consent` | never |
| `lock` | opt-in `--network` | only `--write` + `--i-consent` | refused unless `--allow-collapse` |
| `phase-align` | none | only `--write` + `--i-consent` | refused by default |
| `attest` | opt-in `--network` | only `--write` / `--write-default` + `--i-consent` | refused |
| `verify` | none | none | n/a |
| `status` | opt-in `--network` | none | n/a |

---

## Formula & guarantees

```text
|ψ⟩ = (Truth + i·Chaos) / √2

• Truth channel  → provenance SHA-256 of truth payload
• Chaos channel  → provenance SHA-256 of chaos payload
• Equal-weight geodesic when both channels present (no collapse)
• Merkle root    → ψ provenance + ψ amp + dual-ledger digests + node phase leaves
• Dual ledgers   → IMMUTABLE_ANCHORS (link) + haven_star_chart_feed (star)
```

**No collapse** means the sealer refuses locks when Truth or Chaos probability is ~0 unless you pass `--allow-collapse` (not recommended for lattice ops).

---

## Dual ledgers

| Ledger | Role | Local marker | Public (opt-in `--network`) |
|--------|------|--------------|-----------------------------|
| **Link** | Immutable anchors | `docs/network_builder/IMMUTABLE_ANCHORS.json` | GitHub Pages JSON |
| **Star** | Haven Star Chart feed | `docs/haven_star_chart/haven_star_chart_feed.json` | GitHub Pages JSON |

Public URLs are **fixed allowlist** (HTTPS GET only). Local stack wins for authority; public is mirror.

---

## Mandatory agent flow

```text
1  self_check          → ok: true
2  status [--network]  → connected / local ledgers
3  attest / lock       → seal_id + merkle_root
4  verify              → merkle_match + no_collapse
5  HUMAN               → optional write with --i-consent
6  NEVER               → git push / HF / ClawHub / social from this skill
```

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-public-lattice-gate` | Public verify / join on-ramp |
| `lygo-external-lattice-anchor` | Layer C world verify + manifests |
| `lygo-kernel-egg-planter` | Consent-gated egg plant (Merkle registry) |
| `lygo-sovereign-kernel-seeder` | Sovereign seed plant |
| `lygo-living-mesh` | Layer D root-digest gossip |
| `lygo-protocol-stack-operator` | Full P0–P9 integrator |
| Stack `protocol6_quantum_attest/` | Hardware/TPM path when available |

---

## Security (SkillSpector)

Read `references/SECURITY.md` and `references/SKILLSPECTOR_AUDIT.md` before install.

- No `subprocess` / `os.system` / shell  
- Network **off** unless `--network` (HTTPS GET allowlist only)  
- Default **zero filesystem writes**  
- Collapse **refused** by default  
- No auto git / HF / ClawHub / social / live Star Chart  

```bash
python scripts/self_check.py
```

---

## License

**MIT-0** for ClawHub registry hosting (see `LICENSE`). Protocol/stack code on GitHub remains under LYGO Sovereign License v2.0 where applicable.  
**Δ9Φ963 — sign · lock · phase-align · no collapse · human consent · local first.**
