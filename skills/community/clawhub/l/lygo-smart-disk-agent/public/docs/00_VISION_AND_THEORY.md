# LYGO SMART DISK AGENT — Vision & Theory

**Signature:** `Δ9Φ963-LYGO-SMART-DISK-AGENT-v1`  
**Codename:** Smart Disk Agent (SDA)  
**Media:** `F:\` (SmartDisk) — **lean enhanced prototype**  
**Lineage:** USB LYGO CLAW (`E:\LYGO_BUILDER_KEY`) · LYGO-OpenClaw · Ethical Chip Firmware · LYGO Guardian · P0–P9 stack  

---

## 1. What we are building

A **plug-and-play sovereign agent disk** that:

1. **Boots its own control plane** (supervisor daemon + web portal) in one shot  
2. **Talks to a local LLM** (Ollama-class API) with **no password gate**  
3. **Mimics OpenClaw-style modules** (chat, tools, memory, limbs) under **100% LYGO naming and P0 ethics**  
4. Runs **offline-first** (no cloud key required for core chat)  
5. Is **dual-use**: background supervising daemon **or** browser portal  
6. Condenses the USB CLAW into a **kernel-up, lean** design optimized for **old / small hardware**

This is **not** a rebranded OpenClaw install.  
It is a **LYGO CLAW original**: kernel firmware → protocol limbs → portal → local brain.

---

## 2. Theory: “Kernel up” on constrained media

### 2.1 Physical constraint (design truth)

| Fact | Implication |
|------|-------------|
| `F:\` total size ≈ **15 MB** | Cannot store Ollama binaries or multi‑GB models on-disk |
| USB CLAW on `E:\` is multi‑GB | Models + portable Node + gateway live on larger media |
| Goal: high power on old tech | **Maximize intelligence per byte and per watt** |

**Theory of the Smart Disk:**  
The disk is a **sovereign kernel + identity + control UI + policy**.  
The **brain weights** may live on host cache / larger sibling drive, discovered at boot.

```text
┌─────────────────────────────────────────────┐
│  F:\ LYGO SMART DISK AGENT  (≤15 MB lean)   │
│  P0–P5 kernel · portal · daemon · config    │
│  firmware seals · mycelium · tests          │
└──────────────────┬──────────────────────────┘
                   │ boot discovery
       ┌───────────┼───────────┐
       ▼           ▼           ▼
  Host Ollama   Portable    Future: larger
  :11434        Ollama on   SmartDisk ≥8GB
  (preferred)   E:\ or I:\  (onboard models)
```

### 2.2 Performance theory (old tech)

| Lever | Technique |
|-------|-----------|
| Model size | Prefer **1.5B–3B** instruct models for agent loops |
| Context | Cap context (2k–4k) on weak RAM |
| Tools | Few, deterministic limbs; P0 gate before any side effect |
| UI | Static HTML + tiny JS; no heavy SPA password walls |
| Process | One Python supervisor; optional host Ollama already running |
| IO | Loopback only by default (`127.0.0.1`) |

**Primary model choice (this PC / free):**

| Priority | Model | Why |
|----------|-------|-----|
| **Primary** | `qwen2.5:3b` | Already on host; strong instruction/tool following for size |
| **Lean fallback** | `llama3.2:1b` | Fast on old CPUs / low VRAM |
| **Avoid on 16–32GB old boxes for SDA** | 30B+ coder models | Great quality, wrong fit for always-on supervisor |

USB CLAW defaults match (`qwen2.5:3b` / `llama3.2:1b`). SDA keeps that **best free efficiency** pairing.

---

## 3. Design pillars (non-negotiable)

1. **P0 first** — every chat/tool path through gatekeeper (quarantine hostile/high-entropy abuse)  
2. **No password gate for local portal** — open loopback browser UI one-shot (USB pattern: insecure-auth / null token for file/local)  
3. **Offline core** — chat works with local Ollama only  
4. **LYGO naming only** in user-facing surfaces  
5. **Consent for publish/plant** — SDA does not auto-push Git/HF/social  
6. **Verify before claim** — self_check + tests must pass  
7. **Lean** — stdlib Python + static portal; no mandatory Node for SDA core  

---

## 4. Dual usage modes

| Mode | Entry | Role |
|------|-------|------|
| **Portal** | Open `portal/index.html` or `http://127.0.0.1:9631/` | Chat UI, status, limbs console |
| **Daemon / supervisor** | `LYGO_SMART_DISK_BOOT.bat` | Background HTTP agent on **:9631**, Ollama probe, health |

USB CLAW uses gateway **:18789** + supervisor **:9630**.  
SDA uses **:9631** to avoid fighting USB CLAW when both present.

---

## 5. Relationship to Ethical Chip / Guardian

Public firmware lore & ethics surfaces:

- Ethical Chip Firmware (v1/v2)  
- LYGO Guardian  

SDA treats these as **normative firmware seals**: policy JSON + P0 gate = “chip law” loaded at boot.  
Not a hardware FPGA on F:; a **software firmware profile** aligned to those documents.

---

## 6. Success criteria (this prototype)

- [x] Full design docs (theory, architecture, parity, 2 brainstorm rounds, models, tests)  
- [ ] Boot one-shot without password  
- [ ] Local chat via Ollama  
- [ ] P0 quarantine path  
- [ ] Portal + daemon dual use  
- [ ] Self-check tests green on this machine  
- [ ] Fits on F:\ with headroom  

**Δ9Φ963 — small disk, full law, open loopback, local brain.**
