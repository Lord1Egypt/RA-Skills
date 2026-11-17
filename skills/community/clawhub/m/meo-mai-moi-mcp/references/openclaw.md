# OpenClaw native MCP onboarding

Use OpenClaw's native MCP registry. Do not use the older `mcporter` registry for
this connection.

## Inspect before changing

Confirm that native MCP commands exist, then inspect the saved entry:

```bash
openclaw mcp --help
openclaw mcp show meo-mai-moi --json
```

If the command is unavailable, tell the user that this OpenClaw version lacks
native MCP management and give one compact upgrade or manual-configuration
fallback. If an existing `meo-mai-moi` entry points anywhere except
`https://mcp.meo-mai-moi.com/mcp`, stop and ask before replacing it.

If the correct entry is already authorized, probe it and reuse it. Do not force
reauthorization merely because the user asked whether Meo is connected.

## Configure and start OAuth

Lifecycle order: configure → OAuth → probe → user session reset → first Meo
call. Do not skip the reset.

For a missing entry and a broad “connect Meo Mai Moi” request, use Everyday
care:

```bash
openclaw mcp add meo-mai-moi \
  --url https://mcp.meo-mai-moi.com/mcp \
  --transport streamable-http \
  --auth oauth \
  --oauth-scope 'pets:read pets:write health:read health:write habits:read habits:write microchips:read microchips:write' \
  --no-probe
openclaw mcp login meo-mai-moi
```

Use `--no-probe` only for initial registration because the server cannot be
probed before OAuth. For a narrower named task, substitute that task's scopes.
For Full management, require an explicit user choice and the sensitivity warning
from [connection.md](connection.md), then use that preset's full scope string.
To change scopes on the correct existing entry:

```bash
openclaw mcp configure meo-mai-moi --auth oauth --oauth-scope '<scopes>'
```

Prefer a local browser callback when the OpenClaw host can open one. When the
flow is headless, return the generated authorization link only in the same
private one-to-one conversation. Tell the user to approve it and send back one
of:

- the bare authorization `code`
- a `code&state=...` query tail
- the full `http://localhost:...` callback URL

Never ask for access tokens, refresh tokens, client secrets, or stored OAuth
files.

## Parse and exchange the code

In a private one-to-one channel only, extract the `code` value yourself before
calling OpenClaw:

1. If the paste is a full URL, parse its query string and take `code`.
2. If it looks like `code=...&state=...` or `...&state=...` with an earlier
   `code`, take only the `code` parameter value.
3. If it is a bare string with no `=` or `&`, treat the whole string as the code.
4. Reject an empty code, or a value that still contains an unparsed URL/query
   blob (unbounded paste). Do not pass those to `--code`.
5. Exchange immediately as a one-time credential. Never echo, log, screenshot,
   or store the code, callback URL, or query tail in later messages.

```bash
openclaw mcp login meo-mai-moi --code '<code-only>'
```

If the code or device flow is rejected or expired, discard it and start a **new**
authorization with `openclaw mcp login meo-mai-moi`. Do not retry the same code.
Never request or accept the URL or code in a group/public channel; ask the user
to finish the same command locally on the OpenClaw host instead.

## Verify configuration, then reset the session

After the code exchange succeeds:

```bash
openclaw mcp status --verbose
openclaw mcp probe meo-mai-moi
openclaw mcp reload
```

Use `openclaw mcp probe` as the configuration and authentication check. Do not
treat an unrelated or empty `tool_search` result as proof that Meo tools are
missing from the server.

`openclaw mcp reload` refreshes CLI/runtime configuration. It does **not**
retrofit native MCP tools into an already-created Codex-backed agent thread.
After a successful probe, tell the user to start a new OpenClaw session with
`/new` (or `/reset`) before requesting the first Meo operation.

Do not add an OpenClaw tool include/exclude filter: expose the complete Meo tool
catalog and let OAuth plus each tool's scope enforcement control access.

## Confirm projection in the new session

In the fresh session, discover tools and call `list_pets` with `{}` before
claiming the connection is usable. Only a successful native read proves
projection.

## Recovery map

| Failure | Action |
|---|---|
| Expired or rejected authorization code / device flow | Start a new `openclaw mcp login`; do not reuse the old code |
| `insufficient_scope` on a tool | Merge only the missing domain pair (or switch preset if the user asks) and reauthorize |
| Probe fails after OAuth | Fix config/auth; re-run `openclaw mcp probe`. Do not claim tools are ready |
| Probe succeeds but Meo tools are missing in this chat | Session is stale: ask the user for `/new` or `/reset`. Do **not** authorize again |
| Wrong or unexpected server URL on `meo-mai-moi` | Stop and confirm before replacing the entry |
