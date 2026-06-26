# NBA Today Pulse Tool Notes

Version: `1.0.15`

This public bundle packages the current `NBA_TR` runtime behind the stable release skill key `nba-today-pulse`.

## Runtime Entry

Production paths should inject `--tz` whenever timezone is known.

```bash
python3 {baseDir}/tools/nba_today_command.py --command "<raw request>" --tz "<resolved timezone>"
```

This is the only public runtime entrypoint. The release bundle does not ship separate maintainer verification commands for the host to invoke.

If timezone is not known, ask once for a city or IANA timezone. Relative-date requests such as `today`, `tomorrow`, `今天`, and `明天` must stay grounded in the resolved requestor timezone.

## Release Contract

- the skill should act as a thin wrapper only: pass raw request + resolved timezone to `nba_today_command.py`
- normal `day / stats_day / pregame / live / post / injury` routes should stay aligned with the faster `v12`-style product shape
- explicit single-game `live` should stay on the bundled fast path unless the user explicitly asks for deeper enrichment
- `official_report` is the only route allowed to summarize NBA.com story bodies
- normal `day / pregame / post` output must not append official-report prompts or story background
- English requests should receive English-shaped output with canonical NBA names; Chinese requests should preserve Chinese section labels and controlled Chinese name mappings where available
- do not add freeform browsing, command retry narration, or result rewriting at the skill layer

## Credentials

No credentials are required. The bundle only uses public sports data and does not require API keys, tokens, cookies, passwords, or account-specific secrets.

The only optional environment inputs recognized by this public bundle are timezone fallbacks:

- `OPENCLAW_USER_TIMEZONE`
- `OPENCLAW_TIMEZONE`
- `USER_TIMEZONE`
- `TZ`

These values are configuration inputs, not credentials. User-provided timezone or city text takes priority.

## Cache Behavior

The public bundle uses in-memory caching only during the current Python process. It does not expose public runtime cache environment variables and does not require persistent storage.

## Data Sources

- ESPN public JSON scoreboards, summaries, rosters, schedules, injuries, and team statistics
- NBA.com public stats and live JSON endpoints
- NBA.com public game pages for official preview/recap stories
- Official NBA injury-report listing and report PDFs

Outbound HTTP requests and remote PDF reads are limited to those supported NBA reporting features. They are not generic browsing.

## Example Commands

English:

```bash
python3 {baseDir}/tools/nba_today_command.py --command "Show today's NBA games" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "Show today's NBA stats" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "Preview tomorrow's Celtics vs Hornets game" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "Show today's Lakers live game flow" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "Recap today's Knicks vs Thunder game" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "Show tomorrow's Pistons injury report" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "Today NBA official reports" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "Summarize https://www.nba.com/game/hou-vs-lal-0042500171 official report" --tz Asia/Shanghai
```

Chinese:

```bash
python3 {baseDir}/tools/nba_today_command.py --command "今日NBA赛况" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "今天比赛谁得分最高" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "明天凯尔特人vs黄蜂前瞻" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "今天湖人 live" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "复盘今天尼克斯vs雷霆" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "明天活塞伤病报告" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "今天NBA官方报道" --tz Asia/Shanghai
python3 {baseDir}/tools/nba_today_command.py --command "总结 https://www.nba.com/game/hou-vs-lal-0042500171 的官方报道" --tz Asia/Shanghai
```

## Maintainer Checks

- Run `python3 -m py_compile tools/*.py` from the bundle directory before packaging.
- Run the bundle regression test before packaging.
- Scan the directory and zip for private paths, non-public identity text, test-only runtime overrides, and credential language.
