# Connecting LinkedCamp to OpenClaw

LinkedCamp's tools come from its hosted MCP server,
`https://mcp.linkedcamp.com/mcp`. OpenClaw connects to it as an MCP server named
`linkedcamp`; its tools then appear as `linkedcamp__<tool>`.

The commands below run on the machine that hosts the OpenClaw Gateway. If you
have an exec tool and the user approves, you may run them; otherwise give them
to the user to run. Never put an API key on a command line yourself.

## Option A — sign in with OAuth (recommended)

No secret is stored in config; OpenClaw keeps an encrypted token and refreshes
it.

```bash
openclaw mcp set linkedcamp '{"url":"https://mcp.linkedcamp.com/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login linkedcamp
```

`login` prints an authorization URL. The user opens it, pastes their API key
from **LinkedCamp → Settings → Integrations** into LinkedCamp's own page, and
approves. If the browser cannot reach the Gateway's loopback callback (a remote
or headless Gateway), the page shows a code; finish with
`openclaw mcp login linkedcamp --code <code>`.

From the Control UI the same thing is **Settings → MCP → linkedcamp → Sign in**,
once the server entry exists.

## Option B — API key header

For headless or scripted Gateways. Keep the key in the Gateway's environment,
not in `openclaw.json`:

```bash
# ~/.openclaw/.env on the Gateway host
LINKEDCAMP_API_KEY=<paste the key here, never into chat>
```

```bash
openclaw mcp set linkedcamp '{"url":"https://mcp.linkedcamp.com/mcp","transport":"streamable-http","headers":{"X-Api-Key":"${LINKEDCAMP_API_KEY}"}}'
```

The single quotes matter: OpenClaw expands `${LINKEDCAMP_API_KEY}` from its own
environment when it connects, so the key never lands in the config file.
Restart the Gateway after editing `.env`.

## Option C — every chat sender connects their own account

On a shared Gateway (a team Slack or Discord), each sender can sign in to their
own LinkedCamp account instead of sharing one. This needs the Gateway's public
HTTPS origin:

```bash
openclaw config set gateway.publicOrigin https://gateway.example.com
openclaw mcp set linkedcamp '{"url":"https://mcp.linkedcamp.com/mcp","transport":"streamable-http","auth":"oauth","oauth":{"identity":"per-requester"}}'
```

The first LinkedCamp tool call from each sender returns a sign-in link for
that sender. Anyone who opens a sign-in link connects their account to the
sender it was issued for, so use this only where channel members trust each
other.

## Verify

```bash
openclaw mcp probe linkedcamp
```

A healthy probe lists the LinkedCamp tools. Then, in a new chat turn, call
`linkedcamp__whoami` — it names the connected account and plan.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `401` / "API key" error | OAuth: `openclaw mcp logout linkedcamp`, then `login` again. Header: check `LINKEDCAMP_API_KEY` is set in the Gateway's environment and is the UUID from Settings → Integrations. |
| Probe works but the agent has no `linkedcamp__*` tools | The agent's tool profile excludes MCP tools. `coding` and `messaging` include them; `minimal` does not. Check `tools.deny` for `bundle-mcp` or `linkedcamp__*`. |
| Changes not picked up | `openclaw mcp reload`, or restart the Gateway that owns the connection. |
| A tool the skill mentions is missing | The LinkedCamp plan or permissions hide it (see `whoami`). It is not a connection problem. |
| Your provider gave you a different MCP URL | Use that URL in place of `https://mcp.linkedcamp.com/mcp`. |
