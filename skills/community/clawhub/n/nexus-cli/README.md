<p align="center">
  <br>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/logo.svg">
    <img alt="Admirarr" src="assets/logo.svg" width="180">
  </picture>
  <br><br>
  <a href="#quick-start"><img src="https://img.shields.io/badge/install-one_liner-D4A843?style=for-the-badge" alt="Install"></a>
  &nbsp;
  <img src="https://img.shields.io/badge/go-single_binary-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go">
  &nbsp;
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/Agent_Skills-compatible-D4A843?style=for-the-badge" alt="Agent Skills"></a>
  &nbsp;
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="License"></a>
  <br><br>
  <strong>Command your fleet. The unified CLI for your *Arr stack — human and agent operated.</strong>
</p>

<br>

## What is Admirarr?

Deploy, wire, operate, and diagnose your Jellyfin/Plex + *Arr stack from one terminal. One binary, 26 commands, JSON output everywhere. Ships with a [`SKILL.md`](https://agentskills.io) following the Agent Skills open standard — so any AI agent on any platform can command your fleet too.

- **`admirarr setup`** — zero to media server in 15 minutes
- **`admirarr doctor`** — 15 diagnostic categories, 34 checks, AI-powered repair
- **`admirarr status`** — your entire fleet at a glance

<br>

## Quick Start

```bash
curl -fsSL https://get.admirarr.dev | sh
admirarr setup      # deploy + wire the stack
admirarr status     # see everything at a glance
```

```
⚓ Fleet Status
──────────────────────────────────────────────
  Services     8/8 online
  Movies       1,247 (1,189 with files)
  Shows        86 (2,341 episodes)
  Downloads    3 active — 42.1 MB/s
  Disk         2.4 TB / 8.0 TB (30%)
  Requests     2 pending
──────────────────────────────────────────────
```

```
⚓ Doctor — 15 categories, 34 checks
──────────────────────────────────────────────
  ✓ Connectivity      All 8 services reachable
  ✓ API Keys          All keys valid
  ✓ Containers        All running
  ✓ Download Clients  qBittorrent connected
  ✗ VPN               Gluetun tunnel down
  ✓ Media Paths       All paths exist
  ...
──────────────────────────────────────────────
  33 passed · 1 failed — run admirarr doctor --fix
```

<br>

## Your Agent Already Knows Admirarr

Admirarr ships a `SKILL.md` following the [Agent Skills](https://agentskills.io) open standard — the same spec used by 26+ platforms. Your agent reads it, discovers Admirarr's commands, and operates your stack.

**Works with:** Claude Code, OpenClaw, OpenCode, Codex, Gemini CLI, Cursor, VS Code, Goose, Aider — and any future SKILL.md-compatible platform.

### Install for your agent

<table>
<tr><th>Platform</th><th>Install command</th></tr>
<tr>
<td><strong>Any agent</strong> (universal)</td>
<td>

```bash
npx skills add maxtechera/admirarr
```

</td>
</tr>
<tr>
<td><strong>Claude Code</strong></td>
<td>

```
/plugin marketplace add maxtechera/admirarr
/plugin install admirarr@admirarr
```

</td>
</tr>
<tr>
<td><strong>OpenClaw</strong></td>
<td>

```bash
clawdhub install maxtechera/admirarr
```

</td>
</tr>
<tr>
<td><strong>OpenCode</strong></td>
<td>

Auto-discovered — clone the repo and OpenCode reads `.claude/skills/` and `AGENTS.md` natively.

</td>
</tr>
<tr>
<td><strong>Cursor / Copilot / Cline</strong></td>
<td>

Auto-discovered — `SKILL.md` and `AGENTS.md` at repo root are read natively.

</td>
</tr>
</table>

> Already installed Admirarr the CLI? Your agent picks up `SKILL.md` automatically — no extra step needed.

### What ships in the box

| File | What it does | Platforms |
|---|---|---|
| **`SKILL.md`** | Agent Skills standard — full command reference | All 26+ platforms |
| **`AGENTS.md`** | Agent reference — commands, patterns, rules | OpenCode, Codex, Gemini CLI, Cursor, Copilot |
| **3 Claude Code agents** | `doctor-fix` (Sonnet), `fleet-status` (Haiku), `content-search` (Haiku) | Claude Code, OpenCode |
| **`/plex-stack` skill** | Dispatches by argument: status, doctor, fix, search, downloads | Claude Code |
| **`.opencode/opencode.jsonc`** | Agents + commands config for OpenCode | OpenCode |
| **Claude Code plugin** | `.claude-plugin/` with marketplace for `/plugin install` | Claude Code |

### `doctor --fix` — two-tier AI repair

```
"My downloads seem stuck"
→ agent calls admirarr doctor -o json
→ finds VPN down
→ calls admirarr restart gluetun
→ re-runs admirarr doctor to verify
```

Built-in fixes run first (container restarts, directory creation, VPN detection). Remaining issues get dispatched to whichever AI agent you have installed — auto-detected.

### How it fits together

```
┌─────────────────────────────────────────────┐
│           Any Agent Platform                 │
│  Claude Code · OpenClaw · Codex · Cursor ... │
└──────────────────┬──────────────────────────┘
                   │ reads SKILL.md
                   ▼
┌─────────────────────────────────────────────┐
│            ⚓ admirarr                       │
│  One binary · JSON output · 26 commands     │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│           Your *Arr Stack                    │
│  Jellyfin · Radarr · Sonarr · Prowlarr      │
│  qBittorrent · Gluetun · Seerr · Bazarr     │
└─────────────────────────────────────────────┘
```

<br>

## Commands

```bash
admirarr status               # Fleet dashboard — services, libraries, queues, disk
admirarr status --live         # Live-updating TUI
admirarr doctor               # 15 diagnostic categories, 34 checks
admirarr doctor --fix          # AI agent detects + fixes issues automatically
admirarr setup                 # Deploy + wire the entire stack (12 phases)

admirarr add-movie "Dune"     # Search → pick → add → downloading
admirarr add-show "Severance" # Same for Sonarr
admirarr search "4k remux"    # Search all Prowlarr indexers

admirarr downloads            # Active torrents (+ pause/resume/remove)
admirarr queue                # Import queues
admirarr missing              # Monitored but not on disk
admirarr movies / shows       # Library with file status
admirarr recent / history     # Recently added / watch history
admirarr requests             # Seerr requests

admirarr indexers             # Indexer health (+ setup/add/remove/test/sync)
admirarr recyclarr sync       # TRaSH Guide quality profiles
admirarr health               # Service warnings
admirarr disk                 # Storage breakdown
admirarr restart <service>    # Restart a service
admirarr logs <service>       # Tail logs
admirarr scan                 # Library scan
```

Every command supports `-o json` for structured output.

<br>

## Diagnostic Engine

15 categories, 34 checks — connectivity, API keys, containers, download clients, disk, media paths, root folders, quality config, indexers, health warnings, VPN, permissions, hardlinks, cross-service wiring, and recyclarr.

```bash
admirarr doctor               # Run all checks
admirarr doctor --fix          # Built-in fixes → AI agent for the rest
```

Every failure includes an actionable fix. `--fix` runs deterministic repairs first (restart containers, create directories, detect VPN credentials), then dispatches remaining issues to your AI agent with full context.

<br>

## Setup

```bash
admirarr setup
```

12 phases: detect environment → select services → deploy via Docker Compose → connectivity check → API key discovery → download clients → root folders → Prowlarr wiring → Seerr wiring → Bazarr wiring → quality profiles → write config.

Idempotent — run again anytime to converge. Detects existing services and wires what's missing.

<br>

## Supported Services

10 default + 14 optional services.

| Service | Role |
|---|---|
| **Jellyfin** | Media server |
| **Radarr** / **Sonarr** | Movie + TV automation |
| **Prowlarr** | Indexer management |
| **qBittorrent** + **Gluetun** | Downloads behind VPN |
| **Seerr** | Media requests |
| **Bazarr** | Subtitles |
| **FlareSolverr** | Cloudflare bypass |
| **Profilarr** | TRaSH Guide quality profiles (GUI) |
| **Watchtower** | Auto-updates |

Want Plex instead? Setup asks. Don't want something? Skip it.

<details>
<summary><strong>Optional services</strong></summary>

Plex, Lidarr, Readarr, Whisparr, SABnzbd, Autobrr, Unpackerr, Recyclarr, Tdarr, Tautulli, Jellystat, Notifiarr, Maintainerr

</details>

<br>

## Why CLI + Agent Skills?

- **CLIs compose** — agents call `admirarr status -o json`, not navigate web UIs
- **SKILL.md is portable** — one file makes Admirarr work on 26+ agent platforms, no per-platform integration
- **One binary, zero deps** — works in SSH, tmux, CI, agent sandboxes
- **Already standard** — Agent Skills is the industry spec, adopted by Claude, OpenAI, Google, Microsoft, GitHub, and more. Admirarr uses what's already there.

<br>

## Why Another CLI?

Your stack has 10+ services, each with its own API, web UI, and config format. No single tool manages all of them.

### The *Arr ecosystem — what Admirarr manages

| Service | What it does | What Admirarr does with it |
|---------|-------------|---------------------------|
| **Jellyfin** / **Plex** | Media server — streams your library | Libraries, watch history, recently added, library scans |
| **Radarr** | Movie automation — monitors, grabs, imports | Search, add movies, queue, missing, quality profiles, health |
| **Sonarr** | TV automation — same as Radarr for shows | Search, add shows, queue, missing, quality profiles, health |
| **Prowlarr** | Indexer manager — searches torrent/usenet sites | Indexer status, add/remove/test/sync indexers |
| **qBittorrent** | Download client — torrents behind VPN | Active downloads, pause/resume/remove, speed |
| **Gluetun** | VPN container — routes downloads through VPN | VPN status, credential detection, restart |
| **Seerr** | Request system — users request movies/shows | View requests, wiring to Radarr/Sonarr/Jellyfin |
| **Bazarr** | Subtitles — auto-downloads subs for your library | Subtitle status, connectivity |
| **Recyclarr** | Quality profiles — syncs TRaSH Guide configs | Sync, verify, instance management |
| **FlareSolverr** | Cloudflare bypass for indexers | Connectivity check |
| **Watchtower** | Auto-updates containers | Container status |
| **+ 14 optional** | Lidarr (music), Readarr (books), Tdarr (transcoding), Tautulli (stats), etc. | Varies by service |

### How tools compare

| Tool | Services | Deploy | Configure | Diagnose | CLI/JSON | Agent Skills |
|------|----------|--------|-----------|----------|----------|--------------|
| Docker Compose | containers only | yes | — | — | — | — |
| Recyclarr/Profilarr | Radarr, Sonarr | — | quality profiles | — | Recyclarr CLI | — |
| Managarr | Radarr, Sonarr, misc | — | browse | — | — | — |
| **Admirarr** | **all 10 + 14 optional** | yes | yes | 34 checks | yes | SKILL.md + 3 agents |

<br>

## Install

```bash
curl -fsSL https://get.admirarr.dev | sh
```

<details>
<summary><strong>Other methods</strong></summary>

```bash
brew install maxtechera/tap/admirarr              # Homebrew
go install github.com/maxtechera/admirarr@latest  # Go
yay -S admirarr-bin                               # Arch AUR
dpkg -i admirarr_*.deb                            # Debian/Ubuntu
irm https://get.admirarr.dev/windows | iex        # Windows PowerShell
```

</details>

<br>

## Contributing

```bash
git clone https://github.com/maxtechera/admirarr.git
cd admirarr && go build -o admirarr . && go test ./...
```

<br>

## License

[MIT](LICENSE)

---

<p align="center">
  <sub>Built with ⚓ by <a href="https://github.com/maxtechera">maxtechera</a></sub>
</p>
