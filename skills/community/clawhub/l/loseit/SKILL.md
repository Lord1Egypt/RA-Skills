---
name: loseit
description: >
  Read your Lose It! nutrition from any agent. Logs in with your Lose It
  email/password (self-healing — it obtains and refreshes its own session token),
  fetches your data export, and emits per-day nutrition as JSON — calories,
  protein, carbs, fat, fiber, a per-meal breakdown, and Lose It's own budget /
  under / exercise-adjustment figures. A self-contained, read-only extractor: it
  never changes your Lose It account and does no application writing (no daily log,
  no sync) — the caller decides what to do with the data. The only file it writes
  locally is its own session-token cache (a credential, mode 0600). Single static
  binary, no Python or other runtime. Auth options:
  email/password (recommended — set LOSEIT_EMAIL/LOSEIT_PASSWORD or put them in
  config.json), a downloaded export ZIP (--zip, no credentials), or a saved liauth
  cookie.
metadata:
  openclaw:
    emoji: 🥗
    homepage: https://github.com/stozo04/loseit-cli
    primaryEnv: LOSEIT_EMAIL
    permissions:
      network:
        - "Lose It! login endpoint (api.loseit.com/account/login, HTTPS) — exchange your email/password for a session token"
        - "Lose It! export endpoint (www.loseit.com/export/data, HTTPS) — download your own data export (read-only) using the session token"
      files.read:
        - "config.json — your Lose It credentials (email, password), in the working directory or next to the binary"
        - "token file — the liauth session cookie (default ~/.config/loseit/token; overridable via LOSEIT_TOKEN_PATH)"
        - "--zip file — a downloaded Lose It export ZIP, when the --zip path is used"
      files.write:
        - "token file — the session token obtained at login is saved to token_path (default ~/.config/loseit/token, mode 0600). No other writes; nutrition goes to stdout."
    requires:
      bins: []
      env: []
    envVars:
      - name: LOSEIT_EMAIL
        description: "Lose It account email — for the email/password login path (recommended). Or set it in config.json."
        required: false
      - name: LOSEIT_PASSWORD
        description: "Lose It account password — for the email/password login path. Or set it in config.json. Never printed."
        required: false
---

# Lose It Nutrition — read-only nutrition extractor

Read your **Lose It!** nutrition from any agent. This is a read-only extractor: it never changes your
Lose It account — it obtains the Lose It data export, parses the food log, and prints **per-day
nutrition as JSON** — calories, protein, carbs, fat, fiber, a per-meal breakdown, plus Lose It's own
budget/under/exercise figures. It does **no application writing** — no daily log, no sync; you get the
data and store whatever you care about. The only file it writes locally is its own session-token cache
(`token_path`, mode 0600). Single static binary — **no Python or other runtime**.

> ⚠️ **Read-only** for your Lose It data — it reads the export and prints JSON. It is not a no-write
> tool, though: it caches its `liauth` **session token** (a reusable ~14-day credential) to
> `token_path` (mode 0600), and it reads your **plaintext** email/password from `config.json`. Both
> are secrets — see **Security & secrets** below.

> 🔑 **Self-healing auth.** With your email/password configured, `login` fetches a session token and
> `days` re-logs-in automatically when it expires (~14 days) — no manual cookie juggling. The `--zip`
> and manual-cookie paths still work and need no credentials.

## Install

```bash
# A) Download a release for your OS/arch and put it on PATH:
#    https://github.com/stozo04/loseit-cli/releases
# B) Or with Go (1.24+):
go install github.com/stozo04/loseit-cli/cmd/loseit-cli@latest
```

## Getting your data

Provide your two Lose It credentials — **`email` and `password`** — and nothing else. Put them in
`config.json` (`{ "email": "you@example.com", "password": "your-loseit-password" }`) or export
`LOSEIT_EMAIL`/`LOSEIT_PASSWORD`, then:

