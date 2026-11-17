---
name: keyword-clustering
description: "Group keywords into page-level clusters by search intent and map each cluster to an existing or new page, flagging cannibalization. Use when the user has a keyword list, saved keywords, or Search Console queries and asks which page should target which keywords, or wants a keyword map, content plan, topic clusters, or to fix pages competing for the same query."
---

# HarborRank Keyword Clustering

## Goal

Group keywords into page-level clusters and decide which existing or new page should target each cluster. This is a keyword mapping workflow, not just a semantic grouping exercise.

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

- Cluster the keywords the user supplies, or a Search Console query or query+page CSV export, by intent and page type.
- Check whether borderline terms share results by running them through web search; label intent calls you could not check as unverified.
- Map clusters to existing pages by reading the user's site; label the rest as proposed pages.
- Flag cannibalization only when a query+page export shows it. Do not tag keywords.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to add search volume, difficulty, and SERP-overlap checks to these clusters." Do not add more sales copy than that.

## Required inputs

If the project's SEO folder has `seo-context.md` (see `seo-context`), read it first for the site, market, audience, competitors and goals, and ask only for what it doesn't cover.

- `projectId`
- A keyword list, saved keyword tag, seed topic, or target domain
- Optional existing URLs/pages to map against

If keywords are not provided, use `list_saved_keywords` for saved sets, `research_keywords` for seed discovery, or `get_ranked_keywords` when the user starts from a target domain.

## HarborRank MCP tools

- `list_saved_keywords`: fetch an existing keyword set, optionally filtered by tags.
- `research_keywords`: expand a seed when the user starts from a topic.
- `get_ranked_keywords`: gather exact ranking keywords and URLs when the user starts from a domain or page.
- `get_search_console_performance`: when Search Console is connected, pull real queries with `dimensions: ["query","page"]` to map terms to the pages already earning impressions and to surface cannibalization (one query splitting clicks across multiple URLs).
- `get_serp_results`: validate whether keywords belong on the same page by checking SERP overlap and intent.
- `search_local_businesses`: find the businesses and categories around a location before mapping local clusters.
- `get_local_serp_results`: use for local SEO clusters when Maps/local-pack intent should affect page mapping.
- `save_keywords`: optionally tag final clusters after user confirmation.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

## Workflow

1. Gather the candidate keyword set.
   - Use `get_search_console_performance` (dimensions `["query","page"]`) when Search Console is connected to start from real queries and the pages already ranking for them.
   - Use `get_ranked_keywords` for domain/page-driven clustering.
   - Use `search_local_businesses` and `get_local_serp_results` when proximity, local packs, or Google Business results determine whether terms belong on location pages.
2. Remove duplicates, irrelevant terms, and terms that clearly require a different product or audience.
3. Build clusters around intent and page type:
   - Same SERP intent and similar ranking pages belong together.
   - Different intent, buyer stage, or SERP format should be split.
   - Similar words do not guarantee the same cluster.
4. For important borderline terms, use a small `get_serp_results` batch to check overlap.
5. Assign each cluster to:
   - Existing URL, if supplied and appropriate
   - New page recommendation, if no existing page fits
   - Do-not-target / later bucket, if weak or off-strategy
6. Identify cannibalization risk when multiple pages would target the same intent. When Search Console is connected, confirm it from real data with `get_search_console_performance` (`dimensions: ["query","page"]`) — the same query sending impressions to multiple URLs.
7. Ask before applying cluster tags with `save_keywords`.

## Output format

Start with a short mapping summary:

- Number of clusters
- Pages to create
- Existing pages to update
- Cannibalization or consolidation issues

Then include:

| Cluster | Primary keyword | Secondary keywords | Intent | Target page | Priority | Notes |
| ------- | --------------- | ------------------ | ------ | ----------- | -------- | ----- |

For each cluster, include a recommended page brief:

- Page type
- Searcher problem
- Required sections
- Internal-link opportunities
- Save/tag suggestion

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `competitor-analysis` on the domain that holds the top result for the highest-priority cluster's primary keyword, to see what the new or updated page has to beat.
- **Check back:** end with one dated follow-up: the date (today plus 28 days, written out, for example "Monday, November 9") and the exact question to ask then: "Are any of my pages still competing for the same queries?" Say in one line why it needs that wait: Search Console needs a few weeks of data after pages are merged or retargeted. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the cluster table as `keywords/clusters-<YYYY-MM-DD>.csv` and one brief per cluster as `content/briefs/<cluster-slug>.md`. Cluster tags go to the HarborRank project only after the user confirms. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Do not over-cluster tiny keyword sets. If there are fewer than 10 usable terms, produce a simple map.
- Do not rely on lexical similarity alone. SERP intent wins.
- Do not replace tags broadly without explicit confirmation.
- If existing URL data is missing, label target pages as proposed.
