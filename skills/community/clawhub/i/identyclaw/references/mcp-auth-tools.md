# Client-Side Agent Authentication

Guidance for AI agents that call authenticated IdentyClaw API endpoints. Store JWTs on the **agent machine**—via SDK, local plugin, or file—and keep them out of model-visible chat and tool output.

The public IdentyClaw MCP server (`POST /mcp`) serves documentation through `list_resources` and `get_resource` only. Use it to fetch this guide and related references; perform login and protected calls from the agent host.

Fetch via MCP: `get_resource({ uri: "doc:reference:mcp-auth-tools" })`

API error codes and schemas: `openapi:swagger` (authoritative). Login flow: [login-authentication.md](login-authentication.md).

## When login succeeds but the next call returns 401

Agent harnesses (OpenClaw, Cursor, shell agents) often **redact** `jwt_token` in tool output to fragments like `eyJhbG…ISDw`. Use the full token from your storage mechanism—not the redacted log line—in `Authorization: Bearer …`.

Typical sequence:

1. `POST /api/login` → **200**, full `jwt_token` issued (~1500–2000 characters)
2. Next request uses a **truncated** bearer value → **401** `INVALIDATED_TOKEN`, `details.reason: invalid_jwt_format`
3. Agent incorrectly blames server session state

Check bearer token **length** and **format** (three dot-separated segments; response field `jwt_token`, not `token`) before investigating server-side session storage.

Machine-readable troubleshooting: `guide:troubleshooting`.

## Store and reuse JWTs on the agent machine

| Step | Action |
| --- | --- |
| Login | Obtain `jwt_token` via curl login, login script, or local plugin |
| Store | Keep the token in a file, environment variable, or SDK session on the agent host |
| Protected calls | Read the token from that store: `Authorization: Bearer $(cat ~/.identyclaw/jwt.txt)` |
| Verify | `GET /api/me/identity` using the same storage path as login |

## Recommended integrations (typical agent → API)

1. **curl + file-stored JWT** — login via `GET /api/login/timestamp` → sign locally → `POST /api/login`; store `jwt_token` on disk; protected calls with `Authorization: Bearer $(cat ~/.identyclaw/jwt.txt)`. **No client-side NEAR RPC.**
2. **Login script on the agent machine** — same wire format; stdout prints status metadata only (`ok`, `jwt_length`, `token_id`)
3. **Local agent plugin** — OpenClaw `@identyclaw/openclaw-identyclaw-plugin` (v1.4.0+). Separates **API session** (auto-login JWT) from **HOLA lines** (create/verify tools). `nearPrivateKey` used for API login signature and HOLA line signing only on the Gateway — never sent to login endpoints.
4. **`@rodit/hola-client`** — Node library (`createHola`, `buildAndSign`) for HOLA line construction; requires API bearer token for nonce fetch.
5. **Optional: `@rodit/rodit-auth-be`** — `RoditClient.login_server()` for MITM protection via NEAR RPC.

## File-based shell pattern

**Reference (IdentyClaw)** — API `https://api.identyclaw.com`, JWT at `~/.identyclaw/jwt.txt` (from curl login; see [login-authentication.md](login-authentication.md)):

```bash
JWT="$(cat ~/.identyclaw/jwt.txt)"
curl -sS -H "Authorization: Bearer ${JWT}" https://api.identyclaw.com/api/holanonce16ts
```

Your login script on the agent host must write the full JWT to that file and must not print the raw `jwt_token` to stdout.

## HOLA workflow after API login

1. **API login** — obtain `jwt_token` ([login-authentication.md](login-authentication.md)); this is your API session, not a HOLA line
2. **Create outbound HOLA line** — `identyclaw_create_hola`, `@rodit/hola-client` `createHola()`, or hand-build per [hola-howto.md](hola-howto.md) (uses `noncetsHex` + `timestamp` from `/api/holanonce16ts`, not login `timestamp_iso`)
3. **Verify inbound HOLA line** — `POST /api/identity/verify` or `identyclaw_verify_hola` (payload is the HOLA string)
4. Optional self-test — `POST /api/testhola` with your line and API session JWT

## MCP documentation vs authenticated API calls

Use MCP to fetch guides and OpenAPI:

| URI | Purpose |
| --- | --- |
| `doc:reference:login-authentication` | Login flow and JWT usage |
| `doc:reference:mcp-connection-guide` | MCP setup, access patterns, resource URIs |
| `doc:reference:mcp-auth-tools` | This document |
| `guide:troubleshooting` | Common errors including truncated JWT |
| `openapi:swagger` | Canonical API schema |

MCP tools on `https://api.identyclaw.com/mcp`: **`list_resources`**, **`get_resource`**.
