# OpenClaw / free claw systems → LYGO SMART DISK parity

**Signature:** `Δ9Φ963-SDA-PARITY-v1`  
**Sources:** USB LYGO CLAW, `lygo_openclaw/`, `lyra-openclaw` skill, OPEN CLAW LEGACY workspace, public OpenClaw-style gateway patterns.

---

## 1. OpenClaw-style capability clusters

| OpenClaw-style module | What it does | USB LYGO CLAW | Smart Disk Agent (lean) |
|----------------------|--------------|---------------|-------------------------|
| **Gateway** | Local agent HTTP/WS control plane | Node `lygo-gateway` :18789 | Python `smart_disk_agent` :9631 |
| **Control UI** | Browser dashboard | `dashboard/` + control-ui | `portal/index.html` one-shot |
| **Auth** | Token / pairing | token + allowInsecureAuth | **No password**; loopback only |
| **Local LLM** | Ollama provider | Portable Ollama + qwen2.5:3b | Host/portable discovery; **qwen2.5:3b / llama3.2:1b** |
| **Agents workspace** | Session files, SOUL/USER md | lygo-claw workspace | `workspace/` + mycelium |
| **Memory** | Daily / long memory | mycelium + lyra | **P1 mycelium** `data/mycelium/` |
| **Tools / skills** | Browser, shell, web, etc. | plugins + hybrid limbs | **Limbs:** help, status, chat, lattice, health, open-url |
| **Browser** | agent-browser LEFT/RIGHT | via hybrid / host | Limb `browser-open` (open default browser to URL) |
| **Cron / heartbeat** | Background pulse | army supervisor | Daemon health loop in agent |
| **Channels** | Discord, etc. | optional host | **Stub limbs** (offline default off) |
| **Doctor / onboarding** | Setup wizards | minimized on USB | **None** (one-shot boot) |
| **Identity** | Agent persona | champions | firmware seal + Lightfather/LYRA system prompts |

---

## 2. Free systems referenced (build-on / learn-from)

| System | License/use | What we take | What we reject |
|--------|-------------|--------------|----------------|
| **OpenClaw / Claw gateway patterns** | Free to run/build locally | Gateway+UI+Ollama provider shape | Vendor branding, password onboarding, cloud defaults |
| **Ollama** | Free local runtime | API shape `/api/chat`, model tags | Shipping multi‑GB models on 15 MB disk |
| **LYGO-OpenClaw (stack)** | Our code | P0/P1/P3/P5 pipeline | Heavy Node dependency for SDA core |
| **USB LYGO CLAW** | Our portable embodiment | Launch sequence, open local UI, model prefs | Full multi‑GB footprint |
| **Ethical Chip / Guardian HTML** | Our public firmware lore | Ethics language, guardian posture | Hardware claims we cannot put on F: |

---

## 3. Limb map (SDA v1)

| Limb | OpenClaw analog | SDA behavior |
|------|-----------------|--------------|
| `help` | help | List limbs + usage |
| `status` | status | Kernel + Ollama + disk |
| `health` | doctor (light) | JSON health, no wizard |
| `chat` | agent message | LLM via Ollama |
| `lattice` | lattice pulse | Local seal + stack pointer status |
| `memory` | memory recall | Last N mycelium events |
| `open-url` | browser open | `webbrowser.open` local only targets preferred |
| `army-sentinel` | army check | Probe Ollama process / tags |

**Deferred (documented, not on 15 MB disk):** Discord, Moltbook, Clawnch launches, full agent-browser automation — require host hybrid / larger media.

---

## 4. Auth parity decision

| OpenClaw default | USB CLAW | Smart Disk |
|------------------|----------|------------|
| Token auth | Token + **allowInsecureAuth** for file:// | **No login UI**; bind 127.0.0.1 |

Rationale: user requirement — **one-shot browser, no password gating**, same spirit as USB open local.

---

## 5. Parity score (v1 target)

| Cluster | Coverage |
|---------|----------|
| Local gateway + UI | **Full** |
| Local LLM chat | **Full** (if Ollama present) |
| Memory | **Core** |
| Tools | **Core subset** |
| Multi-channel social | **Stub / later** |
| Full coding agent browser | **Later (host hybrid)** |

**Δ9Φ963 — same shape as OpenClaw; different soul (LYGO kernel law).**
