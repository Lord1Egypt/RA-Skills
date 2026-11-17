🌐 English | [中文](README.zh-CN.md)

<p align="center">
  <img src="./icon/appIcon.png" alt="App Logo" width="20%">
</p>

# Outlook Calendar Management

Manage Outlook calendar events through conversation with an AI agent. The agent understands the request; this local Python CLI validates explicit inputs and calls Microsoft Graph. It supports personal outlook.com and Microsoft 365 accounts, recurring events, reminders, free-time queries, and English/Chinese output. No MCP server or background service is required.

Version **3.0.0** separates language understanding from execution. The CLI accepts absolute dates and structured recurrence patterns. Local `context` and `date` helpers provide the current timezone/clock and deterministic calendar arithmetic, so the agent can normalize a request before writing and reuse the same values during retries.

## Quick start

Place the complete project folder in your agent's skill directory, or run it directly with Python 3.10+. [SKILL.md](SKILL.md) is the agent entrypoint.

```bash
# Local helpers: no calendar access or sign-in required.
python scripts/outlook_cal.py context --timezone Asia/Shanghai --json
python scripts/outlook_cal.py date --base 2026-09-07 --days 4 --json

# Sign in for calendar commands; follow the displayed device-code instructions.
python scripts/outlook_setup.py

# These dates are examples; replace them with your intended absolute dates.
python scripts/outlook_cal.py list --from 2026-09-09 --days 7 --timezone Asia/Shanghai --json
python scripts/outlook_cal.py add "Planning" "2026-09-11 15:00" "2026-09-11 15:30" --remind 10 --timezone Asia/Shanghai --json
python scripts/outlook_cal.py free 2026-09-11 --from 14:00 --to 17:00 --timezone Asia/Shanghai --json
```

Login and calendar commands install missing `requests`, `msal`, and `tzdata` dependencies automatically. Offline helpers do not install packages; when regional timezone data is unavailable, install it with the same interpreter: `python -m pip install tzdata`. Device-code sign-in stores credentials at `~/.outlook_cal_token.json`; the tool renews the login when possible. See [configuration](references/configuration.md) for account and Azure app setup.

## Responsibilities

| AI agent | Python backend |
|---|---|
| Interpret relative language and conversation context | Return current clock/timezone and compute explicit date offsets |
| Select the event, requested fields, and occurrence/series scope | Validate IDs supplied to operations, input formats, ranges, and recurrence structure |
| Resolve material ambiguity and reuse existing authorization | Convert named timezones and all-day boundaries |
| Normalize absolute values and retain them for retries | Authenticate, paginate API results, apply retry rules, and return JSON |
| Verify the requested result and report it accurately | Return server data and structured errors |

For example, “Am I free this Friday 14:00–17:00?” is still valid conversational input. The agent reads `context`, adds four days to its Monday `week_start`, then passes the resulting date to `free`. The backend itself rejects strings such as `this friday` or `今天下午2点`.

## Explicit command contract

- Dates are `YYYY-MM-DD`; timed values are `YYYY-MM-DD HH:MM` or `YYYY-MM-DDTHH:MM`, with zero padding. Timezone is supplied separately using `--timezone` with an IANA or Windows name; absent that option, local detection applies.
- `list` requires `--from` or a creation filter. `free` requires a date. The old `today`/`tomorrow`/`week` commands and `--past` have been removed.
- Timed creation requires both start and end; all-day creation requires `--all-day`. Converting between types requires explicit start and end.
- Recurrence uses a Graph pattern JSON object through `--repeat` or `--repeat-file`. Natural-language rules are no longer parsed. Use the file form to avoid shell quoting problems.
- `--json` yields one JSON value on stdout; warnings and diagnostics go to stderr. Decode JSON to recover Unicode. `--lang zh|en` changes human text, not field names.
- Timed operations use the effective timezone. All-day dates use the mailbox timezone when accessible, otherwise the effective timezone, to preserve their calendar-date meaning in Outlook.

Read the [command reference](references/commands.md) and [recurrence guide](references/recurring-events.md) for complete options. [DEVELOPMENT.md](DEVELOPMENT.md) describes implementation boundaries and offline tests.
