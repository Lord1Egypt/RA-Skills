---
name: nba-today-pulse
description: Timezone-aware NBA daily intelligence using bundled public ESPN/NBA fetchers plus official NBA injury-report PDFs, with compact day fast path, same-day stats, phase-specific game routes, stronger single-game live detail, independent official-report summaries, refresh-safe follow-ups, and direct tool-output delivery.
user-invocable: true
metadata: {"openclaw":{"skillKey":"nba-today-pulse","requires":{"bins":["python3"]}}}
---

# NBA Today Pulse v15

Version: `1.0.15`

Get a compact mixed-status NBA day view, same-day stat leaders, dedicated pregame/live/post reports, independent injury reports, and explicit `official_report` summaries in one skill. This public `1.0.15` bundle keeps the stable public skill identity while following the validated thin-wrapper contract from the current `NBA_TR` runtime.

Do not invent scores, injuries, lineups, player stats, matchup reasons, article facts, or turning-point narratives that are not supported by the bundled tool output.

## Single Execution Command

Production paths must resolve timezone first and inject `--tz` explicitly.

If the user message already includes a timezone or city:

```bash
python3 {baseDir}/tools/nba_today_command.py --command "<raw request>" --tz "<resolved timezone>"
```

If the user message does not include a timezone but the runtime already knows the user's timezone preference:

```bash
python3 {baseDir}/tools/nba_today_command.py --command "<raw request>" --tz "<resolved timezone>"
```

Only the single branch that asks the user for timezone is allowed to omit `--tz`.

Relative-date requests must stay grounded in the same injected timezone:

```bash
python3 {baseDir}/tools/nba_today_command.py --command "Show today's NBA games" --tz "Asia/Shanghai"
python3 {baseDir}/tools/nba_today_command.py --command "Show tomorrow's NBA games" --tz "America/Los_Angeles"
python3 {baseDir}/tools/nba_today_command.py --command "Who scored the most in today's NBA games?" --tz "Asia/Shanghai"
python3 {baseDir}/tools/nba_today_command.py --command "Summarize today's NBA official reports" --tz "Asia/Shanghai"
python3 {baseDir}/tools/nba_today_command.py --command "今日NBA赛况" --tz "Asia/Shanghai"
python3 {baseDir}/tools/nba_today_command.py --command "明天NBA赛况" --tz "America/Los_Angeles"
python3 {baseDir}/tools/nba_today_command.py --command "今天比赛谁得分最高" --tz "Asia/Shanghai"
python3 {baseDir}/tools/nba_today_command.py --command "今天NBA官方报道" --tz "Asia/Shanghai"
```

## Intent Mapping

- `day`: today's or tomorrow's NBA slate, daily status, all games, mixed-status day view
- `stats_day`: today's NBA stats, who scored the most today, best performance today, rebounds leader, assists leader, most threes, largest margin
- `pregame`: preview, pregame, prediction, matchup preview, all-games preview, multi-matchup preview
- `live`: live game, in-game direction, current momentum, current game flow
- `post`: recap, review, postgame, what happened in the game
- `injury`: injury report, team injuries, matchup injury report
- `official_report`: NBA.com official story, official recap, official preview, game article summary, or any `nba.com/game/...` URL

Injury requests take priority over preview phrasing. Explicit official-report wording or an NBA.com game URL takes priority over generic `day`, `pregame`, or `post` wording.

`official_report` remains a separate explicit route and must not be mixed back into normal `day`, `pregame`, `post`, or `live` rendering.

## Follow-up Refresh Handling

- If the previous turn only asked the user for timezone and the next reply is just a city or IANA timezone, continue the same NBA request silently
- If the user says `refresh`, `update`, `check again`, `score looks wrong`, `更新`, `刷新`, `再看一下`, or `比分不对` while the conversation is already about one NBA matchup, rerun the same request silently and return only the latest tool output
- If the user says `key players only`, `play digest only`, `fourth quarter only`, `injuries only`, `只看关键球员`, `只看回合摘要`, `只看第四节`, or `只看伤病` while the conversation is already about one NBA matchup, keep the same matchup and append the focus phrase to the reconstructed full request
- If the user follows a normal answer by asking for `official report`, `NBA.com story`, `article summary`, or `官方报道`, keep the same date or matchup context when reconstructing the official-report request
- Refresh follow-ups must not add commentary, score explanations, or rewritten summaries

## Fixed Output Shapes

- `stats_day`: Best Performance → Top Scorer → Top Rebounder → Top Assists → Most Threes → Double/Triple Doubles → Largest Margin → Summary
- `pregame`: Game Info → Lineups & Key Players → Injuries → Team Form → Prediction Analysis → Summary
- `live`: Game Info → Lineups & Key Players → Injuries → Live Momentum → Team Comparison → Key Player Stats (up to 5 players per team, compact PTS/REB/AST/STL/BLK + shooting) → Play Digest (up to 8 scored plays plus recent 3-minute run when available) → Summary
- `post`: Game Info → Starting Lineups → Result & Flow Summary → Key Performances → Team Comparison → Injuries → Turning Point → Summary
- `day`: grouped cards ordered by `Live → Final → Upcoming`; live cards show at most 3 compact player lines per team, without team-total rows or duplicate play lines; final cards stay compact
- `injury`: Fact Layer → Analysis Layer
- `official_report`: source/game info → official headline/type/date/byline when available → concise rewritten article summary → themes or single-game cards → source label/link

