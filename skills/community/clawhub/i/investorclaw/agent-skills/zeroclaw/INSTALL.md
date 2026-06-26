<!--
SPDX-License-Identifier: MIT-0
Copyright 2026 InvestorClaw Contributors

User-facing install guide for the InvestorClaw zeroclaw skill.
This file is documentation; it is NOT part of the audited skill payload.
-->

# Installing the InvestorClaw skill on zeroclaw

This guide assumes **zeroclaw on master** (not the 0.7.3 demo image at
`ghcr.io/perlowja/nclawzero-demo:latest`, which lacks `[mcp]` config
support) and **Docker** (or Podman with a docker-compatible CLI).

## Prerequisites

| Requirement | Verify with |
| --- | --- |
| zeroclaw built from master, with `[mcp]` config support | `zeroclaw --version` and inspect `~/.zeroclaw/config.toml` for an existing `[mcp]` section |
| Docker (or Podman + alias) | `docker --version` |
| Docker compose v2 | `docker compose version` |
| Localhost ports 5002, 8090, 8092 free | `lsof -i:5002 -i:8090 -i:8092` should show nothing |

If any of these fail, fix them before continuing. zeroclaw 0.7.3
specifically does **not** support `[mcp.servers.*]` blocks; the demo
image will silently ignore the config and the tools will not register.

## Step 1 — Drop the skill manifest in place

Copy `SKILL.md` and `SKILL.toml` from this directory into the zeroclaw
skill registry:

```
mkdir -p ~/.zeroclaw/skills/investorclaw
cp SKILL.md SKILL.toml ~/.zeroclaw/skills/investorclaw/
```

Do **not** copy `INSTALL.md` or `config-snippet.toml` into the skill
directory — they are documentation, not part of the audited payload.

## Step 2 — Install and start the InvestorClaw service

```
mkdir -p ~/.investorclaw
curl -sSL https://raw.githubusercontent.com/ncz-os/mnemos-ic-runtime/main/compose.yml \
  > ~/.investorclaw/compose.yml
cd ~/.investorclaw
docker compose up -d
```

This starts two containers bound to localhost:

| Container | Image | Port |
| --- | --- | --- |
| mnemos | `mnemos-os/mnemos-rs:4.2` | `localhost:5002` |
| ic-engine | `argonautsystems/ic-engine:4.7.7-cpu` | `localhost:18090` |
| dashboard (optional) | bundled | `localhost:18092` |

Wait for health:

```
curl -fsS http://localhost:18090/healthz
curl -fsS http://localhost:5002/healthz
```

Both should return 200 within ~10 seconds of `compose up`.

## Step 3 — Add the MCP servers to zeroclaw config

Open `~/.zeroclaw/config.toml` and merge in the block from
`config-snippet.toml` (also reproduced here for convenience):

```toml
[mcp.servers.investorclaw]
transport = "http"
url = "http://localhost:18090/mcp"

[mcp.servers.mnemos]
transport = "http"
url = "http://localhost:5002/mcp"
```

If `config.toml` already has an `[mcp]` section, append the
`[mcp.servers.*]` blocks under it. Order does not matter; TOML allows
either flat dotted keys or nested tables.

If your zeroclaw build enforces `autonomy.allowed_commands`, ensure
the following are allowed (used by future install/refresh paths,
harmless to add now):

```toml
[autonomy]
allowed_commands = ["docker", "curl", "mkdir", "investorclaw"]
```

## Step 4 — Validate the config

```
zeroclaw config validate
```

Expected: no errors, and the output should list `investorclaw` and
`mnemos` under registered MCP servers. If you see "unknown key
`mcp.servers`", you are running zeroclaw 0.7.3 or older — upgrade to
master.

## Step 5 — Try it

```
zeroclaw agent -m "What is in my portfolio?"
```

If you have not uploaded a portfolio yet, the engine returns a
structured "no portfolio loaded" envelope and points you at the
dashboard wizard:

```
http://localhost:18092/
```

Upload a broker CSV / Excel / PDF there, then re-run the agent
command.

## Future: one-command install

A pending upstream PR adds a `zeroclaw services` subcommand that will
collapse Steps 2 and 3 into:

```
zeroclaw services install https://raw.githubusercontent.com/ncz-os/mnemos-ic-runtime/main/compose.yml
```

This will pull the compose file, run `docker compose up -d`, wait for
health, and patch `config.toml` with the MCP server blocks
automatically. Until that lands on master, follow the steps above.

## Troubleshooting

**Tools not registering after step 5.** Check `zeroclaw config
validate` again. The most common cause is running the 0.7.3 demo
image, which silently drops unknown `[mcp]` keys. Upgrade zeroclaw to
master.

**`zeroclaw agent` hangs on the first call.** The MCP server may still
be warming up. Wait 5–10 seconds after `docker compose up -d` and
retry. If the hang persists, check `docker compose logs ic-engine`.

**`investorclaw.portfolio_*` returns "no portfolio loaded".** The
engine has not detected a portfolio file. Open the dashboard at
`http://localhost:18092/`, upload a CSV/PDF, then call
`investorclaw.portfolio_refresh` (or just retry the original prompt).

**Port already in use on 5002, 8090, or 8092.** Stop the conflicting
process or override the port mappings in
`~/.investorclaw/compose.yml`. If you change a port, update the
matching `[mcp.servers.*]` URL in `~/.zeroclaw/config.toml` to keep
them in sync.

**Wanting to remove the skill.** Stop the containers
(`cd ~/.investorclaw && docker compose down`), delete
`~/.zeroclaw/skills/investorclaw/`, and remove the
`[mcp.servers.investorclaw]` and `[mcp.servers.mnemos]` blocks from
`~/.zeroclaw/config.toml`.

## Reporting issues

- Skill manifest bugs (this directory):
  `https://github.com/argonautsystems/InvestorClaw/issues`
- Service bugs (engine / mnemos): same repo; tag `service` /
  `ic-engine` / `mnemos-rs`
- zeroclaw bugs (config parsing, MCP transport): upstream zeroclaw
  repository
