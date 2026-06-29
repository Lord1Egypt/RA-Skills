# google-health-cli

A single, statically-compiled Go binary that reads your **Google Health** data over read-only OAuth2 and
emits it as JSON. It is a generic, **self-contained** extractor: it owns the OAuth login and the v4 REST
wire, exposes every Google Health data type, and does **no** filtering or interpretation — every consuming
agent or script gets the raw data and parses whatever it cares about.

No Python interpreter and no external helper binary are required.

## How it works

```
google-health-cli auth login           # read-only OAuth2 in the browser, once
        │   token cached 0600, auto-refreshed thereafter
        ▼
google-health-cli data list <type> --days 7
        │   GET https://health.googleapis.com/v4/users/me/dataTypes/<type>/dataPoints
        │       ?filter=<time window on the type's default time field>
        ▼
   JSON array of the raw data points on stdout   →   your agent parses it
```

The tool returns the data points exactly as the API does. It does not merge, label, filter by activity,
or derive anything — those are the consumer's job.

## Install

Download a binary from the [releases page](https://github.com/stozo04/google-health-cli/releases), or:

```sh
go install github.com/stozo04/google-health-cli/cmd/google-health-cli@latest
```

## Setup

1. Create a Google Cloud OAuth client and authorize the tool (one time, ~10 min). See **[OAUTH_SETUP.md](OAUTH_SETUP.md)**.
2. `copy config.example.json config.json` and fill in `client_id` and `client_secret`.
3. Authorize and confirm:
   ```sh
   google-health-cli auth login     # opens a browser, read-only scopes, caches a token
   google-health-cli doctor         # expect  "tokenValid": true
   ```

## Usage

```sh
google-health-cli types list                      # all data types you can read
google-health-cli types describe heart-rate        # one type's record shape, scope, time field

google-health-cli data list heart-rate --days 1    # data points for a type, last 1 day
google-health-cli data list sleep --days 14         # sleep sessions, last 14 days
google-health-cli data list steps --date 2026-06-16 # a specific civil day
google-health-cli data list weight --from 2026-01-01T00:00:00Z --to 2026-07-01T00:00:00Z
google-health-cli data list daily-resting-heart-rate --all   # everything, no time filter

google-health-cli rollup daily steps --days 7       # server-side daily totals (not 1 MB of raw points)
google-health-cli rollup daily active-minutes --days 7  # a rollup-only type (no `data list`)

google-health-cli sessions --days 14               # parsed exercise sessions (convenience)
google-health-cli sessions --raw                    # raw exercise data points
google-health-cli api get /v4/users/me/profile      # raw read-only GET for anything else

google-health-cli auth login | logout | status
google-health-cli doctor [--json]
google-health-cli config show [--json] | config path
google-health-cli version [--json]
google-health-cli completion bash|zsh|fish|powershell
```

stdout is data; human hints, counts, and logs go to stderr. `data list` always prints a JSON array;
`--json` on the other commands switches them to machine-readable output.

## Data types and time windows

`types list` prints all of them (the catalog is embedded — no network call). Each type belongs to a record
family that determines its time-filter format; the tool builds the right filter automatically:

| Family | Time field | Filter value | Examples |
|---|---|---|---|
| Interval / Session | `…civil_start_time` | civil wall-clock (no zone) | exercise, steps, distance, hydration-log |
| Sample | `…sample_time.physical_time` | RFC3339 instant (UTC) | heart-rate, weight, oxygen-saturation |
| Daily | `…date` | date only (`YYYY-MM-DD`) | daily-resting-heart-rate, daily-vo2-max |

Notes:
- **Window flags** (in precedence order): `--all` (no filter) > `--from`/`--to` (explicit RFC3339) >
  `--date`/`--days` (a civil window, default: last 7 days ending today).
- **`sleep`** filters on `civil_end_time` (its start time is not a valid filter member) — handled for you.
- A few types are **rollup/reconcile-only** and cannot be listed (e.g. `total-calories`,
  `time-in-heart-rate-zone`). `data list` rejects them with a clear message; `types list` marks the
  listable ones with `*`. Read them with **`rollup daily <type>`** instead.
- If a type rejects server-side filtering, re-run with `--all` and filter client-side.
- **`rollup daily <type>`** returns one server-reconciled value per civil day (a `dailyRollUp` query) —
  the cheap way to get daily totals and the only way to reach the rollup-only types. The value is
  reconciled across data sources, so it is *not* a naive sum of `data list` points.

## Configuration

`config.json` is discovered via `--config` → `$GOOGLE_HEALTH_CONFIG` → `./config.json` → next to the
executable → `<user config dir>/google-health-cli/config.json` (so the tool works from any directory
without `--config` or the env var). Precedence is flags > env > file > defaults.

If the cached token has expired and none of those locations yields OAuth `client_id`/`client_secret`, API
commands fail fast with an actionable error (exit `64`) instead of a cryptic `oauth2 "Could not determine
client ID"` failure. Run `google-health-cli doctor` to see `configFound` / `clientIdLoaded` and where it
looked.

| Key | Default | Env override |
|---|---|---|
| `client_id` | `""` | `GOOGLE_HEALTH_CLIENT_ID` |
| `client_secret` | `""` | `GOOGLE_HEALTH_CLIENT_SECRET` |
| `base_url` | `https://health.googleapis.com` | `GOOGLE_HEALTH_BASE_URL` |
| `user` | `users/me` | — |
| `token_cache` | `<user cache dir>/google-health-cli/token.json` (non-roaming) | `GOOGLE_HEALTH_TOKEN_CACHE` |
| `scopes` | the six read-only Google Health scopes (see below) | — |

`config.json` and the token cache hold credentials — they are written `0600` and must never be committed.
The token cache lives under the **user cache dir** (`%LocalAppData%` on Windows, `~/.cache` on Linux), not
the config dir: a token is regenerable state, not config, and the cache dir does not roam across machines.
A token left at the older `<user config dir>` location is migrated forward automatically on first run, so
upgrading users keep their session without re-authenticating.

## Notes

- **Privacy, data minimization & consent.** stdout carries sensitive health PII (and, via `api get`,
  profile/settings) that a downstream agent may log, persist, or transmit — request the narrowest window
  and only the data types you need, and run only against an account whose owner has consented to having
  their health data read. The OAuth `client_id`/`client_secret` and the cached token are sensitive secrets
  stored on disk in plaintext — keep them `0600`, gitignored, and out of shared folders, backups, and logs.
  Every data-emitting command prints a one-line privacy notice to stderr at run time, and `api get` is
  constrained to read-only `/v4/` paths (a non-`v4/` path, absolute URL, or `..` traversal is rejected).
  See **[SKILL.md](SKILL.md)** and **[AGENTS.md](AGENTS.md)** for the full guidance.
- **Read-only.** The tool requests only read scopes and never mutates your data. The six scopes are the
  read-only forms of: profile, settings, activity & fitness, health metrics & measurements, sleep, nutrition.
- The OAuth token is cached locally (`0600`) and auto-refreshed; the refreshed token is re-persisted so it
  stays valid between runs. The only network calls are Google OAuth + the Health API.
- For agent/automation consumers, see **[AGENTS.md](AGENTS.md)** for the `--json` shapes and exit codes.
