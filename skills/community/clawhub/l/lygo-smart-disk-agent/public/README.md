# LYGO SMART DISK AGENT

**100% LYGO CLAW lean prototype** — kernel-up, OpenClaw-shaped, **localhost + local operator token**.

| | |
|--|--|
| Portal | http://localhost:9631/ |
| Boot | `launch/LYGO_SMART_DISK_BOOT.bat` or `python agent/smart_disk_agent.py` |
| Auth | **Local token** (auto-generated, one-shot browser URL) — not a cloud password gate |
| Models | Host Ollama: `qwen2.5:3b` primary |
| Docs | `docs/` · stack: [`../docs/LYGO_SMART_DISK_AGENT.md`](../docs/LYGO_SMART_DISK_AGENT.md) |
| ClawHub | [deepseekoracle/lygo-smart-disk-agent](https://clawhub.ai/deepseekoracle/lygo-smart-disk-agent) |

## Security (1.1.0)

| Control | Behavior |
|---------|----------|
| Bind | `localhost` only (refuse `0.0.0.0` without `LYGO_SDA_ALLOW_LAN=1`) |
| HTTP auth | Local operator token (`X-SDA-Token` / `data/.sda_local_token`) |
| Memory over HTTP | **Blocked** |
| Chat on disk | Hash + lengths only |
| open-url over HTTP | **Blocked** |
| Boot UX | Opens browser with `?t=<token>` once (sessionStorage) |

```bash
ollama pull qwen2.5:3b
python verify/self_check.py
python -m unittest tests/test_smart_disk.py -v
python agent/smart_disk_agent.py          # prints token + opens portal
python agent/smart_disk_agent.py token    # print token only
```

Set `"auth": {"required": false}` in `config/smart_disk.json` only if you intentionally want open loopback (not recommended).

**Signature:** `Δ9Φ963-LYGO-SMART-DISK-AGENT-v1.1.0`
