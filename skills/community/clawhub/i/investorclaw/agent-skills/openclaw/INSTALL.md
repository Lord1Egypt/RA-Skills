<!--
SPDX-License-Identifier: MIT-0
Copyright 2026 InvestorClaw Contributors
-->

# Installing InvestorClaw on openclaw (4.29-beta.4+)

Install path for the **openclaw** agent runtime. InvestorClaw v4.0 ships
as a two-container Docker compose service; openclaw connects to it via
two native MCP-HTTP servers. Total setup is five steps.

## Prerequisites

- **openclaw 4.29-beta.4 or newer** — verify with `openclaw --version`.
  Earlier versions don't expose the `openclaw mcp set` CLI surface this
  install relies on.
- **Docker** (or Podman with `docker` shim) — verify with
  `docker --version`. The compose file uses Docker Compose v2 syntax.
- A free pair of loopback ports: `18090` (investorclaw) and `5002`
  (mnemos). Also `8092` for the dashboard.

## Step 1 — Install the InvestorClaw service

Stage the compose file and start the stack:

```bash
mkdir -p ~/.investorclaw
curl -sSL https://raw.githubusercontent.com/ncz-os/mnemos-ic-runtime/main/compose.yml \
  > ~/.investorclaw/compose.yml
cd ~/.investorclaw && docker compose up -d
```

Wait for the health endpoints to come up:

```bash
curl -fsS http://localhost:18090/healthz   # investorclaw / ic-engine
curl -fsS http://localhost:5002/healthz   # mnemos
```

Both should return `200 OK` within ~30 seconds on first start (the
`argonautsystems/ic-engine:4.7.7-cpu` image needs a moment to warm caches).

## Step 2 — Register the two MCP servers with openclaw

Use the validated `openclaw mcp set` CLI. **Do not edit
`~/.openclaw/openclaw.json` directly** — see Troubleshooting below.

```bash
openclaw mcp set \
  --name investorclaw \
  --transport http \
  --url http://localhost:18090/mcp

openclaw mcp set \
  --name mnemos \
  --transport http \
  --url http://localhost:5002/mcp
```

Verify both are registered:

```bash
openclaw mcp list
openclaw mcp show investorclaw
openclaw mcp show mnemos
```

> **Alternative — JSON5 patch path.** If you prefer to apply both
> servers in one shot (e.g., reproducible provisioning), use the
> `config-snippet.json5` shipped in this directory:
>
> ```bash
> openclaw config patch --file config-snippet.json5
> ```
>
> This goes through the same validator as `openclaw mcp set` and
> survives the config-health daemon.

## Step 3 — Validate the config

```bash
openclaw config validate
```

Should report no errors. If it does report errors, do not proceed —
fix them first (typical cause: a typo in a URL, or the CLI flagged an
unrelated provider-config issue inherited from a prior install).

## Step 4 — Reload openclaw

If openclaw is running as a long-lived gateway/daemon (Docker container,
systemd service, etc.), reload or restart it so the gateway picks up
the new MCP servers:

```bash
# Docker:
docker restart openclaw

# Or, if running interactively, exit and re-launch your openclaw session.
```

For one-shot CLI invocations (`openclaw agent ...`), no reload is
needed — the next invocation reads the updated config.

## Step 5 — Try it

```bash
openclaw agent \
  --to "$YOUR_OPENCLAW_CHANNEL_TARGET" \
  --message "What is in my portfolio?"
```

The LLM should pick the `investorclaw.portfolio_holdings` tool from its
schema, call the MCP server at `127.0.0.1:18090/mcp`, and return a
structured summary. If you don't yet have a portfolio file uploaded, the
tool will return a structured "no portfolio detected" envelope — open
the dashboard at `http://localhost:18092/` to upload one.

## Networking note (if openclaw runs in a container)

If openclaw itself is containerized, `127.0.0.1` inside that container
is **not** the host's loopback. Two options:

1. **Join the InvestorClaw compose bridge network.** Add openclaw's
   container to the `investorclaw_default` bridge and use the service
   names `investorclaw:8090` and `mnemos:5002` in the MCP URLs.
2. **Use `host.docker.internal`.** On Docker Desktop (macOS/Windows)
   and recent Docker on Linux, `host.docker.internal` resolves to the
   host. Replace `127.0.0.1` with `host.docker.internal` in the MCP
   URLs you pass to `openclaw mcp set`.

If openclaw runs natively on the host (no container), `127.0.0.1` works
as written above.

## Troubleshooting

### "I edited `openclaw.json` and my MCP servers vanished"

openclaw 4.29-beta.4+ ships a config-health daemon. On every gateway
reload, it re-validates `~/.openclaw/openclaw.json` against the JSON
schema. If a write is missing schema-required fields it flags the file
`"suspicious":["reload-invalid-config"]`, moves it aside as
`openclaw.json.clobbered.<ts>`, and restores from
`openclaw.json.last-good`.

**Always use `openclaw mcp set` or `openclaw config patch --file <path>`
to write config.** Both go through the validator before write — they
won't be clobbered. Never `cat > openclaw.json`. Never hand-edit the
file in a text editor.

### LLM acknowledges the request but never invokes a tool

openclaw 4.29-beta.4 includes a workspace-bootstrap workflow at
`~/.openclaw/workspace/{BOOTSTRAP,IDENTITY,USER}.md` that, on first
contact, instructs the LLM to ask the operator for name / timezone /
persona before doing anything else. For interactive use, just answer
those prompts once. For headless automation (cron jobs, harnesses),
seed the workspace files with `Status: COMPLETE` content so the LLM
proceeds directly to tool calls. v4.0's MCP integration is far less
likely to trigger this loop than the v2.x plugin path — the LLM has
clear, well-described MCP tools available, so it tends to call them
rather than re-enter onboarding chat — but the workaround is the same
when it does fire. See `KNOWN_ISSUES.md` OC-1 in the InvestorClaw repo
for the seeded-file format.

### `openclaw mcp set` reports "transport http not supported"

You're on an openclaw older than 4.29-beta.4. Upgrade — earlier
versions either lack `mcp set` entirely or only expose stdio transport.

### Tools register but every call returns a connection error

The InvestorClaw service isn't running (or isn't reachable from
openclaw's network namespace). Re-run the health checks from Step 1.
If those pass from the host but openclaw still can't reach them, see
the "Networking note" above — you likely need `host.docker.internal`
or compose-network membership.

### Dashboard

The dashboard at `http://localhost:18092/` is where users upload
portfolio files, configure the optional InvestorClaw narrative tier
(separate from openclaw's own LLM provider config), and inspect raw
`ic_result` envelopes for debugging. Bookmark it.

## Uninstall

```bash
openclaw mcp unset --name investorclaw
openclaw mcp unset --name mnemos
cd ~/.investorclaw && docker compose down -v
rm -rf ~/.investorclaw
```