```bash
loseit-cli days --json     # logs in automatically when needed, fetches, parses
loseit-cli login           # (optional) explicit login to refresh the saved token
```

No browser, no manual cookie, no captcha — the API doesn't require the one the web form attaches. The
session token is fetched, cached, and refreshed for you; email + password are the only inputs.

### Advanced / fallbacks

Not needed for normal use — they exist as a safety net (no credentials required):

- **Downloaded ZIP:** export from Lose It (Settings → Export), then
  `loseit-cli days --zip ~/Downloads/loseit-export.zip --json`.
- **Manual cookie:** save a `liauth` cookie (loseit.com → F12 → Application → Cookies) to
  `~/.config/loseit/token` (or set `LOSEIT_TOKEN`), then `loseit-cli days --json`. Works until it
  expires; the email/password path refreshes it for you.

## Commands

```bash
loseit-cli days --zip export.zip --days 7          # human table for the last 7 days
loseit-cli days --zip export.zip --json --days 7    # the frozen per-day JSON contract
loseit-cli days --zip export.zip --date 2026-06-16 --days 1
loseit-cli days --json --days 7                     # login (email/pw) + fetch + parse
loseit-cli login                                    # log in and save a fresh session token
loseit-cli config show                              # resolved config (password never shown)
loseit-cli doctor                                   # config + token/credentials presence (no network)
loseit-cli version                                  # build metadata (also --version)
loseit-cli completion bash|zsh|fish|powershell      # shell completion
```

### `days --json` output

A JSON object keyed by ISO date → nutrition object (empty selection → `{}`):

```json
{
  "2026-06-16": {
    "source": "Lose It export",
    "calories_food": 505,
    "protein_g": 75,
    "carbs_g": 36,
    "fat_g": 6,
    "fiber_g": 3,
    "meals": [
      { "meal": "Breakfast", "calories": 225, "protein_g": 23, "carbs_g": 36, "fat_g": 0,
        "items": [ { "name": "Greek Yogurt", "qty": "1 cup", "calories": 120 } ] }
    ],
    "loseit_budget": 1663,
    "loseit_under": 1158,
    "exercise_adjustment": 120
  }
}
```

`loseit_budget` / `loseit_under` / `exercise_adjustment` appear only when the daily summary provides
them, after `meals`. Numbers are integers (banker's rounding). See **AGENTS.md** for the full
contract and exit codes.

## Security & secrets

This skill handles two **sensitive** local files. Treat both as you would any password:

- **`config.json`** holds your Lose It **email and password in plaintext**. It is **gitignored** —
  never commit it, and don't place it in a shared, world-readable, or backed-up directory. On a shared
  machine, prefer the `LOSEIT_EMAIL` / `LOSEIT_PASSWORD` environment variables over a file on disk.
- **The session-token cache** (`token_path`, default `~/.config/loseit/token`) holds the `liauth`
  cookie — a **reusable, ~14-day session credential**. It is written **owner-only (`0600`)** in an
  owner-only directory (`0700`), is **gitignored**, and is never printed. Anyone who can read it can
  pull your data until it expires, so keep it off shared disks and out of backups.

Apart from that one cache file, nothing is persisted. All network traffic is HTTPS to Lose It's own
login/export endpoints, and no secret reaches stdout, stderr, or logs at any verbosity.

## Conventions

- **stdout is parseable**; human hints and logs go to **stderr**, never interleaved.
- **Exit codes:** `0` success, `2` export/parse failure (no/expired token, bad ZIP), `64` usage
  error, `78` config error.
- **Read-only for your data:** the tool reads the export and prints JSON and never modifies your Lose
  It account; the only file it writes locally is its session-token cache (`token_path`, 0600).
- **Secrets:** the token file and `config.json` (which holds your email/password in plaintext) are
  gitignored — never commit them and keep them owner-only; on shared machines prefer env vars. The
  password and the cookie/token value are never printed.
