# AGENTS.md — machine contract for loseit-cli

loseit-cli is a read-only Lose It! nutrition extractor. It obtains the data export (a downloaded ZIP or a
cookie fetch), parses the food log, and emits per-day nutrition as JSON. It does **no application** writing —
no daily log, no sync, no upsert; the consuming agent does the storing. The only file it writes locally is
its session-token cache (`token_path`, mode 0600) when it logs in. It never modifies your Lose It account.
**stdout is data; stderr is hints/logs/errors.**

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `2` | Export / parse failure (no token, expired cookie, missing/invalid ZIP, unreadable export, empty `food-logs.csv`) |
| `64` | Usage error (bad flags, bad `--date`) |
| `78` | Config error (unreadable / invalid `config.json`) |
| `1` | Other failure |

## `days` (the core emit)

Parses the export and prints per-day nutrition. A human table by default; `--json` emits the frozen
contract below.

```sh
loseit-cli days --zip export.zip --json --days 7
loseit-cli days --zip export.zip --date 2026-06-16 --days 1
loseit-cli days --json                 # cookie-fetch path (needs a token)
```

| Flag | Meaning | Default |
|---|---|---|
| `--zip PATH` | parse a downloaded export ZIP instead of fetching | — (cookie fetch) |
| `--date` | civil anchor: `today` \| `yesterday` \| `YYYY-MM-DD` | `today` |
| `--days N` | days back from `--date` (inclusive window) | `7` |
| `--json` | emit the frozen per-day JSON contract | off (human table) |

### `days --json` shape (FROZEN)

A JSON **object keyed by ISO date** → nutrition object. Keys are ascending by date. Key order within each
nutrition object is frozen. An empty selection emits `{}`.

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
      {
        "meal": "Breakfast",
        "calories": 225,
        "protein_g": 23,
        "carbs_g": 36,
        "fat_g": 0,
        "items": [
          { "name": "Greek Yogurt", "qty": "1 cup", "calories": 120 }
        ]
      }
    ],
    "loseit_budget": 1663,
    "loseit_under": 1158,
    "exercise_adjustment": 120
  }
}
```

- `loseit_budget`, `loseit_under` (= `loseit_budget − calories_food`), and `exercise_adjustment` appear
  **only** when `daily-calorie-summary.csv` provides them, and **after** `meals`. `loseit_budget`/`loseit_under`
  are emitted together (under is shown even when zero); `exercise_adjustment` is omitted when the day's
  exercise calories are zero.
- All numbers are integers, rounded **half-to-even** (banker's rounding). Day and per-meal totals round the
  summed raw floats; `items[].calories` rounds each row's calorie value.
- Meal order: `Breakfast, Lunch, Dinner, Snacks` first (that order), then any other meals in first-encounter
  order. A blank meal name becomes `Other`. Deleted rows are excluded.

## `login`

Authenticates with email/password and saves a fresh `liauth` session token to `token_path`. POSTs
`username`/`password`/`grant_type=password` (form-encoded) to `login_url` (`api.loseit.com/account/login`);
the reCAPTCHA the web form attaches is **not** required by the API. On success prints a one-line
confirmation to stdout (never the token). Bad credentials / no cookie returned → exit `2`. Credentials come
from `LOSEIT_EMAIL`/`LOSEIT_PASSWORD` or `email`/`password` in `config.json`.

`days` (without `--zip`) auto-logs-in too: if the saved token is missing or expired and credentials are
configured, it logs in, saves the token, and retries once — so the cookie fetch is self-sufficient.

## `config show --json`

The resolved effective config. The password is **never** emitted (only `password_set`). Key order:

```json
{
  "token_path": "~/.config/loseit/token",
  "export_url": "https://www.loseit.com/export/data",
  "login_url": "https://api.loseit.com/account/login",
  "email": "you@example.com",
  "password_set": true,
  "config_path": "<path>"
}
```

`config path` prints just the `config.json` path in use.

## `doctor`

Reports config + whether a token and/or credentials are present. **No network.** Always exits `0` — lacking
a token is not a failure (`--zip` needs none, and credentials enable auto-login); a stderr hint is printed
when neither is available. Never reveals the cookie or password. Key order:

```json
{
  "tokenPresent": false,
  "credentialsPresent": true,
  "exportURL": "https://www.loseit.com/export/data",
  "loginURL": "https://api.loseit.com/account/login",
  "tokenPath": "~/.config/loseit/token",
  "configPath": "<path>",
  "version": "<version>"
}
```

## `version --json`

```json
{ "version": "<version>", "commit": "<sha>", "date": "<iso>", "go": "go1.x" }
```

## Auth model

- **Email/password (recommended):** set `LOSEIT_EMAIL`/`LOSEIT_PASSWORD` (or `email`/`password` in config).
  `login` and `days` obtain a `liauth` cookie from `api.loseit.com/account/login` and save it to
  `token_path`. `days` auto-refreshes on expiry — fully self-sufficient, no captcha.
- `--zip PATH` reads a downloaded export — **no token, no credentials**.
- Manual cookie: put a `liauth` value in `LOSEIT_TOKEN` or the `token_path` file. The cookie fetch sends
  `Cookie: liauth=<t>; fn_auth=<t>`. The cookie expires (~14 days); with credentials set, `days` re-logs-in
  automatically — without them it fails (exit `2`) and you re-supply a cookie or use `--zip`.
