# LYGO SMART DISK AGENT — Architecture

**Signature:** `Δ9Φ963-SDA-ARCH-v1`

---

## 1. Layer cake (kernel up)

```text
 P9  Public mesh / optional HTTPS later     (stub / docs only on lean disk)
 P6–P8  Mesh · attestation · HAIP         (stubs + status limbs)
 P5  Action identity (Light Code node)     harmony.py
 P3  Consensus (3-6-9 optional)            consensus.py
 P1  Mycelium memory                       memory.py + data/mycelium/
 P0  Φ-Gate / ethical firmware             p0_gate.py + firmware/seal.json
 ─────────────────────────────────────
 Agent limbs (help, status, chat, lattice, army-sentinel, browser-open)
 Ollama client (host or portable discovery)
 HTTP supervisor :9631
 Browser portal (static + /api/*)
```

---

## 2. Process model

```text
 LYGO_SMART_DISK_BOOT.bat
        │
        ├─► ensure Ollama (host :11434 or portable path)
        │
        └─► python agent/smart_disk_agent.py serve
                 │
                 ├─ GET  /           → portal UI
                 ├─ GET  /api/health → brain + kernel status
                 ├─ POST /api/chat   → P0 → Ollama → P1 store
                 ├─ POST /api/limb   → P0 → limb dispatch
                 └─ GET  /api/memory → recent mycelium
```

**No login form. No onboarding wizard. No token prompt for local UI.**

---

## 3. Directory map (`F:\LYGO_SMART_DISK_AGENT`)

| Path | Role |
|------|------|
| `docs/` | Design + parity + brainstorm |
| `kernel/` | P0–P5 condensed firmware modules |
| `firmware/seal.json` | Ethical chip / guardian policy seal |
| `agent/` | Supervisor + Ollama + limbs |
| `portal/` | One-shot browser UI |
| `launch/` | Boot / stop scripts |
| `config/smart_disk.json` | Ports, models, bind |
| `data/` | Mycelium, logs, sessions |
| `tests/` | Automated tests |
| `verify/self_check.py` | Green/red gate |

---

## 4. Isolation

| Variable | Smart Disk |
|----------|------------|
| `LYGO_SMART_DISK_ROOT` | `F:\LYGO_SMART_DISK_AGENT` |
| `HOME` override | Optional `data/home` (minimal) |
| Bind | `127.0.0.1` only |
| Auth | **none** for local portal (USB-style open local) |

---

## 5. vs USB LYGO CLAW

| | USB CLAW | Smart Disk Agent |
|--|----------|------------------|
| Media | Multi‑GB E: | **~15 MB F:** |
| Gateway | Node lygo-gateway :18789 | **Python supervisor :9631** |
| UI | lygo-claw.html + control-ui | **Single portal/** |
| Brain | Portable Ollama + models on USB | **Discover host/portable Ollama** |
| Stack | Full copy under stack/ | **Condensed kernel modules** |
| Goal | Full standalone | **Lean kernel-up prototype** |

---

## 6. API sketch

### `POST /api/chat`
```json
{ "message": "status of lattice", "session": "default" }
```
Response includes `verdict`, `reply`, `model`, `memory_id`.

### `POST /api/limb`
```json
{ "limb": "status", "args": [] }
```

### `GET /api/health`
Ollama up, model list, disk free, P0 seal hash.

---

## 7. Security model (local open)

- **Local open is intentional** (USB CLAW allowInsecureAuth pattern).  
- **Not** bound to `0.0.0.0` by default.  
- High-risk limbs (shell, publish) disabled or consent-flagged in config.  
- P0 still blocks obvious quarantine strings / oversized payloads.

**Δ9Φ963 — architecture is law-shaped, not feature-stuffed.**
