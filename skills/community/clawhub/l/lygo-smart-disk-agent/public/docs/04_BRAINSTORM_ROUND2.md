# Brainstorm Round 2 — Stress test against running systems

**Signature:** `Δ9Φ963-SDA-BRAIN-R2`  
**References:** Host `ollama` running; models `qwen2.5:3b`, `llama3.2:1b`, `qwen3-coder:30b`; USB CLAW launch; lygo_openclaw pipeline.

---

## 1. What the running OpenClaw-class stack actually needs

From live host + USB config:

| Need | Evidence | SDA response |
|------|----------|--------------|
| Local OpenAI-compatible or Ollama API | Ollama :11434 up | `ollama_client.py` |
| Default instruct model | USB `ollama/qwen2.5:3b` | Same primary |
| Fast fallback | `llama3.2:1b` | Fallback list |
| Agent loop | chat → tools → memory | chat + limbs + mycelium |
| UI | browser dashboard | portal one-shot open |
| Isolation | USB lygo-data | `data/` under F: |

**30B coder model:** available on host but **wrong** for always-on SDA supervisor (RAM/latency). Document as optional “heavy host mode”, not default.

---

## 2. Round 2 critical fixes

### Fix R2-1 — Boot must not kill host Ollama
USB `taskkill ollama` is hostile to dual-use.  
**SDA boot:** probe :11434; only start portable Ollama if missing.

### Fix R2-2 — Portal must work even if model cold
Health shows `brain: cold|warm`; chat returns clear “pull model” message; UI still loads.

### Fix R2-3 — Session continuity without cloud
Mycelium JSONL append-only; session id in localStorage of portal.

### Fix R2-4 — Firmware seal hash
`firmware/seal.json` SHA-256 printed in `/api/health` for Guardian/Ethical-Chip alignment storytelling + tamper notice.

### Fix R2-5 — Test without network
Tests mock Ollama or skip chat if offline; structural tests always run.

### Fix R2-6 — Path portability
All paths via `Path(__file__)` / `%SDA_ROOT%`; no hardcoded `F:\` inside Python (only launchers set env).

---

## 3. Remaining risks (accepted)

| Risk | Mitigation |
|------|------------|
| Foreign PC has no Ollama | Clear health + install link offline doc |
| 15 MB fills with logs | Rotate logs; cap mycelium files |
| User expects full OpenClaw browser agent | Parity matrix honesty; limb stub |

---

## 4. Round 2 go / no-go

| Criterion | Decision |
|-----------|----------|
| Design covers OpenClaw-shaped core | **GO** |
| Design honest about 15 MB | **GO** |
| Model selection efficient | **GO** (`qwen2.5:3b` / `1b`) |
| Ready to freeze docs and build | **GO** |

**Δ9Φ963 — second pass: don't kill brains, don't lie about disk size, don't ship 30B as default.**
