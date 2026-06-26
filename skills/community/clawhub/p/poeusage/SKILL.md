---
name: poeusage
description: Monitor Poe API point balance and usage history from the terminal using poeusage CLI.
version: 0.5.0
metadata:
  openclaw:
    emoji: "📊"
    homepage: https://github.com/rgstephens/poeusage-skill
    requires:
      bins:
        - poeusage
      env:
        - POE_API_KEY
    install:
      - kind: brew
        tap: rgstephens/tap
        formula: poeusage
        bins:
          - poeusage
---

slug: poeusage
version: 0.5.0

A ClawHub skill for monitoring Poe API point balance and usage history via the `poeusage` CLI.

## Install

```bash
brew tap rgstephens/tap
brew install poeusage
```

## Description

`poeusage` is a terminal utility to monitor your Poe API quota, usage history, and spend summaries. It supports JSON/csv/table output modes, pagination, filtering, and shell completion generation.

## CLI Commands

### Global flags

- `--api-key` string (default from `$POE_API_KEY`)
- `--json` bool
- `--plain` bool
- `--no-color` bool
- `--quiet` / `-q` bool
- `--verbose` / `-v` bool
- `--timeout` int (default 30)
- `--help` / `-h` bool
- `--version` bool

### Subcommands

#### `poeusage balance`

Fetch and display current point balance.

Usage:
```sh
poeusage balance [--json] [--plain]
```

- TTY example: `Current balance: 1,500 pts`
- `--plain` example: `1500`
- `--json` example: `{"current_point_balance":1500}`

#### `poeusage history`

Fetch usage history. Auto-paginates by default until all records are retrieved (or until `--limit`).

Usage:
```sh
poeusage history [flags]
```

Flags:

- `--limit` / `-n` int (0 == all)
- `--page-size` int (default 100, max 100)
- `--no-paginate` bool
- `--cursor` string
- `--bot` / `-b` string
- `--type` / `-t` string (`chat`, `api`, `canvas`)
- `--since` string (`YYYY-MM-DD` or unix timestamp)
- `--until` string (`YYYY-MM-DD` or unix timestamp)
- `--output` / `-o` string
- `--format` / `-f` string (`table`, `csv`, `json`)

Notes:
- `--json` is alias for `--format json`
- `--plain` is alias for `--format csv`
- date filters are applied client-side
- with `--no-paginate`, prints `next-cursor: <query_id>` to stderr if more pages exist

Default table output columns:
`TIME`, `BOT`, `TYPE`, `POINTS`, `COST (USD)`

CSV output columns:
`time,bot_name,usage_type,cost_points,cost_usd,query_id,chat_name,input_pts,output_pts,cache_write_pts,cache_discount_pts`

JSON output example:
```json
[
  {
    "bot_name": "Claude-3.5-Sonnet",
    "time": "2024-01-09T14:00:00Z",
    "query_id": "2Nhd9xBFbLcXEwmNj",
    "cost_usd": "0.00075",
    "cost_points": 339,
    "usage_type": "API",
    "chat_name": null,
    "cost_breakdown": {
      "input": 120,
      "output": 219,
      "cache_write": 0,
      "cache_discount": 0,
      "total": 339
    }
  }
]
```

#### `poeusage summary`

Aggregate usage and display cost breakdown. Same filters as `history` plus grouping.

Usage:
```sh
poeusage summary [flags]
```

Flags:

- `--bot` / `-b` string
- `--type` / `-t` string
- `--since` string
- `--until` string
- `--group-by` / `-g` string (`bot`, `type`, `day`, `bot,type`)
- `--format` / `-f` string (`table`, `csv`, `json`)

Default table output columns (group-by bot):
`BOT`, `QUERIES`, `POINTS`, `COST (USD)`

#### `poeusage completion <shell>`

Generate shell completion script.

Usage:
```sh
poeusage completion <bash|zsh|fish>
```

Example:
```sh
poeusage completion zsh > ~/.zsh/completions/_poeusage
```

## I/O contract

- stdout: primary command output
- stderr: diagnostics, progress, warnings, next-cursor hints
- TTY detection controls color and formatting

## Exit codes

- `0`: success
- `1`: runtime error (network/API error)
- `2`: invalid usage
- `3`: auth error (401)

## Configuration

Priority: flags > env > config file > defaults

Env vars:
- `POE_API_KEY`
- `NO_COLOR`
- `POEUSAGE_TIMEOUT`
- `POEUSAGE_PAGE_SIZE`

Config file: `~/.config/poeusage/config.toml`

```toml
# api_key = "..." # not recommended
timeout = 30
page_size = 100
```

## Release

- `make release TAG=v1.0.0`
