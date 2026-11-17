---
name: keyword-research
description: "Find and prioritize keywords to target: discover ideas from seed topics or Search Console, check search volume, keyword difficulty, CPC, intent and live SERPs, and save the best terms to the HarborRank project. Use when the user asks what keywords to target or wants keyword ideas, content topics, search volume, low-competition or striking-distance keywords, or local service keywords."
---

# HarborRank Keyword Research

## Goal

Turn seed topics into a prioritized keyword opportunity set using HarborRank MCP data. The output should help the user decide what to target, what to save, and what to research next.

## Step 0: Check connection

Before any other step, confirm the HarborRank MCP tools are loaded. Look for `get_domain_overview` or `list_leads` among your tools, including deferred tools you can load (the name may carry a prefix such as `mcp__harborrank__`). If they are there, call `whoami`: it uses no credits, confirms the user is signed in, and returns `creditsRemaining` for budgeting the run. Do not call a research tool to test the connection.

If neither tool is available, or `whoami` fails because the user is not signed in, tell the user plainly: "HarborRank isn't connected, so I can't pull live HarborRank data yet." Then tell them how to connect it:

- Claude Code with the HarborRank plugin: run `/mcp`, choose `harborrank`, and sign in.
- Claude Code without the plugin: run `claude mcp add --transport http --scope user harborrank https://app.harborrank.com/mcp`, then `/mcp` to sign in.
- Claude on the web, desktop or Cowork: open Customize, then Connectors, search for HarborRank, choose Connect, and sign in. New accounts start with a 7-day free trial.
- Cursor with the HarborRank plugin: open Cursor Settings, then MCP, and sign in to `harborrank`.
- Gemini CLI with the HarborRank extension: run `/mcp auth harborrank`.
- Other clients: add `https://app.harborrank.com/mcp` as a remote MCP server. Setup for each client is at https://harborrank.com/docs/mcp.

Tell them what happens when they connect: they sign in to HarborRank with Google or email and start a 7-day free trial. Then they come back to this conversation and say "connected", and you pick up the task where it stopped.

Do not stop there. Continue in fallback mode (below). If the user connects HarborRank mid-task, run Step 0 again and switch to the full workflow.

### Plan limits

On hosted HarborRank, research tools spend credits. New accounts start with a 7-day free trial (1,000 research credits, one project); paid plans start at $29/month with 15,000 credits. Search Console, saved keywords, rank tracker reads, and site crawls use no credits. A keyword search costs about 50 credits and a domain overview about 80. Full backlinks, lead research (`research_lead`), and Lighthouse checks need a paid plan; on Free, the backlinks tools return a preview (totals and the top 3 referring domains, about 50 credits) with an upgrade link.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Gather keyword ideas from seed topics and from web search: related searches, autocomplete suggestions, and People Also Ask questions.
- Work striking-distance queries (average position 5-20) from Search Console CSV exports in the workspace. Those figures are the user's own data; report them with the file as the source.
- Read the top results for the leading candidates to judge intent and what a winning page needs.
- Prioritize on business fit and intent, and deliver the shortlist as a table or file the user can save later. Do not save keywords.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to add search volume, keyword difficulty, and CPC to this shortlist." Do not add more sales copy than that.

## Required inputs

If the project's SEO folder has `seo-context.md` (see `seo-context`), read it first for the site, market, audience, competitors and goals, and ask only for what it doesn't cover.

- `projectId`
- One or more seed topics, products, pages, competitors, or audience problems
- Optional market/location/language

If `projectId` is missing, use `list_projects` first. If the target market/location/language is unclear and would materially affect keyword metrics, ask the user; otherwise use the MCP tool defaults.

## HarborRank MCP tools

