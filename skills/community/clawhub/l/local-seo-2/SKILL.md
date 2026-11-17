---
name: local-seo
description: "Improve a local business's visibility in Google Maps and the local pack: check where it ranks for its main services across the area it serves, compare it with the businesses that outrank it (reviews, categories, website, proximity), review its Google Business Profile signals and questions, find local keywords, and produce a prioritized local action plan. Use when the user asks why their business doesn't show on Google Maps or in the local pack, about near-me rankings, Google Business Profile (GBP) optimization, service-area or multi-location SEO, local keywords, reviews, or NAP and citations."
---

# HarborRank Local SEO

## Goal

Show a local business where it appears in Google Maps for the services that bring in customers, from several points in the area it serves, and why the businesses above it win. End with a short, ordered action plan the owner can work through: profile fixes, reviews, website and location pages, and local keywords.

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

Every Maps check (`get_local_serp_results`, and each point of a `run_local_grid` scan), nearby-business search (`search_local_businesses`), Q&A pull (`get_google_business_questions`) and keyword call in this workflow charges credits; Search Console, the rank tracker and the site crawl do not. A grid of points times keywords adds up fast, so count the calls before running them. Local grid scans need a paid plan.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- Two extras are included in Pro and Agency: local grids larger than 5x5 (a 7x7 `run_local_grid`) and more than 3 tracked competitors per rank tracker (`add_rank_tracker_competitors`). If a tool replies that something needs Pro or Agency, tell the user once what Pro adds, pass on the Pro link from the reply exactly as written, and carry on with what their plan includes (a 5x5 grid, the first 3 competitors). Do not retry it.
- Mention Pro unprompted only when the task needs it: a whole-town map, or watching more than 3 competitors. Say it once per run, in one sentence, with the link from `get_upgrade_link` (`plan: "pro"`).
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Read the business's website: name, address and phone (NAP) on every page, service and city pages, embedded map, LocalBusiness schema, and whether the site matches the profile.
- Compare that NAP with the business's listings that web search turns up (directories, social profiles, industry sites) and list each mismatch with its URL.
- Use Maps screenshots or notes the user takes from their phone at different spots in the service area. Those are the user's own observations; report them with the place and time they were taken.
- Read the sites of the businesses that appear for the main service-and-city queries, and note what they have that this business does not (service pages, city pages, reviews shown, trust signals).
- Gather local keyword ideas from web search: related searches, autocomplete, and People Also Ask for each service plus city or "near me".
- Write the manual Google Business Profile checklist (below) for the owner to work through.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position. Ratings and review counts only as a page visibly shows them, reported as "shown on <source> at <time>"; never fill in a competitor's count you did not see.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to check your Maps position from several points in your service area and pull competitors' ratings, reviews and categories." Do not add more sales copy than that.

## Required inputs

- `projectId` (from `list_projects`)
- The business name as it appears on Google, and its website
- The services that bring in the most customers (two to five)
- Where it serves: a storefront address, or the towns or neighborhoods a service-area business covers
- Optional: the competitors the owner already worries about

If the business has several locations, run one location per pass.

## HarborRank MCP tools

- `get_local_serp_results`: one Google Maps (`searchType: "maps"`, default) or Local Finder SERP for one `keyword` from one point (`near.latitude`, `near.longitude`, optional `near.zoom` 4 to 18). Returns rank, title, domain, URL, main category, rating, reviews, phone, address, claimed status, `placeId`, `cid` and coordinates per listing. `depth` 1 to 100, default 20; `device` desktop or mobile. Charges credits per call.
- `run_local_grid`: checks where the business shows in Google Maps for one `keyword` from a square of points around it (`gridSize` 3, 5 or 7; `spacingMiles` 0.5, 1, 2, 3 or 5) and returns the position at every point, the share of points in the top 3 and the average position. The first call creates the grid from `businessName`, `latitude`, `longitude` and `placeId` (and `domain` when known); later calls pass `gridId` so the points stay the same. Grids and scans are saved in the project, where the user sees them as a heatmap on the Local Grid page. Each point is one Maps search. Paid plans; 7x7 needs Pro or Agency.
- `get_local_grid`: a saved grid and its scans, or the project's grids when no `gridId` is given. Free.
- `search_local_businesses`: business listings near a coordinate within `near.radiusKm`, filtered by `query` (name text) and up to 10 `categories`; `limit` 1 to 50, default 20. Finds nearby competitors in the same category. It does not check rankings. Charges credits.
- `list_business_categories`: the Google Business category slugs (e.g. `dentist`, `roofing_contractor`), filtered by `query`, sorted by how many listings use each.
- `get_google_business_questions`: Google Business Profile questions and answers for one business `keyword` near a coordinate; `depth` 1 to 100, default 20. Charges credits. Run it only when Q&A evidence matters.
- `get_keyword_metrics`, `research_keywords`: volume, keyword difficulty, CPC and intent for local service keywords. Markets are country-level, so the city has to be in the keyword ("plumber austin") to see city demand.
- `get_serp_results`: live organic Google results for 1 to 10 keywords, to see which pages rank under the local pack. Charges credits.
- `get_ranked_keywords` with `resultTypes: ["local_pack", "organic"]`: keywords where the business's domain already shows in the local pack or organic results.
- `get_search_console_performance`: the site's queries with a city or "near me" in them, and clicks to location pages. Free.
- `get_rank_tracker`: organic desktop and mobile positions for tracked keywords, if a tracker exists. It does not track the Maps pack. Free.
- `run_site_audit`, `get_audit_issues`: crawl the website for problems on the service and location pages the profile links to. Free.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

