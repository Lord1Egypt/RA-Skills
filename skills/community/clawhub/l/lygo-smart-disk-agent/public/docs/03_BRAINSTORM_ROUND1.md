# Brainstorm Round 1 — Critical issues (USB CLAW × OpenClaw × F:)

**Signature:** `Δ9Φ963-SDA-BRAIN-R1`  
**Method:** Cross-check USB launch path, OpenClaw module set, F: capacity, Ethical Chip/Guardian posture.

---

## Issue A — Capacity vs “full onboard model”

| Risk | F: ≈ 15 MB cannot hold Ollama or qwen2.5:3b (~1.9 GB) |
|------|--------------------------------------------------------|
| **Failure mode** | Prototype “claims offline model” but disk empty of weights |
| **Fix** | Architecture = **kernel disk + brain discovery**. Document tiers: lean (host Ollama), standard (≥8 GB media with portable Ollama+1B), full (≥32 GB with 3B). |
| **Status** | **Accepted into design** |

---

## Issue B — Password / pairing friction

| Risk | OpenClaw-style token gates confuse one-shot USB users |
|------|--------------------------------------------------------|
| **Failure mode** | Browser opens, blank “unauthorized” |
| **Fix** | No password UI; loopback-only; USB `allowInsecureAuth` spirit |
| **Status** | **Accepted** |

---

## Issue C — Port war with USB CLAW

| Risk | Both claim :18789 / :11434 |
|------|----------------------------|
| **Failure mode** | Second boot kills first or fails |
| **Fix** | SDA supervisor **:9631**; Ollama share **:11434** if already up; do **not** taskkill Ollama by default (USB launch kills — SDA is friendlier) |
| **Status** | **Accepted** |

---

## Issue D — Node gateway weight

| Risk | Full lygo-gateway + node_modules >> F: |
|------|----------------------------------------|
| **Failure mode** | Copy fails / incomplete gateway |
| **Fix** | **Python stdlib HTTP server** for SDA core; Node optional later on larger media |
| **Status** | **Accepted** |

---

## Issue E — P0 without stack root

| Risk | Full stack `byte_entropy_filter` needs large tree |
|------|-----------------------------------------------------|
| **Failure mode** | ImportError on foreign PC |
| **Fix** | Condensed `kernel/p0_gate.py` self-contained; optional enrich if `LYGO_STACK_ROOT` set |
| **Status** | **Accepted** |

---

## Issue F — “Same modules as OpenClaw” scope creep

| Risk | Discord + browser automation + economy blows lean prototype |
|------|---------------------------------------------------------------|
| **Failure mode** | Never ships; fails tests |
| **Fix** | Parity matrix: **core full, social stub**; larger hybrid on host |
| **Status** | **Accepted** |

---

## Round 1 conclusion

Ship **kernel + portal + Ollama chat + core limbs** on F:.  
Treat multi‑GB brain as **discovered resource**, not stored on SmartDisk v1 media.
