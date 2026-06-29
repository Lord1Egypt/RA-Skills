---
name: google-health-cli
description: >
  Read your Google Health data from any agent. Lists data points for every Google
  Health data type (heart rate, resting heart rate, sleep, steps, distance, weight,
  blood oxygen, VO2 max, exercise, and more), returns server-side daily roll-ups
  (one reconciled total per day), gives a parsed view of exercise sessions, and can
  GET any read-only v4 API path. A self-contained, read-only
  client for the Google Health v4 API: authenticates via OAuth2 (token cached
  locally and auto-refreshed) and emits JSON. It does NO filtering, merging, or
  writing — the caller decides what to do with the data. Single static binary, no
  Python or other runtime. NOTE: needs your own Google Cloud OAuth client and a
  one-time interactive browser login; runs headless afterward.
metadata:
  openclaw:
    emoji: 🩺
    homepage: https://github.com/stozo04/google-health-cli
    primaryEnv: GOOGLE_HEALTH_CLIENT_ID
    permissions:
      network:
        - "Google OAuth2 (accounts.google.com, oauth2.googleapis.com) — one-time interactive login and automatic token refresh"
        - "Google Health API (health.googleapis.com, HTTPS) — read your health & fitness data points (read-only scopes only)"
      files.read:
        - "config.json — OAuth client id/secret and optional settings; discovered via --config, then $GOOGLE_HEALTH_CONFIG, then ./config.json, then next to the executable, then <user config dir>/google-health-cli/config.json"
        - "token cache — the cached OAuth token (default <user cache dir>/google-health-cli/token.json, a non-roaming location; overridable via GOOGLE_HEALTH_TOKEN_CACHE; a token left at the older <user config dir> path is migrated forward automatically)"
      files.write:
        - "token cache — written at login and re-written when the token auto-refreshes (no other files are written)"
    requires:
      bins: []
      env:
        - GOOGLE_HEALTH_CLIENT_ID
        - GOOGLE_HEALTH_CLIENT_SECRET
    envVars:
      - name: GOOGLE_HEALTH_CLIENT_ID
        description: "Google Cloud OAuth client ID (Desktop app type). Create one once — see the repo's OAUTH_SETUP.md."
        required: true
      - name: GOOGLE_HEALTH_CLIENT_SECRET
        description: "OAuth client secret for that client."
        required: true
      - name: GOOGLE_HEALTH_CONFIG
        description: "Path to a config.json holding client_id/client_secret (alternative to the env vars)."
        required: false
      - name: GOOGLE_HEALTH_TOKEN_CACHE
        description: "Override the cached-token path (default <user cache dir>/google-health-cli/token.json)."
        required: false
      - name: GOOGLE_HEALTH_BASE_URL
        description: "Override the API base URL (default https://health.googleapis.com)."
        required: false
---

# Google Health — read-only data extractor

Read your **Google Health** data from any agent. This is a generic, **read-only** client
for the Google Health v4 API: it authenticates, pulls data points for any data type, and
prints **JSON**. It does no filtering, merging, or interpretation — you get the data and
parse whatever you care about. Single static binary — **no Python or other runtime**.

> ⚠️ **Read-only.** It requests only read-only Google Health scopes and never writes your
> health data.

