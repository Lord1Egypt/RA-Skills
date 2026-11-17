---
name: keyword-cannibalization
description: "Find and fix keyword cannibalization: queries where two or more of the site's own pages get impressions in Google, which of those splits actually cost traffic, and the fix for each (merge and 301, retarget, canonical, internal links, noindex, or de-optimize). Use when the user mentions cannibalization, two pages competing for the same keyword, pages swapping positions in Search Console, asks which page should rank for a query, or wants to consolidate overlapping content. For mapping a keyword list to pages before they exist, use keyword-clustering instead."
---

# HarborRank Keyword Cannibalization

## Goal

Find the queries where Google splits impressions across two or more of the site's URLs, decide which splits cost traffic, and give one fix per split. This workflow diagnoses pages that already compete. Planning which page should target which new keyword belongs to `keyword-clustering`.

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

On hosted HarborRank, research tools spend credits. New accounts start with a 7-day free trial (1,000 research credits, one project); paid plans start at $29/month with 15,000 credits. Search Console, saved keywords, rank tracker reads, and site crawls use no credits. Most of this workflow runs on free Search Console reads and URL inspections; keep research calls that spend credits (`get_keyword_metrics`, `get_ranked_keywords`, `get_serp_results`) to the splits worth acting on. Full backlinks, lead research (`research_lead`), and Lighthouse checks need a paid plan; on Free, the backlinks tools return a preview (totals and the top 3 referring domains, about 50 credits) with an upgrade link.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Find split queries in a Search Console CSV export that has both query and page columns (Performance report, or a Looker Studio or API export). Those figures are the user's own data; report them with the file as the source.
- Apply the decision rule below to those rows and pick a fix for each split worth acting on.
- Read both competing pages to compare intent, depth, titles, headings, canonical tags and internal links.
- Ask the user to paste URL Inspection results from Search Console when the canonical question matters.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to pull every query-page split from Search Console, check Google's chosen canonical, and add search volume to each split." Do not add more sales copy than that.

## Required inputs

- `projectId`, with Search Console connected. If `projectId` is missing, use `list_projects` first. If Search Console is not connected, the tool reply says so and gives a connect link; pass it on and work from a CSV export meanwhile.
- Optional: a topic, folder or query pattern to focus on, and the pages the user suspects are competing.

## HarborRank MCP tools

- `get_search_console_performance`: the core data. Use `dimensions: ["query","page"]`, `rowLimit: 1000`, and page with `startRow` (from `nextStartRow`) while `hasMore` is true. Narrow with `filters` (up to 5, AND-combined; operators `equals`, `notEquals`, `contains`, `notContains`), for example `{dimension:"query", operator:"contains", expression:"<topic>"}` or a `page` filter on one folder. Pass `startDate`/`endDate` to compare windows. Free.
- `inspect_urls`: URL Inspection on up to 10 URLs per call. Compare `googleCanonical` (Google's choice) with `userCanonical` (the page's declared canonical) and check index state and last crawl. Free.
- `get_audit_pages`: per-page title, description, word count, indexability, crawl depth and link counts from the latest site crawl, to compare the competing pages. Free; if there is no audit, `run_site_audit` starts one.
- `get_landing_page_performance`: organic clicks joined with Google Analytics conversions per page, when Analytics is connected, to decide which page is worth keeping.
- `get_keyword_metrics`: volume and intent for the split queries worth acting on. Spends credits; call it once for the shortlist only.
- `get_ranked_keywords`: with a page URL as the target, the keywords a third-party index sees that page rank for. Spends credits; use only when Search Console data is thin.
- `get_serp_results`: check whether the query's results favor one intent (guide, product page, list) when choosing which page to keep.
- `save_keywords`: after the user confirms, save the acted-on queries with a tag such as `page:<slug>` for the winning page, so later checks track them.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

## Workflow

