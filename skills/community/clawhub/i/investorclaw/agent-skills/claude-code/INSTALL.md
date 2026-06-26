<!--
SPDX-License-Identifier: MIT-0
Copyright 2026 InvestorClaw Contributors
-->

# InvestorClaw v4.0 — Claude Code / Claude Desktop Plugin Install

> Powered by [InvestorClaw](https://investorclaw.app) (Apache 2.0).
> This plugin is MIT-0-licensed.

## Prerequisites

- **Docker Desktop** (or Podman + `podman-compose`). Verify with
  `docker --version`. Install:
  - macOS: `brew install --cask docker` (then launch Docker.app once)
  - Linux: see `https://docs.docker.com/engine/install/` (do not pipe shell scripts from get.docker.com directly to your shell — download, review, then run)
  - Windows: `winget install Docker.DockerDesktop`
- **Claude Code** (current release). The plugin assumes the marketplace
  + MCP-server config conventions in effect at v4.0 release.

The plugin is a manifest + a SKILL.md + an MCP-server config write.
Nothing is installed on the agent side — analysis runs in the user's
container, the agent just talks to it over MCP-HTTP.

## Install from this repo

```text
/plugin marketplace add argonautsystems/InvestorClaw
/plugin install investorclaw
```

Claude Code and Claude Desktop use this repo's container-first plugin:
the same skill bundle, same Docker Compose runtime, and same MCP-HTTP
endpoint as every other agent. See `docs/GETTING_STARTED.md` for the
canonical setup and provider notes.

## Bring up the InvestorClaw service

The plugin is a thin client — the analysis engine runs in Docker on
the user's machine. After installing the plugin, bring up the
containers once:

```sh
mkdir -p ~/.investorclaw
curl -sSL https://raw.githubusercontent.com/ncz-os/mnemos-ic-runtime/main/compose.yml > ~/.investorclaw/compose.yml
cd ~/.investorclaw && docker compose up -d
```

This starts two containers: `mnemos-os/mnemos-rs:4.2` on
`localhost:5002` (memory) and `argonautsystems/ic-engine:4.7.7-cpu` on
`localhost:18090` (portfolio analysis). First boot pulls ~600 MB of
images; subsequent boots are instant.

Verify health:

```sh
curl -fsS http://localhost:18090/healthz
curl -fsS http://localhost:5002/healthz
```

Both should return 200.

## Upload a portfolio

Open the dashboard at **http://localhost:18092** in your browser. Drop
in a broker CSV / XLS / XLSX / PDF. The dashboard handles column
mapping for unfamiliar formats. The file lives inside the container at
`/data/portfolios/` and Claude Code never sees the raw rows.

Once a portfolio is loaded, ask Claude Code anything:

```
/ask what's my current asset allocation?
/ask which holdings underperformed SPY this quarter?
/refresh    # pull fresh quotes
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `/ask` returns "tool not found" | Plugin not loaded. Restart Claude Code. |
| `/ask` returns connection refused | Containers not running. `cd ~/.investorclaw && docker compose up -d`. |
| `docker compose` says "command not found" | Docker Desktop not installed or not running. See Prerequisites. |
| Dashboard at `:8092` won't load | Wait ~10 seconds after `docker compose up -d` for health checks, then retry. |
| Tools return "no portfolio loaded" | Open the dashboard and upload a portfolio file first. |
| MCP endpoints answer but tools list is empty | The ic-engine container started before mnemos-rs finished its DB migration. `docker compose restart ic-engine`. |

If the issue is in the analysis output (numbers look wrong, format not
recognized), file at `github.com/argonautsystems/InvestorClaw` — that's the
Apache 2.0 service repo. If the issue is in the plugin itself
(manifest, SKILL.md, slash command wiring), file at
`mnemos-os/mnemos-ic-runtime`.

## Uninstall

```sh
cd ~/.investorclaw && docker compose down -v   # stop + remove volumes
rm -rf ~/.investorclaw                          # remove staged compose
```

Then uninstall the plugin from the Claude Code marketplace UI to remove
the MCP server config + slash command bindings.