> 🔒 **Privacy — sensitive health data leaves on stdout.** Every `data list`, `rollup daily`,
> `sessions`, and `api get` prints your **personal health information** (heart rate, sleep, weight,
> exercise, blood oxygen, profile, …) to **stdout** as JSON. In an agent or pipeline, stdout may be
> **logged, summarized, persisted, or transmitted** to other tools, model providers, or third
> parties. Treat this output as sensitive PII: only run it in contexts you trust to handle health
> data, and do not persist or forward it unless you intend to. The tool never sends your data
> anywhere itself (it only talks to Google's API over HTTPS) — what happens to stdout is the
> caller's responsibility. Every data-emitting command also prints a one-line
> **privacy notice to stderr** at run time as an execution-time reminder (it stays on stderr, never
> on the JSON stdout).

> 🧭 **Data minimization & consent.** Request only the **data types** and the **narrowest time
> window** you actually need (`--days`/`--date`/`--from`/`--to`, not `--all`); prefer the typed
> `data`/`rollup`/`sessions` commands over `api get`; and don't persist or forward the output beyond
> the task at hand. Run this only against an account whose owner has **knowingly consented** to
> having their health data read by this agent — the one-time `auth login` is the owner consenting to
> *read-only access for the tool*, not consent for a downstream agent to collect, retain, or transmit
> that data more broadly.

> 🩺 **`doctor` prints local environment metadata.** The `doctor` JSON includes your
> **token-cache and config file paths**, the configured **account** (`user`), and the API
> **base URL** — local filesystem layout and account identifiers rather than health data, but
> still **local environment metadata** that an agent or pipeline may log, forward, or persist.
> It exists to diagnose *your own* setup; treat its output like any other local path/account
> detail and don't paste it into untrusted contexts.

## Setup (one time)

Unlike a simple email/password tool, Google Health uses OAuth, so first-time setup needs a
human in a browser **once**. After that it runs headless (the token auto-refreshes).

1. **Install** the binary:
   ```bash
   # A) Download a release for your OS/arch and put it on PATH:
   #    https://github.com/stozo04/google-health-cli/releases
   # B) Or with Go (1.25+):
   go install github.com/stozo04/google-health-cli/cmd/google-health-cli@latest
   ```
2. **Create a Google Cloud OAuth client** (Desktop app, read-only Health scopes, ~10 min,
   no fees). Full walkthrough: the repo's **OAUTH_SETUP.md**.
3. **Provide the client** via `GOOGLE_HEALTH_CLIENT_ID` / `GOOGLE_HEALTH_CLIENT_SECRET`
   (or a `config.json` with those keys in the working directory).
4. **Authorize once** (opens a browser, asks a human to consent to read-only access):
   ```bash
   google-health-cli auth login
   google-health-cli doctor        # expect "tokenValid": true
   ```
   The token is cached `0600` and auto-refreshed; every later run is headless.

## Credentials

| Variable | Required | Notes |
|---|---|---|
| `GOOGLE_HEALTH_CLIENT_ID` | ✓ | OAuth client ID (Desktop app) |
| `GOOGLE_HEALTH_CLIENT_SECRET` | ✓ | OAuth client secret |
| `GOOGLE_HEALTH_CONFIG` | — | Path to a `config.json` holding the above instead |
| `GOOGLE_HEALTH_TOKEN_CACHE` | — | Override the cached-token path |
| `GOOGLE_HEALTH_BASE_URL` | — | Override the API base URL |

`config.json` (gitignored) is an alternative to the env vars:

```json
{
  "client_id": "PASTE_CLIENT_ID",
  "client_secret": "PASTE_CLIENT_SECRET"
}
```

> 🔑 **Protect your credentials.** The OAuth `client_id`/`client_secret` and the cached **token**
> are sensitive secrets stored on disk in plaintext (`config.json` / `token.json`, written `0600`).
> They're gitignored — keep it that way: never commit them, copy them into a shared folder, back them
> up to an untrusted location, or paste them into logs or chat. Rotate the OAuth client (and run
> `auth logout`) if one may have leaked.

## Commands

### Discover the data types

```bash
google-health-cli types list                 # all types ( * = supports list )
google-health-cli types describe heart-rate   # one type's record shape, scope, time field
```

### Read data points (the core)

```bash
google-health-cli data list heart-rate --days 1        # last 1 day
google-health-cli data list sleep --days 14             # last 14 days
google-health-cli data list daily-resting-heart-rate --days 30
google-health-cli data list steps --date 2026-06-16     # one civil day
google-health-cli data list weight --from 2026-01-01T00:00:00Z --to 2026-07-01T00:00:00Z
google-health-cli data list distance --all              # everything, no time filter
```

stdout is **always a JSON array of the raw data points** (verbatim from the API); a one-line
count goes to stderr. Window flags (precedence: `--all` > `--from`/`--to` > `--date`/`--days`):
`--date today|yesterday|YYYY-MM-DD`, `--days N` (default 7), `--from`/`--to` (RFC3339, together),
`--all` (no filter).

Example (`data list daily-resting-heart-rate`):

```json
[
  {
    "dataSource": { "platform": "FITBIT", "device": { "displayName": "Google Pixel Watch 4 (45mm)" } },
    "dailyRestingHeartRate": { "date": { "year": 2026, "month": 6, "day": 17 }, "beatsPerMinute": "78" }
  }
]
```

A few types are roll-up/reconcile-only and can't be `list`ed (`types list` marks listable ones
with `*`); read those with `rollup daily <type>` instead (below).

### Daily roll-ups (server-side totals)