1. If the project's SEO folder has `seo-context.md`, read it first for the site, market, audience, competitors and goals; otherwise ask only what this workflow needs.
2. Pull query-page rows for the last 28 days with `get_search_console_performance` (`dimensions: ["query","page"]`, `rowLimit: 1000`), paging with `startRow` until `hasMore` is false or the rows stop mattering. Use a `query` or `page` filter when the user named a topic.
3. Group rows by query and keep the queries that show two or more URLs. Treat URL variants (trailing slash, `http` vs `https`, `www`, parameters, `#` fragments) as one page and flag them as a canonical or redirect fix, not a content split.
4. Say up front that query rows are a sample. Google hides anonymized low-volume queries and the API returns top rows, so splits on rare queries will be missing and query totals undercount the site. Take site totals from the `date` dimension, never by summing query rows.
5. Apply the decision rule to each split: act when the better of the two pages ranks inside the top 20 (average position 20 or better) and the query is one the business wants, per `seo-context.md` or the user. Otherwise note it and move on. Pages that both sit past position 20, or queries off the business, are not costing traffic yet.
6. For splits worth acting on, confirm the split is real over time: pull the same query with `dimensions: ["date","page"]` and a `query` `equals` filter. Pages that trade places day to day are competing; a page that showed once for a day is noise.
7. Check the canonical picture with `inspect_urls` on both URLs. If `googleCanonical` differs from `userCanonical`, Google is overriding the site's choice and the pages look like duplicates to it; that points to merge or canonical, not retargeting.
8. Compare the pages with `get_audit_pages` (titles, word count, links in, depth) and by reading them. Pick the page to keep: the one closer to the query's intent, with more clicks, conversions (`get_landing_page_performance`) and internal links. Use `get_serp_results` when intent is unclear.
9. Choose one fix per split:
   - **Merge and 301:** both pages serve the same intent and one is weaker. Move its useful content into the keeper, 301 the old URL, and update internal links to point at the keeper.
   - **Differentiate intent and retarget:** both pages deserve to exist but serve different intents (for example a guide and a product page). Rewrite the weaker page's title, H1 and opening around its own query, and link from it to the keeper.
   - **Canonical:** near-duplicates that must both stay live (print versions, filtered or parameter URLs, syndicated copies). Point `rel=canonical` at the keeper.
   - **Internal links and anchors:** both pages are fine but the site links to the wrong one with the query as anchor text. Move exact-match anchors, menu links and hub links to the keeper.
   - **Noindex:** a thin duplicate with no search value that must stay for users (tag pages, thin archives, internal search results). Add `noindex`; do not also canonical it elsewhere.
   - **De-optimize the weaker page:** the weaker page must keep its own job but mentions the query too heavily. Remove the query from its title, H1 and headings and keep one link to the keeper.
10. Hydrate the acted-on queries with `get_keyword_metrics` if volume would change the order of the fixes. Ask before saving them with `save_keywords`.

## Output format

Start with:

- **Verdict:** one or two sentences, for example "Two splits cost traffic; the other 9 are past position 20 and can wait."
- **Fixes:** in priority order, one line each with the keeper page.

Then include:

| Query | Pages (impressions, avg. position) | Better position | Act? | Canonical (Google vs declared) | Keeper | Fix |
| ----- | ---------------------------------- | --------------: | ---- | ------------------------------ | ------ | --- |

List splits you chose not to act on below the table, one line each with the reason. Close with what was not checked (anonymized queries, splits outside the date window, pages not inspected).

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `content-brief` on the keeper page for the highest-priority split, to rewrite it around the merged intent. If the splits come from a whole topic with no clear page map, recommend `keyword-clustering` on that topic's queries instead.
- **Check back:** end with one dated follow-up: the date (today plus 28 days, written out, for example "Monday, November 9") and the exact question to ask then: "Does each query I fixed now go to one page?" Say in one line why it needs that wait: Google has to recrawl the changed pages and follow the redirects, and Search Console needs a few weeks of data after that, at no credit cost to check. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the split table as `keywords/cannibalization-<YYYY-MM-DD>.csv`, with the verdict and fixes at the top of `keywords/cannibalization-<YYYY-MM-DD>.md`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Do not invent metrics. Every impression, position and click comes from a tool reply or the user's file; write `unknown` otherwise.
- Two URLs on one query is not a problem by itself. Recommend a fix only when the decision rule says to act.
- A site with sitelinks or a page and its PDF can show two URLs for a brand query; do not treat brand queries as cannibalization unless the wrong page wins.
- Never recommend a 301 and a canonical or noindex on the same URL at once.
- Recommend changes, never make them. Ask before any write action, including `save_keywords`.
