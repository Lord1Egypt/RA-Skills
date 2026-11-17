---
name: maxpreps
description: "Read MaxPreps.com high school sports data — find a school, then get team schedules, scores, records, rosters, stat leaders, rankings, and athlete careers for any US high school."
---

# MaxPreps

National high-school sports database (CBS Sports). **No auth, no API key, no browser bridge** — plain `curl` from anywhere, no signed-in tab.

Pages are Next.js SSR: every public page has a companion JSON route at
`/_next/data/<buildId>/<path>.json`. `scripts/mpx.mjs` resolves the `buildId`, fetches, and decodes.

```bash
# scripts/mpx.mjs sits next to this SKILL.md — point M at it.
# Standalone install: M=~/.claude/skills/maxpreps/scripts/mpx.mjs
# Shipped with maxpreps-mcp: M=<plugin-root>/skills/maxpreps/scripts/mpx.mjs
M=~/.claude/skills/maxpreps/scripts/mpx.mjs

node "$M" search "myers park"
node "$M" schedule nc/charlotte/myers-park-mustangs/football/25-26/schedule
```

`mpx.mjs <kind> [path]` — `path` is the site path without leading/trailing slashes.
With no path it decodes a payload on stdin. Kinds:

- `search "<query>"` — schools + athletes (**start here**)
- `teams <school-or-team-path>` — every team path the school publishes
- `schedule` — games with scores, result, home/away (decodes the positional array)
- `roster` — players with jersey, position, height, class (decodes the positional array)
- `stats` — team stat leaders · `team` — season info, record, standings, rankings
- `rankings` — ranked leaderboard for a sport (see path note below)
- `teamrankings` / `standings` — one team's ranks; its conference table
- `statcats` / `statleaders` — stat leaderboard index; one board's ranked athletes
- `school` — school profile + nearby schools · `athlete` — one athlete's career
- `raw` — undecoded `pageProps`, for anything without a dedicated kind
- `buildid` — print the cached build id

Flags: `--all` keep `isDeleted` rows · `--raw` emit undecoded `pageProps` · `--fresh` (buildid) bypass cache.

## Resolve before you fetch

Don't guess paths — two lookups, both cheap:

```bash
# 1. school -> canonicalUrl
node "$M" search "mater dei" | jq -r '.schools[] | "\(.name) (\(.city), \(.state))  \(.canonicalUrl)"'

# 2. school path -> real team paths
node "$M" teams ca/santa-ana/mater-dei-monarchs | jq -r '.[] | "\(.path)  [\(.gender) \(.sport) \(.level)]"'
```

Team path grammar is `<sport>[/girls][/jv|/freshman][/<yy-yy>]/<tab>`, but the segments are
**not predictable** — the default gender varies by sport (`golf/girls` + `golf/spring`,
`field-hockey` is Girls with no gender segment). Always take paths from `teams`.

Tabs: `schedule`, `roster`, `stats`, `rankings`, `standings`. Omit the tab for the team home page.

Leaderboards live on their own path: `[<st>/]<sport>[/<season>]/rankings/<page>` — the trailing
page number is **required** (omitting it 404s) and each page holds 25 teams.

## Seasons

Current season = no year segment. Prior seasons insert `<yy-yy>` **before** the tab:
`.../football/25-26/schedule`. Roughly 20 years of history; `mpx teams <team-path>` lists
every season with its `year`, or read `.seasons` from `mpx team <team-path>`.

## Gotchas

- **`buildId` rotates on every deploy.** `mpx` caches it for 6h and silently re-resolves on a 404, so this is handled — but a hand-rolled `curl` against a stale id 404s. Use the script, or `node "$M" buildid` first.
- **An out-of-season team looks broken.** Before opening day the current season has an empty roster and no results. That is correct data, not a failure — check the prior season (`25-26`) before reporting nothing.
- **`isDeleted` rows are real and numerous.** The 25-26 Myers Park football roster carries 87 entries, 63 of which the site renders; the rest are soft-deleted duplicates. `mpx` filters them by default (matching the site) — `--all` keeps them. Same for contests.
- **`resultString` is winner-first, not team-first.** A loss reads `"L 20-13"` even though the team scored 13. For team-vs-opponent use the decoded `teamScore` / `opponentScore` fields, which `mpx` orients correctly.
- **`homeAwayType`: `0` = home, `1` = away, `2` = neutral site** (decoded to `homeAway`; any other value → `unknown`).
- **`classYear` is a number**: 9–12, decoded to `classYearLabel` (`Fr.`/`So.`/`Jr.`/`Sr.`).
- **Statewide scoreboards are not in the JSON.** `/<st>/<sport>/scores/` returns only page chrome — the game list is hydrated by a route that never fires server-side. Get scores per-team from `schedule` instead; don't claim a state had no games.
- Search is strict — `"myers park high"` returns zero, `"myers park"` returns the school. Drop qualifiers and retry before concluding a school is absent.

## In context groups

maxpreps-mcp joins the **school** group with `lookup` hints only (aliases like "game",
"score", "roster", "ranked"). It declares **no canonical read and no subject**: every read
needs a school or team path the person names, and MaxPreps has no account to list "my" teams
from, so it cannot answer "what's on at school this week?" alone. A compound ask such as
"what's due at school — and when is the varsity football game?" is answered by the group's
canonical reads for the first half and by `maxpreps_search` → `maxpreps_list_teams` →
`maxpreps_get_schedule` (`played: upcoming`) for the named team. No browser bridge is
involved, so it never answers "needs your browser open".

Read-only and low-volume by design; there is no write path. See `references/recipes.md` for
field shapes, the positional key maps, and ready-to-run jq.

For the same data as typed MCP tools — usable from claude.ai or any client without this CLI —
see [maxpreps-mcp](https://github.com/chrischall/maxpreps-mcp), which ships this skill.
