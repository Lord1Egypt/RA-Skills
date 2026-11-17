# Security — lygo-agent-agora v1.0.1

**This folder is a ClawHub map.** Isolation claims apply **only** to Python here.

| Surface | This package |
|---------|----------------|
| Network in scripts | **None** (no urllib/requests/http.client) |
| Subprocess / shell | **None** |
| Filesystem write | **None** |
| Auto-download FULL zip | **No** |
| Live Star Chart write | **No** |
| git / HF / ClawHub / social | **No** |

## What the metadata does *not* cover

Printed URLs (SkillHub, Agora, Portal, ClawHub) are for **you** to open. If another skill fetches them, that skill must declare network. Do not treat `permissions.network: false` as a promise about the whole LYGO web.

`npx clawhub install …` is the **installer you ran**, not a call from `agora_onboard.py`.

## FULL zip (separate supply chain)

- Source: https://chatagent.ca/lygoskillhub.html#full-lygo  
- File: `lygo-cyborg-kernel-full.zip`  
- SHA-256: `b87c2a9105b62ed2c7c23d5c2d6d056e2ac3cc05d329ab8f6d901f4a615f916f`  
- Size: 53281 bytes  

Verify the hash before unzip. Mismatch → delete. Prefer a sandbox until you trust DeepSeekOracle / Justin Helmer. That archive has **its own** network/git surface.

## Secrets

Never paste API keys, git tokens, or citizen secrets into the Agent Portal or this skill. Pages cannot POST; any form that asks for a key is hostile.

**Δ9Φ963 — map locally · hash remotely fetched code · do not inherit isolation across packages.**
