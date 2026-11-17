---
name: google-business-profile
description: "Audit and optimize one Google Business Profile: primary and secondary categories compared with the local businesses that outrank it, services and products, business description, hours, attributes, photos, posts, review volume, recency, rating and reply practice, Q&A, NAP consistency with the website, and the landing page the profile links to. Produces a prioritized fix list with ready-to-paste text for the description, services, Q&A answers and review reply templates. Use when the user asks to optimize their Google Business Profile, wants a GBP audit, asks which categories to choose, how to get more reviews, or how to improve their Google Maps listing. For Maps rankings across the service area, use local-seo instead."
---

# HarborRank Google Business Profile

## Goal

Review one business's Google Business Profile against the businesses that beat it in Google Maps, and hand the owner a prioritized fix list they can work through in their Business Profile manager. Where text helps, write it: the description, services, Q&A answers and review reply templates.

HarborRank cannot open or edit the private profile dashboard. It sees what Google shows publicly. Every item only the owner can see is marked "check in your Business Profile manager".

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

In this workflow, each Maps check (`get_local_serp_results`), nearby-business search (`search_local_businesses`) and Q&A pull (`get_google_business_questions`) charges credits; Search Console and the site crawl (`run_site_audit`, `get_audit_pages`) do not.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Read the business's website and the page the profile links to: name, address and phone (NAP), hours, services, LocalBusiness schema, and whether they match what the owner says is on the profile.
- Work from screenshots or a copy of the profile the owner pastes from their Business Profile manager. Those are the user's own data; report them with the file as the source.
- Compare NAP with the listings web search turns up (directories, social profiles, industry sites) and list each mismatch with its URL.
- Write the description, services list, Q&A answers and review reply templates from the website and the owner's input.
- Give the full profile checklist (step 6 below) for the owner to work through.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position. Ratings, review counts and competitors' categories only as a page visibly shows them, reported as "shown on <source> at <time>".

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to compare your categories, rating and review count with the businesses that outrank you in Google Maps." Do not add more sales copy than that.

## Required inputs

- `projectId` (from `list_projects`)
- The business name as it appears on Google, its address or town, and its website
- Its two to five main services
- Optional: what the owner can paste or screenshot from their Business Profile manager (categories, services, description, attributes, recent posts)

If the business has several locations, run one location per pass.

## HarborRank MCP tools

- `get_local_serp_results`: one Google Maps (`searchType: "maps"`, default) or Local Finder SERP for one `keyword` from one point (`near.latitude`, `near.longitude`). Returns rank, title, domain, URL, main category, rating, reviews, phone, address, claimed status, `placeId` and `cid` per listing. `depth` 1 to 100, default 20. Charges credits.
- `search_local_businesses`: business listings near a coordinate within `near.radiusKm`, filtered by `query` (name text) and up to 10 `categories`; `limit` 1 to 50. The rows can carry more profile fields than the Maps SERP, such as additional categories, description, hours, attributes and photo count, when Google exposes them. Treat any missing field as `unknown`, not as empty. Charges credits.
- `list_business_categories`: Google Business category slugs (e.g. `dentist`, `roofing_contractor`), filtered by `query`, sorted by how many listings use each.
- `get_google_business_questions`: the profile's public questions and answers for one business `keyword` near a coordinate; `depth` 1 to 100. Charges credits.
- `run_site_audit`, `get_audit_pages`: crawl the website and read the landing page's status, title, description, word count and indexability. Free.
- `get_search_console_performance`: clicks and queries for the landing page, when Search Console is connected. Free.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

No tool reads the private dashboard, review text, Insights or posts, and none edits the profile. Those checks are manual.

## Workflow

If the project's SEO folder has `seo-context.md`, read it first for the site, market, audience, competitors and goals; otherwise ask only what this workflow needs.

