---
name: lygo-smart-disk-agent
description: "LYGO SMART DISK AGENT — lean 100% LYGO CLAW. Localhost portal with local operator token (not cloud password), P0–P5, host Ollama. No HTTP chat-memory export. Read references/SECURITY.md first."
metadata: {"lygo": true, "biophase7": true, "version": "1.1.0", "signature": "Δ9Φ963-LYGO-SMART-DISK-AGENT-v1.1.0", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "tree": "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/lygo_smart_disk", "publisher": "deepseekoracle", "portal": "http://localhost:9631/", "security_doc": "references/SECURITY.md", "skillspector": "references/SKILLSPECTOR_AUDIT.md"}
---

# LYGO SMART DISK AGENT

Lean **LYGO CLAW** disk product: kernel-up offline portal + host Ollama.

| | |
|--|--|
| Version | **1.1.0** |
| Portal | http://localhost:9631/ |
| Auth | **Local operator token** (`X-SDA-Token`, auto on boot) |
| Package | https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/lygo_smart_disk |

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-smart-disk-agent
cd public
ollama pull qwen2.5:3b
python verify/self_check.py
python agent/smart_disk_agent.py
```

Boot prints the token and opens the browser with `?t=` once.

## Security summary

- Localhost only; local token on API  
- No HTTP memory export; chat metadata only on disk  
- Static self-check (no dynamic loaders)  
- See `references/SECURITY.md` + `references/SKILLSPECTOR_AUDIT.md`

## Self-check

```bash
python scripts/self_check.py
```

**Δ9Φ963 — small disk, full law, local token.**