## Timezone Behavior

- First use any explicit timezone or city in the user message
- Otherwise use a valid timezone input supplied by the runtime and inject it through `--tz`
- If no timezone can be resolved, ask once for a city or IANA timezone and stop there
- If the request already carries relative-date semantics, do not invent a conflicting external `--date`
- Never explain internal runtime provenance or inspect memory files
- If timezone still cannot be resolved after checking the current message and runtime preference, return the short city/IANA prompt once and stop

## Parameter Mapping Examples

- `Show today's NBA games in Shanghai time` -> `--tz Asia/Shanghai`
- `Who scored the most in today's NBA games in Shanghai time?` -> `--tz Asia/Shanghai`
- `Show tomorrow's NBA games in Los Angeles time` -> `--tz America/Los_Angeles`
- `Show today's NBA games in America/Los_Angeles` -> `--tz America/Los_Angeles`
- `Preview tomorrow's Celtics vs Hornets game in Shanghai time` -> `--tz Asia/Shanghai`
- `Show today's Lakers live game flow in Shanghai time` -> `--tz Asia/Shanghai`
- `Recap today's Knicks vs Thunder game in Shanghai time` -> `--tz Asia/Shanghai`
- `Show tomorrow's Pistons injury report in Shanghai time` -> `--tz Asia/Shanghai`
- `Summarize today's NBA official reports in Shanghai time` -> `--tz Asia/Shanghai`
- `Summarize the official report for https://www.nba.com/game/hou-vs-lal-0042500171 in Shanghai time` -> `--tz Asia/Shanghai`
- `今日NBA赛况，按上海时区` -> `--tz Asia/Shanghai`
- `今天比赛谁得分最高，按上海时区` -> `--tz Asia/Shanghai`
- `明天NBA赛况，按洛杉矶时区` -> `--tz America/Los_Angeles`
- `明天凯尔特人vs黄蜂前瞻，按上海时区` -> `--tz Asia/Shanghai`
- `今天湖人 live，按上海时区` -> `--tz Asia/Shanghai`
- `复盘今天尼克斯vs雷霆，按上海时区` -> `--tz Asia/Shanghai`
- `明天活塞伤病报告，按上海时区` -> `--tz Asia/Shanghai`
- `今天NBA官方报道，按上海时区` -> `--tz Asia/Shanghai`
- `总结 https://www.nba.com/game/hou-vs-lal-0042500171 的官方报道，按上海时区` -> `--tz Asia/Shanghai`
- runtime-known timezone, no explicit timezone in the message -> `--tz <resolved timezone>`

## Data Access Behavior

This skill makes outbound HTTP requests through bundled providers to fetch public ESPN and NBA data. For supported injury-report requests it also downloads and parses official NBA injury-report PDFs. For explicit `official_report` requests it reads public NBA.com game pages for official preview/recap story data. This is declared scope, not generic browsing, and it must not be replaced with freeform web search or unrelated host inspection.

No install step is defined. The host runs the bundled Python files in place through the single entrypoint above, without fetching extra installers, package-manager dependencies, or remote archives at install time.

No credentials are required. Do not request API keys, tokens, cookies, passwords, or unrelated account access.

The public bundle is memory-cache only. Its only optional environment inputs are timezone fallbacks: `OPENCLAW_USER_TIMEZONE`, `OPENCLAW_TIMEZONE`, `USER_TIMEZONE`, and `TZ`.

## Output Rules

- Run only the bundled `nba_today_command.py` entrypoint
- Do not switch scripts, reconstruct parameters, or retry alternate command formats
- On success, return the tool output directly
- Do not summarize, simplify, rephrase, add suggestions, or append follow-up offers after the tool output
- Prefer compact cards and concise sections; `day` and `live` should stay readable without raw stat dumps or repeated season-average lines
- For live requests, trust the explicit scoreboard returned by the bundled tool chain; the runtime may refresh it from `nba_live` play-by-play or boxscore before rendering
- For postgame requests, trust the bundled play-by-play-driven recap and turning-point text instead of rewriting it in the skill layer
- For official-report requests, trust the bundled official-report output and do not expand it with freeform article text
- On user-fixable issues such as missing timezone or no matching game, return the final short tool result directly
- Keep `AWAY @ HOME` ordering unchanged
- Match the user's language; Chinese output should prefer Chinese team names and controlled player-name mappings
- Chinese team-name display may vary by locale-aware mapping inside the tool chain, while English display remains canonical and non-regionalized
- Keep relative dates such as `today / tomorrow / 今天 / 明天 / 今日 / 明日` grounded in the resolved requestor timezone
- Do not compute or guess the game score from `FG`, `3PT`, `FT`, player-point subtotals, or team-total snippets

## Forbidden Behaviors

- Do not expose process narration, tool exploration, file inspection, or command retry chatter
- Do not mention internal memory files, host runtime details, or prior-record reasoning
- Do not use web search or generic browsing to patch missing facts unless the user explicitly asks for online verification
- Do not inspect unrelated host files or request secrets, API keys, tokens, or credentials
- Do not add betting advice, odds, spreads, totals, or gambling language
- Do not add future speculation, unverified lineup guesses, or unsupported injury assumptions
- Do not rewrite the tool result into a different structure
