---
name: link-prospecting
description: "Find link-building prospects for a page or asset: resource pages, listicles, publishers, and local sites from live SERPs and competitor backlinks, with contact paths and personalized outreach drafts. Use when the user wants backlinks, link building, guest post or PR targets, outreach emails for links, or the sites that link to a competitor."
---

# HarborRank Link Prospecting

## Goal

Find realistic pages, sites, and authors that might reference the user's page, product, study, guide, or tool. Use HarborRank for prospect discovery, then use available web/search/browser tools for contact discovery.

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

- Run the prospecting query patterns through web search instead of `get_serp_results`, then filter prospects as usual.
- Read prospect pages to qualify relevance and choose the outreach angle.
- Discover contact paths and draft outreach as usual; those steps already use web and browser tools.
- Skip competitor backlink analysis.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to add competitor backlink patterns and the strength of each prospect's domain." Do not add more sales copy than that.

## Required inputs

If the project's SEO folder has `seo-context.md` (see `seo-context`), read it first for the site, market, audience, competitors and goals, and ask only for what it doesn't cover.

- `projectId`
- User domain or target URL
- Linkable asset, page, product, study, tool, or topic
- Optional competitors
- Optional market/location/language

## HarborRank MCP tools

- `get_serp_results`: find ranking articles, listicles, resource pages, comparisons, and topical publishers.
- `get_backlinks_overview`: inspect competitor domain or page backlink/referring-domain patterns.
- `get_domain_overview`: qualify important prospect domains.
- `get_ranked_keywords`: understand what a prospect or competitor ranks for when topical fit matters.
- `search_local_businesses` and `get_local_serp_results`: use for local SEO link prospecting when nearby businesses, local competitors, or Maps/category signals can reveal partnership targets.
- `research_keywords`: expand prospecting queries.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

## Contact discovery tools

After HarborRank identifies good prospects, use available non-HarborRank browsing or search tools for public contact discovery. Depending on the client, this may be web search, page fetches, browser automation, or a search API.

Look for:

- Author byline pages
- Contact pages
- Editorial guidelines
- About/team pages
- LinkedIn, X, Bluesky, or other professional profiles
- Newsletter or publication masthead pages
- Public email addresses in page HTML or visible page text
- Structured data such as `Person`, `Organization`, `sameAs`, or `email`

Only record contact details that were actually found. Include the source URL for any email, profile, or contact form.

## Prospecting query patterns

Build queries from the asset/topic:

- `<topic> resources`
- `best <category> tools`
- `<competitor> alternatives`
- `<topic> statistics`
- `<topic> guide`
- `<topic> examples`
- `<topic> templates`
- `<topic> software`
- `<topic> for <audience>`

Use `get_serp_results` in batches for the most relevant patterns. Send at most 10 queries per call.

## Workflow

1. Clarify the linkable asset and the reason someone would reference it.
2. Build 5-10 prospecting queries by default.
3. Call `get_serp_results` for those queries.
4. If competitors are provided, call `get_backlinks_overview` for the strongest competitor domains or pages first. On Free this returns a preview (totals and the top 3 referring domains); use it, note that the full profile needs a paid plan, and continue.
5. For local SEO, use `search_local_businesses` and `get_local_serp_results` around priority locations to identify nearby competitors, categories, and local SERP evidence before searching for local chambers, associations, campus resources, community pages, and directories.
6. Filter prospects:
   - Keep topical relevance and editorial pages.
   - Prioritize articles, directories, resource pages, comparisons, statistics pages, templates, and curated lists.
   - Deprioritize homepages, login pages, thin affiliate pages, spam, unrelated forums, and direct competitors unless a comparison angle is valid.
7. For each good prospect, define the outreach angle:
   - Broken/missing resource
   - Better current data
   - Useful tool/template
   - Alternative or comparison inclusion
   - Expert quote or supporting reference
8. For the strongest prospects, visit or search the prospect site to find the best contact path.
9. Draft outreach messages. If contact details were found, include the source. If not, list the next best contact-discovery path.

## Output format

Start with:

- Best outreach angle
- Highest-priority prospect type
- Any data limitations

Then include:

| Prospect URL | Site/domain | Source | Relevance | Suggested angle | Contact path | Priority |
| ------------ | ----------- | ------ | --------- | --------------- | ------------ | -------- |

Then provide 2-3 reusable outreach drafts:

- Resource/list inclusion
- Article update/reference suggestion
- Competitor alternative/comparison angle

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `keyword-research` to pick the next page worth building and promoting, since links work best when pointed at a page that targets a winnable query.
- **Check back:** end with one dated follow-up: the date (today plus 14 days, written out, for example "Monday, November 9") and the exact question to ask then: "Which <asset> prospects replied or linked?" Say in one line why it needs that wait: outreach replies come within days, and new links take a week or more to appear in backlink data. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the prospect table as `outreach/prospects-<asset-slug>-<YYYY-MM-DD>.csv` and the drafts as `outreach/drafts-<asset-slug>-<YYYY-MM-DD>.md`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Do not invent email addresses, social handles, or contact names.
- Do not say HarborRank found contact details unless an HarborRank tool returned them. Attribute contact discovery to the web/search/browser source used.
- If contact details are not available after a reasonable search, recommend specific discovery steps such as checking the author page, contact page, LinkedIn, X, or a reputable contact-enrichment tool.
- Avoid spammy mass outreach. Personalize by page and reason.
- Flag prospects that are direct competitors or likely paid placements.