1. Call `list_projects` and pick the project. Confirm the business name, location, website and main services.
2. Find the profile: call `get_local_serp_results` for the main service keyword from the business's address. Match it by `domain`, `placeId`, `cid` or title and note its rating, reviews, main category and claimed status. If it is missing from the top 20, retry with `depth: 100`, then `search_local_businesses` with the name as `query`. If the profile is unclaimed, that is the first fix; stop and tell the owner to claim and verify it before anything else.
3. Pick the comparison set: the top three to five businesses in that Maps result. Call `search_local_businesses` with their names or the shared category to pull the business and competitor rows with any extra fields. Check category slugs with `list_business_categories`.
4. Categories: compare the business's primary category with the leaders'. If most leaders use a more specific primary category that fits the business's main service, recommend it. List secondary categories the leaders use that match services the business actually offers. Never suggest a category for a service it does not provide.
5. Reviews: compare rating and review count with the leaders and state the gap. Recency and reply practice are not in the data; ask the owner how many reviews arrived in the last 90 days and whether they reply, or mark "check in your Business Profile manager".
6. Profile checklist. For each item, record what is publicly visible, what the owner confirmed, or "check in your Business Profile manager":
   - Business name matches the real-world name, with no added keywords or cities
   - Primary and secondary categories (from step 4)
   - Services and products: every main service listed, with a short description each
   - Description: up to 750 characters, first 250 carry the main service and area, no links or promotions
   - Regular hours, holiday hours and special hours
   - Attributes that apply (accessibility, payments, service options, owner identity attributes the owner chooses)
   - Photos: exterior, interior, team, work examples, recent uploads by the owner
   - Posts: an update or offer at least every two weeks
   - Q&A (step 7)
   - NAP: exact match with the website footer, contact page and schema
   - Website link and appointment link
7. Q&A: call `get_google_business_questions` for the business. List unanswered questions and wrong answers left by the public. An empty result means no questions were returned, not a fault. Draft answers to the real questions and to the three to five questions customers ask most (from the website FAQ or the owner).
8. Landing page: read the page the profile links to. If the site has more than a handful of pages, call `run_site_audit`, then `get_audit_pages`, and check that page for status 200, indexable, a title and H1 naming the service and town, NAP that matches the profile, and a clear call to action. Linking a single-location profile to the home page is fine; a multi-location business should link each profile to its location page.
9. Write the text: a description, a services list with one line each, Q&A answers, and three review reply templates (positive, mixed, negative). Replies thank the reviewer by name, mention the service, and for negative reviews take the issue offline without arguing or sharing customer details.
10. Rank the fixes: claim and verification, wrong primary category, NAP mismatches and a broken or wrong landing page come first. Then missing services and secondary categories, the review gap and reply practice, then description, photos, posts and Q&A.

## Output format

Start with:

- **Verdict:** one or two sentences, for example "Primary category is 'Contractor' while all four leaders use 'Roofing contractor', and the profile has 31 reviews against their 120 to 400."
- **Top 3 fixes**, in order.

Then include:

| Business | Maps rank | Rating | Reviews | Primary category | Secondary categories | Claimed |
| -------- | --------: | -----: | ------: | ---------------- | -------------------- | ------- |

| Priority | Fix | Evidence | Suggested text or action | Effort |
| -------- | --- | -------- | ------------------------ | ------ |

Effort is `quick`, `moderate`, or `project`. Then the profile checklist, and the ready-to-paste text: description, services, Q&A answers and review reply templates. Close with what was not checked: items only visible in the owner's Business Profile manager, and review text, which no tool reads.

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `local-seo` for this business, to see where it ranks in Google Maps across its service area once the profile is fixed. If the landing page has problems, recommend `seo-audit` on the website instead.
- **Check back:** end with one dated follow-up: the date (today plus 28 days, written out, for example "Monday, November 9") and the exact question to ask then: "Did the profile changes move <business> in Google Maps?" Say in one line why it needs that wait: Google takes weeks to reflect category, service and review changes in Maps rankings, and new reviews need time to arrive. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the report as `local/gbp-<business-slug>-<YYYY-MM-DD>.md`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Never invent a number. Every rank, rating, review count and category comes from a tool result, a page you name, or the owner.
- Never write fake reviews, and never suggest buying reviews, offering discounts or gifts for reviews, asking only happy customers (review gating), or posting reviews from staff. They break Google's policies and can get reviews removed or the profile suspended. Recommend asking every customer, with a direct review link, soon after the job.
- Do not recommend keywords in the business name, a virtual office or fake address, or categories for services the business does not offer.
- Do not claim you checked anything in the private dashboard. Say what the owner must check there.
- Recommend changes, never make them. Ask before any write action.
