---
name: market-recon
description: GitHub market recon when the user asks for AI money trends, hot niches, competitor signals, or "找风口/赚钱方向调研", especially when sources are restricted to GitHub only or a previous research run was interrupted. Produces an evidence-linked trend report.
---

# Market Recon (GitHub-only)

Run a trend/opportunity recon where every claim traces to a github.com or api.github.com page fetched during this run. Never fill gaps from memory.

## Steps

1. **Fix constraints and scope.** Default: only `github.com` and `api.github.com` may be fetched; no `web_search`; no writes to user files; report lands in chat. State the constraint set (and any user-added ones) as the first line of the final report.
   Done when: the constraint set is written down for the report.

2. **Choose staffing.** Recon needing ≤8 fetches: run inline. Larger: spawn 3–4 subagents, each task embedding the constraints verbatim plus its own URL list from `references/url-sets.md`. Do not give subagents file access.
   Done when: every dispatched task carries the constraint block and its URL list.

3. **Fetch in capped batches.** Max 5 parallel fetches (unauthenticated Search API allows ~10 req/min). Set `maxChars` 12000–20000 per fetch: Search API JSON runs 65–180KB and truncates otherwise. Prefer `extractMode: "text"` for API JSON, `"markdown"` for HTML pages.
   Done when: trending pages and keyword queries returned HTTP 200, or the rate-limit fallback (step 3a) was used.

   3a. **Rate-limit fallback.** On 403/abuse signals: stop that batch, switch the remaining queries to `https://github.com/search?q=...&type=repositories` HTML pages (still GitHub), and note the throttling in the report.
   Done when: throttling is either absent or disclosed.

4. **Salvage interrupted runs before re-running anything.** If a subagent run was killed or a turn interrupted: pull each child session's `sessions_history` (`includeTools: true`, small limit) and mine `toolResult` blocks for usable fetch payloads. Re-fetch only gaps the salvage cannot cover. Disclose killed runs and their recovered/lost data in the report.
   Done when: every usable payload from the dead run is accounted for and nothing was re-fetched needlessly.

5. **Synthesize the report.** Group findings by opportunity (风口). Per repo: full name as link, stars, velocity (stars/day or /week), created/pushed dates, one-line monetization angle. Flag repos created <6 months ago with high velocity as "new". Close with 3–5 trend conclusions, each naming its evidence, plus the caveat: GitHub heat proves tool/content demand, not revenue.
   Done when: every claim has a link fetched this run and killed/missing data is disclosed.

6. **Verify.** Re-check the report: zero non-GitHub sources, no unfetched claims, rate-limit and truncation events disclosed, `stargazers_count` values quoted only when actually seen (never "about").
   Done when: the checklist passes; fix the report before sending if not.

## Reference

- `references/url-sets.md` — proven URL sets (trending pages, zh/en keyword API queries, vertical queries), URL-encoding for CJK queries, and batch/rate-limit notes.
