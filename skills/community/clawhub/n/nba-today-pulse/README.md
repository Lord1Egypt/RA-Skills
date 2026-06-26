# NBA Today Pulse v15

Version: `1.0.15`

`nba-today-pulse-v15` is the public skill-only OpenClaw bundle built from the current `NBA_TR` runtime after the wrapper rollback. It keeps the stable public skill key `nba-today-pulse` and packages one bundled Python command wrapper.

## What Changed in 1.0.15

- Rolls ordinary `day / stats_day / pregame / live / post / injury` behavior back toward the faster proven wrapper path used before official-report mixing expanded.
- Keeps `official_report` as a separate explicit route instead of blending official-story prompts or story background back into normal `day / pregame / post` output.
- Retains the explicit single-game `live` fast path: scoreboard, ESPN summary, NBA live boxscore, key-player sections, scored play-digest lines, and recent-run summaries stay in; slower full-detail enrichment remains deferred unless the user explicitly asks for it.
- Keeps bilingual request handling: English prompts should stay in English with canonical NBA names, while Chinese prompts should keep Chinese section labels and controlled Chinese name mappings where available.
- Keeps the public release package review-safe: no credential requirements, no public persistent-cache controls, and no test-only provider override settings.

## Supported Requests

- Daily NBA status for the requestor's local date
- Day-level stat leaders for completed games
- Single-game and multi-game pregame previews
- Single-game live game flow
- Single-game postgame recap
- Team or matchup injury report
- NBA.com official report summary as an explicit separate route, including direct `nba.com/game/...` URLs

## Runtime

Use the bundled entrypoint:

```bash
python3 {baseDir}/tools/nba_today_command.py --command "<raw request>" --tz "<resolved timezone>"
```

If timezone is not known, ask once for a city or IANA timezone. Known-timezone paths should inject `--tz` explicitly.

This public bundle is instruction-only. It does not install packages, download extra archives, or run a secondary installer. The host executes the bundled Python files in place through the single public entrypoint above.

## Data Access

The bundle makes outbound HTTP requests only to public NBA reporting sources:

- ESPN public JSON endpoints
- NBA.com public stats and live JSON endpoints
- NBA.com public game pages for official stories
- Official NBA injury-report listing and report PDFs

Remote PDF parsing is limited to official NBA injury-report documents. The bundle does not require credentials, API keys, tokens, cookies, or account-specific secrets.

## Timezone Inputs

The only optional environment inputs recognized by the public bundle are timezone fallbacks:

- `OPENCLAW_USER_TIMEZONE`
- `OPENCLAW_TIMEZONE`
- `USER_TIMEZONE`
- `TZ`

These are configuration inputs. They are not secrets.

## Examples

English:

- `Show today's NBA games in America/Los_Angeles`
- `Show today's NBA stats in Asia/Shanghai`
- `Preview tomorrow's Celtics vs Hornets game in Asia/Shanghai`
- `Show today's Lakers live game flow in Asia/Shanghai`
- `Recap today's Knicks vs Thunder game in Asia/Shanghai`
- `Show tomorrow's Pistons injury report in Asia/Shanghai`
- `Today NBA official reports in Asia/Shanghai`
- `Summarize https://www.nba.com/game/hou-vs-lal-0042500171 official report in Asia/Shanghai`

Chinese:

- `今日NBA赛况，按上海时区`
- `今天比赛谁得分最高，按上海时区`
- `明天凯尔特人vs黄蜂前瞻，按上海时区`
- `今天湖人 live，按上海时区`
- `复盘今天尼克斯vs雷霆，按上海时区`
- `明天活塞伤病报告，按上海时区`
- `明天NBA官方报道，按上海时区`
- `总结 https://www.nba.com/game/hou-vs-lal-0042500171 的官方报道，按上海时区`

## Packaging Notes

- This is a skill-only bundle.
- The public runtime entrypoint is `tools/nba_today_command.py`.
- Maintainer-only verification helpers are intentionally not included in the public bundle.
- Runtime scripts resolve imports from the local `tools/` directory.
- Runtime cache is in-memory only for the current Python process.
- The bundle must not ask for secrets or inspect unrelated host files.
- The bundle must not use generic web browsing to patch missing sports facts.
- NBA.com article summaries must be rewritten summaries, not copied article bodies.
- Ordinary `day / pregame / post` output should not append official-report prompts.