- `research_keywords`: primary discovery tool. Use 1-5 seeds per call and prefer 150 results unless the user asks for exhaustive research.
- `get_keyword_metrics`: hydrate up to 700 known keywords with volume, keyword difficulty (KD), search intent, CPC, and monthly trends in one call. Use it to score candidate or known terms — including the Search Console striking-distance queries from step 1.
- `get_ranked_keywords`: pull exact ranking keyword rows when a target domain or page is part of the research brief.
- `get_search_console_performance`: when Search Console is connected, start from the project's real first-party demand — queries already earning impressions and near-ranking ("striking distance") terms. Request a high `rowLimit` and filter average position 5-20 client-side, since the API sorts by clicks and can't filter by position. Then hydrate those striking-distance queries with `get_keyword_metrics` to attach difficulty and intent.
- `get_serp_results`: inspect SERPs for the top candidate terms, especially when intent is ambiguous.
- `search_local_businesses`, `get_local_serp_results`, and `get_google_business_questions`: use for local SEO topics when a business/location radius matters.
- `list_saved_keywords`: avoid duplicating already-saved work or use existing tags as context.
- `save_keywords`: save selected keywords only after explicit user confirmation.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

## Workflow

1. Normalize seeds into a small set of distinct research angles. If Search Console is connected for the project, first pull `get_search_console_performance` (high `rowLimit`, default lookback), filter to striking-distance positions (~5–20) client-side, and hydrate those queries with `get_keyword_metrics` to attach KD and intent. That ranked, hydrated list is your fastest opportunity set — work it before broad discovery.
2. If the request is local SEO, identify the business, location/coordinates or service area, and local categories. Use `search_local_businesses` and `get_local_serp_results` for the most important location/keyword set instead of relying only on national keyword/SERP data.
3. Call `research_keywords` for exploratory seeds. Use bulk calls when possible.
4. Use `get_keyword_metrics` to hydrate a fixed keyword list — or the striking-distance queries from step 1 — with volume, KD, and intent before prioritizing.
5. Use `get_ranked_keywords` when the user provides a domain/page and wants opportunities based on current rankings, near-misses, or competitor-owned terms.
6. Remove irrelevant, duplicate, branded-only, and off-intent terms.
7. Prioritize by practical opportunity, not volume alone:
   - Strong match to the user's product/page/topic
   - Clear search intent
   - Reasonable difficulty
   - Useful volume/CPC signal
   - SERP where the user can plausibly compete
   - For local SEO, local-pack/Maps visibility and proximity fit
8. Use `get_serp_results` for high-potential or ambiguous keywords when SERP intent would change the recommendation; keep the default check small.
9. Present a shortlist and a longer opportunity table.
10. Ask before saving keywords. When saving, suggest concise tags such as `topic:<topic>`, `intent:<intent>`, or `page:<slug>`.

## Output format

Start with the highest-signal recommendation:

- Best opportunity theme
- Top keywords to target now
- Keywords to save
- Risks or SERP caveats

Then include a compact table:

| Keyword | Intent | Volume |  KD | CPC | Priority | Notes |
| ------- | ------ | -----: | --: | --: | -------- | ----- |

End with whether to save the chosen keywords.

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `keyword-clustering` on the shortlist, to decide which page targets each keyword. If one domain holds the top results for most of the shortlist, recommend `competitor-analysis` on that domain instead.
- **Check back:** end with one dated follow-up: the date (today plus 28 days, written out, for example "Monday, November 9") and the exact question to ask then: "Where do my saved <topic> keywords rank now?" Say in one line why it needs that wait: new or updated pages take weeks to rank, and Search Console positions cost no credits to check. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the opportunity table as `keywords/<topic>-<YYYY-MM-DD>.csv`, with the summary at the top of `keywords/<topic>-<YYYY-MM-DD>.md`. Keywords the user approves are also saved to the HarborRank project with `save_keywords`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Do not invent metrics. If HarborRank does not return a value, write `unknown`.
- Do not call `save_keywords` without explicit confirmation.
- Prefer business-fit and intent-fit over chasing the largest volume term.
