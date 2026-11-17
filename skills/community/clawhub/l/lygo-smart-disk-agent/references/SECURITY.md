# SECURITY — lygo-smart-disk-agent v1.1.0

**Signature:** `Δ9Φ963-SDA-SECURITY-v1.1.0`

## Trust model

| Control | Detail |
|---------|--------|
| Bind | **localhost** only |
| Remote password wall | **No** (`password_gate: false`) |
| Local operator token | **Yes** by default (`auth.required: true`) |
| Token storage | `data/.sda_local_token` (generated, gitignored, not in package payload) |
| Header | `X-SDA-Token` or `Authorization: Bearer …` |
| One-shot UX | Boot opens `http://localhost:9631/?t=<token>` then portal stores in sessionStorage |

## Agentic controls

| Surface | Policy |
|---------|--------|
| `/api/health`, `/api/auth` | Public probe (no token secret returned) |
| `/api/chat`, `/api/limb`, `/api/status`, `/api/help` | **Require local token** |
| `memory` / `open-url` / limb `chat` over HTTP | **403** |
| Chat persistence | Metadata only (hash + lengths) |
| CORS | No wildcard |
| POST body | ≤ 64 KiB |
| `0.0.0.0` bind | Refused unless `LYGO_SDA_ALLOW_LAN=1` |

## Not malware

- No cloud callbacks at install
- No dynamic remote code load
- Pure Python/HTML/JSON
- Token is **local operator secret**, not vendor cloud auth

## Disable token (not recommended)

```json
"auth": { "required": false }
```

## Reviewer note

This is a **disclosed local AI portal**. Unauthenticated remote abuse is mitigated by:

1. localhost bind  
2. local token on API  
3. no HTTP chat-history export  

See `SKILLSPECTOR_AUDIT.md`.