There is no tool that edits a Google Business Profile, fetches review text, or audits citations. Those checks are manual (see step 7).

## Workflow

If the project's SEO folder has `seo-context.md`, read it first for the site, market, audience, competitors and goals; otherwise ask only what this workflow needs.

1. Call `list_projects` and pick the project. Confirm the business name, the services and the service area.
2. Pick the keywords: for each service, the plain term ("dentist", "emergency plumber") and the term with the city. Google localizes the plain term to where the searcher stands, so it is the one that shows true Maps position. If Search Console is connected, call `get_search_console_performance` with `dimensions: ["query"]` and look for local queries already earning impressions. Keep three to five keywords.
3. Find the business and its coordinates: call `get_local_serp_results` for the main keyword from the center of its town (use the address the user gave). Match the business by `domain`, `placeId`, `cid` or title, and note its `latitude`, `longitude`, main category and claimed status. If it is not in the top 20, raise `depth` to 100 before saying it does not show.
4. Plan the grid. A 5x5 grid fits most businesses: 1 mile apart for a storefront in town, 2 or 3 miles for a service-area business. Use 3x3 for a quick check near the shop, and 7x7 (Pro and Agency) for a business that serves a whole city or several towns. State the call count (points times keywords) and ask before running more than 50 points.
5. Run `run_local_grid` for the main keyword with the business's name, coordinates and `placeId` from step 3, then for each other keyword with the `gridId` it returned. Record the top-3 share, the average position and where the business drops out. If the grid is refused because the plan doesn't include it, sample the points by hand instead: the business location plus three or four points across the service area (the towns it serves, or about 3 to 8 km out in different directions), with `get_local_serp_results` for each keyword from each point, recording the rank at each point or "not in top <depth>".
6. Compare with the leaders: take the businesses that hold the top three at most points. For each, record rating, reviews, main category, claimed status, website domain, and distance from the point. Use `search_local_businesses` with the business's category slug (check it with `list_business_categories`) to see how crowded the category is nearby. Call `get_google_business_questions` for the business and the top competitor only if the user asks about Q&A or the profile looks thin; an empty result means no questions were returned, not a fault.
7. Write the manual profile checklist. These need the owner's Google Business Profile access or a look at the live listing: primary and secondary categories, services list, business description, hours and holiday hours, photos, posts, review count over the last 90 days and owner replies, the website link and which page it points to, verification status, and NAP matching the website and main directories. Mark each item "to check" unless the owner confirms it.
8. Check the website: read the page the profile links to and the service and city pages. If the site has more than a handful of pages, call `run_site_audit`, then `get_audit_issues` with `severity: "critical"`, and keep only issues on those pages.
9. Local keywords: call `get_keyword_metrics` for the service-plus-city terms and the services the leaders' categories suggest. Use `research_keywords` only for a new service area. Flag terms with no matching page on the site.
10. Rank the actions. Things the business controls and the leaders do better come first: wrong or missing primary category, profile not claimed, NAP mismatches, website link pointing to the wrong page. Then the review gap, then missing service or city pages, then everything else. Proximity cannot be changed; say where distance alone explains a gap, so the owner does not chase it.

## Output format

Start with:

- **Verdict:** one or two sentences, for example "Shows in the top 3 near the shop for 'dentist', drops out 5 km north where two practices with three times the reviews take the pack."
- **Grid:** for each keyword, the top-3 share and average position, and that the heatmap is saved on the project's Local Grid page (when `run_local_grid` ran).
- **Top 3 actions**, in order.

Then include:

| Keyword | Point | Rank | Top 3 at that point |
| ------- | ----- | ---: | ------------------- |

| Business | Rank (most points) | Rating | Reviews | Main category | Claimed | Website |
| -------- | ------------------ | -----: | ------: | ------------- | ------- | ------- |

Then the profile checklist (checked or "to check"), the local keywords with volume and whether a page targets each, and the full action plan with effort (`quick`, `moderate`, or `project`). Close with what was not checked (points not sampled, profile items only the owner can see).

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `seo-audit` on the business's website, because the page the profile links to and the service and city pages carry local rankings too. If one competitor holds the pack at most points and has a stronger site, recommend `competitor-analysis` on its domain instead.
- **Check back:** end with one dated follow-up: the date (today plus 28 days, written out, for example "Monday, November 9") and the exact question to ask then: "Where does <business> show in Google Maps now from the same points?" (re-run `run_local_grid` with the same `gridId`, so the points match) Say in one line why it needs that wait: profile, category and review changes take weeks to move Maps rankings, and checking the same points with the same keywords keeps the numbers comparable. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the report as `local/<business-slug>-<YYYY-MM-DD>.md`, with the points-by-keyword ranks (including each point's coordinates, so the re-check uses the same ones) as `local/<business-slug>-<YYYY-MM-DD>.csv`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Never invent a number. Every rank, rating and review count comes from a tool result or a page you name.
- A Maps rank is true for one keyword from one point at one time. Never report it as the business's rank for the whole city.
- Do not call a business "not on Maps" until a deeper search (`depth: 100`) and a name search with `search_local_businesses` both miss it.
- Do not recommend keyword stuffing in the business name, fake addresses, or review gating or buying. They break Google's guidelines and can get the profile suspended.
- Recommend changes, never make them. Ask before any write action.
