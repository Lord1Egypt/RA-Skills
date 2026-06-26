# GET /api/holanonce16ts — HOLA nonce response

Use this endpoint **after** API login (Bearer JWT). Fetch a **new** nonce immediately before each HOLA you sign (~5 minute validity).

## Exact JSON response shape

Use these **JSON property names verbatim** (not login field names, not guessed names like `nonceHex`):

```json
{
  "noncetsHex": "4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE",
  "timestamp": "2026-04-19T10:47:00.000Z",
  "length": 16,
  "algorithm": "randomBytes(16)_hex",
  "requestId": "01HQXYZ..."
}
```

| Field | Type | Use in HOLA line |
| --- | --- | --- |
| `noncetsHex` | string | Yes — 32 uppercase hex chars (segment often written `noncets-hex` in format docs) |
| `timestamp` | string | Yes — ISO-8601 UTC from this response |
| `length` | number | Metadata only (always `16`) |
| `algorithm` | string | Metadata only |
| `requestId` | string | Correlation only |

```javascript
const { noncetsHex, timestamp } = await nonceResponse.json();
const message = `HOLA/${recipient}/${tokenId}/${timestamp}/${noncetsHex}/API.IDENTYCLAW.COM/`;
```

## Do not confuse with API login

| Endpoint | JSON fields | Purpose |
| --- | --- | --- |
| `GET /api/login/timestamp` | `timestamp`, `timestamp_iso` | Sign `accountid + timestamp_iso` for `POST /api/login` |
| `GET /api/holanonce16ts` | `noncetsHex`, `timestamp` | Build and sign the **HOLA line** |

**Invalid on holanonce16ts:** `timestamp_iso`, `nonceHex`, `noncets`, `nonce`.

## Related docs

- [hola-agent-authentication.md](hola-agent-authentication.md) — full HOLA flow
- [hola-subagent-authentication.md](hola-subagent-authentication.md) — subagent HOLA
- [login-authentication.md](login-authentication.md) — JWT first