```bash
google-health-cli rollup daily steps --days 7           # one reconciled total per civil day
google-health-cli rollup daily active-minutes --days 7   # a roll-up-only type (no `data list`)
```

`rollup daily <type>` returns the API's **daily roll-up** rows — one value per civil (local)
calendar day — instead of the raw per-minute/per-sample points `data list` returns. It's the cheap
way to get daily totals (e.g. a `steps` total per day rather than a per-minute dump) and the **only**
way to read the roll-up-only types that have no `list` op (`active-minutes`, `total-calories`,
`floors`, `calories-in-heart-rate-zone`, `time-in-heart-rate-zone`). stdout is a JSON array of the
raw roll-up rows; an `N <type> daily rollup(s)` count goes to stderr. Each value is **reconciled
across data sources** (and excludes off-wrist intervals), so it is *not* a naive sum of `data list`
points. Window flags mirror `data list` minus `--all` (the range is required).

```json
[
  {
    "civilStartTime": { "date": { "year": 2026, "month": 6, "day": 16 }, "time": {} },
    "civilEndTime":   { "date": { "year": 2026, "month": 6, "day": 17 }, "time": {} },
    "steps": { "countSum": "8000" }
  }
]
```

### Parsed exercise sessions (convenience)

```bash
google-health-cli sessions --days 14 --json    # flattened exercise rows
google-health-cli sessions --raw               # raw exercise data points
```

```json
[
  { "date": "2026-06-16", "exercise_type": "ELLIPTICAL", "duration_min": 35,
    "avg_hr": 130, "calories": 236, "platform": "FITBIT" }
]
```

`sessions` returns **all** exercise types (no filtering); the caller keeps what it wants.

### Raw read-only API access

```bash
google-health-cli api get /v4/users/me/profile     # GET any read-only v4 path
google-health-cli api get /v4/users/me/settings
```

> ⚠️ **Sensitive endpoints — broader than the typed metrics.** `api get` can read **any**
> read-only v4 path, including `users/me/profile` and `users/me/settings` — account, identity, and
> settings data that the typed commands don't surface. Its responses are personal data printed to
> stdout, so the same **Privacy** caution above applies, and the broad reach makes
> over-collection easy. It stays **GET-only** (no path can write or delete) and is
> **constrained to the read-only v4 surface** (`/v4/...`): a non-`v4/` path, an absolute URL, or a
> `..` traversal is rejected (exit 64) before any request is made. Still, prefer the typed
> `data`/`rollup`/`sessions` commands and reach for `api get` only when you need an endpoint they
> don't model.

## Full command reference

| Command | What it does | `--json` |
|---|---|---|
| `auth login \| logout \| status` | OAuth login (one-time browser), token mgmt | `status` |
| `doctor` | Config + token validity; reports `configFound`/`clientIdLoaded` and exits non-zero (78) when no config / no `client_id` is found, else 2 if not authed | always |
| `types list \| describe <type>` | Inspect the data-type catalog (no network) | ✓ |
| `data list <type>` | List data points for a type (always JSON) | n/a (always) |
| `rollup daily <type>` | Server-side daily totals, reconciled per civil day | n/a (always) |
| `sessions [--days N] [--raw]` | Parsed exercise sessions (convenience) | ✓ |
| `api get <path>` | Raw read-only GET of any v4 path | n/a |
| `config show \| path` | Inspect resolved config (`client_secret` masked) | `show` |
| `version` | Build metadata (also `--version`) | ✓ |
| `completion <shell>` | Shell completion (bash/zsh/fish/powershell) | — |

## Conventions

- **stdout is parseable**; human hints, counts, and logs go to **stderr**, never interleaved.
- **Exit codes:** `0` success, `2` auth/API failure (incl. `doctor` when unauthenticated),
  `64` usage error (incl. an expired token with no OAuth client credentials to refresh it),
  `78` config error. An expired token plus an undiscoverable/credential-less config fails fast
  with an actionable message — not the cryptic `oauth2 "Could not determine client ID"` error.
- **Read-only:** six read-only `googlehealth.*.readonly` scopes; no write operations exist.
- **Secrets:** `config.json` and the token cache are gitignored — never commit them.
- **Time-filter formats** are handled for you per data type (civil wall-clock, RFC3339
  instant, or date-only). If a type rejects server-side filtering, re-run with `--all`.

See the repo's **AGENTS.md** for the exact `--json` shapes and exit-code contract.
