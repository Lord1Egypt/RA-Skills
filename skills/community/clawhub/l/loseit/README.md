# loseit-cli

The **nutrition** counterpart to [`speediance-cli`](https://github.com/stozo04/speediance-cli) (strength) and [`google-health-cli`](https://github.com/stozo04/google-health-cli) (cardio).

A self-contained, **read-only** extractor for the **Lose It!** data export. It reads the export and
**emits per-day nutrition as JSON** — calories, **protein**, carbs, fat, **fiber**, a per-meal
breakdown, and Lose It's own budget / under / exercise-adjustment figures. "Read-only" means it
**never creates, changes, or deletes anything in your Lose It account**, and does no application
storage (no daily log, no sync) — the consuming agent does that. Locally it writes exactly **one**
file: its own session-token cache (a credential — see [Security & secrets](#security--secrets)).
Single static binary — **no Python runtime**.

## How it works

```
Lose It export ZIP  ── from --zip PATH, or GET /export/data with the liauth cookie
        │
        ▼
  food-logs.csv  (Date, Meal, Calories, Protein, Carbs, Fat, Fiber, …)
  daily-calorie-summary.csv  (Date, Food cals, Exercise cals, Budget cals)
        │
        ▼
  aggregate per day + per meal  →  per-day nutrition JSON  (stdout)
```

That's it — download, unzip, parse, print. No GWT-RPC, no Playwright, pure stdlib + cobra.

## Install

```sh
# A) Download a release for your OS/arch and put it on PATH:
#    https://github.com/stozo04/loseit-cli/releases
# B) Or with Go (1.24+):
go install github.com/stozo04/loseit-cli/cmd/loseit-cli@latest
```

## Getting your data

Set your two Lose It credentials — **`email` and `password`** — and that's it:

```sh
# config.json — holds your credentials in PLAINTEXT; keep it private (see "Security & secrets").
# Place it next to the binary or in the working directory. It is gitignored.
{ "email": "you@example.com", "password": "your-loseit-password" }
```

(or export `LOSEIT_EMAIL` / `LOSEIT_PASSWORD` instead), then:

```sh
loseit-cli days --json          # logs in automatically when needed, fetches, parses
loseit-cli login                # (optional) explicit login to refresh the saved token
```

`days` logs in on first use, caches the returned `liauth` session cookie, and re-logs in on its own
when it expires (~14 days) — no browser, no manual cookie copy, no captcha (the API doesn't require
the one the web form attaches). Email + password are the **only** inputs you supply; everything else
is handled for you.

## Usage

```sh
loseit-cli days --zip export.zip --days 7           # human table
loseit-cli days --zip export.zip --json --days 7     # the frozen JSON contract
loseit-cli days --zip export.zip --date 2026-06-16 --days 1
loseit-cli days --json                               # login + fetch (email/password in config)
loseit-cli login                                     # log in and save a fresh session token
loseit-cli config show                               # resolved config (password never shown)
loseit-cli doctor                                    # config + token/credentials presence (no network)
loseit-cli version                                   # build metadata
```

## What it emits (`days --json`)

A JSON object keyed by ISO date → nutrition object (empty → `{}`):

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

See **AGENTS.md** for the full contract (key order, rounding, exit codes) and **SKILL.md** for the
ClawHub skill.

## Config

The only thing you configure is your Lose It **email** and **password**:

```json
{
  "email": "you@example.com",
  "password": "your-loseit-password"
}
```

`config.json` is **gitignored** — keep it local; the password is never printed (`config show` emits
`password_set` only). Discovery precedence: `--config` flag > `LOSEIT_CONFIG` env > `./config.json` >
next to the executable. Everything else (the session token, the login/export endpoints) is handled by
the binary and needs no configuration — note the session token **is cached to disk** as an owner-only
(`0600`) secret (see below).

## Security & secrets

This tool handles two **sensitive** local files. Treat both as you would any password:

- **`config.json`** holds your Lose It **email and password in plaintext**. It is **gitignored** —
  never commit it, and don't drop it in a shared, world-readable, or backed-up location. On a shared
  machine, prefer the `LOSEIT_EMAIL` / `LOSEIT_PASSWORD` environment variables over a file on disk.
- **The session-token cache** (`token_path`, default `~/.config/loseit/token`) holds the `liauth`
  cookie — a **reusable, ~14-day session credential** for your account. It is written **owner-only
  (`0600`)** inside an owner-only directory (`0700`), is **gitignored**, and is never printed. Anyone
  who can read it can pull your data until it expires, so keep it off shared disks and out of backups.

Apart from that one cache file, the tool persists nothing, makes no network calls beyond Lose It's own
login/export endpoints over HTTPS, and prints **no secret** to stdout, stderr, or logs (`config show`
emits only `password_set`; the password and token value are never shown). It is read-only with respect
to your Lose It account — it never modifies data there.

## Advanced / fallbacks

You should not need any of these for normal use — they exist as a safety net and for testing.

**Fallback paths (no credentials):**

- **Downloaded ZIP:** export your data from Lose It (Settings → Export), then parse it directly:
  ```sh
  loseit-cli days --zip ~/Downloads/loseit-export.zip --json
  ```
- **Manual cookie:** save a `liauth` cookie (loseit.com → F12 → Application → Cookies) to
  `~/.config/loseit/token` (or set `LOSEIT_TOKEN`), then `loseit-cli days --json`. Works until the
  cookie expires; the email/password path refreshes it for you.

**Environment overrides (break-glass / testing):** `LOSEIT_EMAIL` and `LOSEIT_PASSWORD` mirror the
config keys. The rest are rarely needed — `LOSEIT_TOKEN` (a `liauth` cookie value), `LOSEIT_CONFIG`
(config path), `LOSEIT_TOKEN_PATH` (token cache location), and `LOSEIT_EXPORT_URL` / `LOSEIT_LOGIN_URL`
(endpoint overrides; the defaults are baked in).

## Notes

- **Read-only against your Lose It account** — it only downloads and reads your export; the consuming
  agent stores nutrition. The one file it writes locally is its session-token cache (see
  [Security & secrets](#security--secrets)).
- `config.json` (your email/password) and the token file are **secrets** — gitignored, never commit
  them, keep them owner-only; the password and cookie are never printed.
- The export endpoint (`GET https://www.loseit.com/export/data`) and the `liauth` cookie scheme were
  learned from the MIT-licensed [RichClarkeAI/loseit-cli](https://github.com/RichClarkeAI/loseit-cli).
  Unofficial path; a Lose It web change could break it, but `/export/data` is first-party and fairly
  stable.
