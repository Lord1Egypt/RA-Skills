---
name: new-hire-detection
description: 'Get a Slack alert when a decision-maker joins a company in your ICP: a Sales Navigator job-change search watches your market for people who just took a role you sell to, an agent qualifies each one''s new company against your ICP, and fits are posted with verdict and links. Triggers: "watch our market for new hires", "put new VPs of Sales in our market into HubSpot", "post in Slack when a new VP Sales joins a company in our ICP", "a decision-maker just joined a company in our market", "a new head of sales starts at an account", "new KDM detection", "route new hires into the CRM", "tell the deal owner when a new decision-maker lands mid-deal", "run our new-hire play on a schedule". Cargo project, Sales Navigator, Slack, HubSpot, Salesforce, Attio. Skip when: your own CRM contacts may have moved jobs, which is track-job-changes; or you want a list of people once, which is find-b2b-leads.'
version: "0.1.3"
compatibility: "Requires the cargo-project skill, a Cargo project (cargo.json at its root), @cargo-ai/cdk 1.0.88 or later, and authenticated Sales Navigator, LinkedIn, LLM, and Slack connectors. A CRM connector (HubSpot in the example; Salesforce and Attio by adaptation) is needed only for the CRM variations. No LinkedIn seat, user, or cookie is needed. The repository example does not deploy, extract, or post anything until an agent adapts it in the consumer project."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/new-hire-detection
metadata:
  author: getcargo
  source: cookbook
  personas:
    - revops
    - sales-development
    - gtm-engineering
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/gtm-skills
---

# New-hire detection

**State: to-be-approved.** Deploy-verified against a live workspace: not yet. Treat `Done when`
below as the acceptance test and review `cargo-ai project plan` before deploying. Make no outcome claim
for this skill until it is approved.

## The outcome

Every person who just took a role you sell to, anywhere in your market, at a company that fits your
ICP, shows up in a Slack channel the team reads: who they are, where they landed, why the company
fits, and the links. Not a list pulled once: a pipeline that keeps watching.

A person entering a new role is the cleanest buying signal in B2B: fresh budget, a mandate to
change things, and no loyalty yet to the vendor already in place. Most of the market is not worth a
rep's time, so every company is qualified against the ICP in the workspace context first, and only
the ones that fit are posted. A channel that hears about everyone stops being read.

The market is the scope, not your book. The source is a Sales Navigator people search over the
industry, headcount band, location and titles you choose, filtered to people who changed jobs in
the last year and took this position in the last year. Watching people you already hold is
`track-job-changes`.

The play ends at the Slack post. It writes to no CRM and sends nothing to the person. A team with a
CRM can add a read-only "already in the CRM" line to the post, or make the CRM the destination with
routed tasks; both are variations in
[`references/crm-adaptation.md`](references/crm-adaptation.md).

**Two failure modes worth knowing before you start.** A search URL encoded once instead of twice
loads an empty search, and the sync reports success with nothing in it. And a missing ICP leaves
the qualifier judging against nothing, so it passes everything or nothing.

## Example

> Every time a new VP Sales or head of RevOps starts at a US software company with 51 to 500 people, post it in #new-hires.

Illustrative output, fictional records:

| Person (role)                   | Company (domain)              | Status    | What landed in Slack                                                         |
| ------------------------------- | ----------------------------- | --------- | ---------------------------------------------------------------------------- |
| Priya Raman (VP Sales)          | Northwind (northwind.example) | posted    | "New VP Sales at Northwind (Tier 1, 88/100)", the rationale, both links      |
| Mei Lin (Chief Revenue Officer) | Contoso (contoso.example)     | posted    | "New Chief Revenue Officer at Contoso (Tier 1, 84/100)", the rationale       |
| Tomás Ortega (Head of RevOps)   | Fabrikam (fabrikam.example)   | posted    | "New Head of RevOps at Fabrikam (Tier 2, 71/100)", the rationale             |
| Sam Hale (VP Sales)             | Tailspin (tailspin.example)   | not_icp   | Nothing: a consumer app, a disqualifier in the ICP                           |
| Ana Costa (Director of RevOps)  | Litware                       | no_domain | Nothing: the company page has no website, so there was nothing to qualify on |

Five new hires in one sync: three posted, one declined by the qualifier, one stopped at the domain
guard before any qualifier call.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job
is to end up with the code your company would have written, in your project, and an agent does the
adapting.

**Install the required authoring skill first.** If `cargo-project` is absent, run:

```sh
npx skills add getcargohq/cargo-skills --skill cargo-project
```

Then read `.agents/skills/cargo-project/SKILL.md` directly; no session reload is needed. Complete its
bootstrap and use its authoring, state, plan, and deployment rules throughout. Stop before any
search or template work if the skill cannot be installed or read.

1. **Install it: the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/new-hire-detection` writes this example to
   `infra/new-hire-detection/` and this procedure to `.claude/skills/new-hire-detection/`. No
   project yet? `cargo-ai project init <dir> --cookbook new-hire-detection && cd <dir> && npm install`
   does both; this folder never ships a shell. **If you are reading this from the project's
   `.claude/skills/`, the install already happened. Start at step 2.** On a CLI too old to have
   `add`, copy this folder in as a sibling of what is there by hand; everything below is unchanged.
2. **Reconcile it with what is already declared.** For every resource this example carries that the
   project already has (a Sales Navigator, LinkedIn, LLM, or Slack connector, a new-hire folder),
   rewire the imports to the existing one and drop the copy. Two resources with one slug is a
   collision at deploy. This skill declares no `defineContext`: that resource is a per-workspace
   singleton owned by the project. Copy this skill's `context/icp.md` into the project's `context/` only
   when no ICP is written there yet. This folder needs nothing in `.env`; append nothing and never
   overwrite it.
3. **Pick the channel, and offer the CRM.** Resolve the Slack channel id through the connector's
   autocomplete and set `slackChannelId`. Then inspect the authenticated connectors: if a CRM is
   connected, offer `crm_lookup` and `crm_routing` from
   [`references/crm-adaptation.md`](references/crm-adaptation.md), say what each costs, and build
   neither without a yes.
4. **Shape and count the search.** Follow [`references/search.md`](references/search.md): derive
   the titles, industries, headcount and locations from the ICP (ask only when there is none),
   resolve every facet id through the autocompletes, and count each URL with
   `searchPersonMetrics`. Above 2,500, split by a facet. Stop for approval of the search, the
   limit, the cadence and the estimated cost per sync. Nothing is extracted while it is pending.
5. **Adapt and deploy for the pilot.** Work the sections below in order: _What should not change_
   is what you argue back about (say what breaks, then do it if they still want it); _What you can
   change_ is what you offer unprompted; _What you will be asked_ is the floor, and you derive
   before you ask. Record what you changed and why under a `## Decisions` section in your copy of
   this file. The model ships as the pilot (`limit: 10`, no schedule); keep it that way for the
   first deploy. Then run `node --import tsx evals/contract.mjs` from this skill's folder, followed
   by `cargo-ai project types && cargo-ai project check && cargo-ai project plan` from the project root. Show
   the diff and deploy with the play disabled. Never run `cargo-ai project init --force` in a non-empty
   directory.
6. **Run ten, then open it up.** Follow [`references/run.md`](references/run.md): sync ten, enable
   and execute the play once, and report every run with its status and the Slack post. Only on an
   explicit yes after that, set the approved `limit`, add the cadence, and redeploy. Walk _Done
   when_ line by line and report each with evidence. Deployed cleanly and produced nothing is the
   normal failure.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked. Only the ones marked
_asked_ genuinely live in the operator's head.

| Input           | Kind    | How it is answered                                                                                                                                                                                                            | Why it matters                                                                                                                                              |
| --------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `market`        | derived | Titles, industries, headcount band and locations, read from the ICP in the workspace context. Ask for exactly these four only when no ICP exists and no company domain can be researched, then write them to `context/icp.md` | It is the audience. The qualifier reads the same ICP, so a market that lives only in a URL leaves the agent judging against nothing                         |
| `search_size`   | derived | `searchPersonMetrics` on each candidate URL, as in references/search.md                                                                                                                                                       | Above 2,500 a single URL silently stops at 2,500 and the rest of the market is never seen                                                                   |
| `slack_channel` | asked   | Which channel the team reads for this. Resolve its id through the Slack connector's autocomplete; never type a name                                                                                                           | A channel nobody owns is a channel nobody reads, and a wrong id posts somewhere else or nowhere                                                             |
| `cadence`       | asked   | Whether it should run on its own, and how often. Default: every two weeks (the 1st and the 15th). The alternative is on demand                                                                                                | Every sync re-extracts and re-bills the whole search, so cadence is the main cost dial, traded against how fresh a new hire is when the team hears about it |
| `crm`           | derived | Inspect the authenticated connectors. None: nothing to ask. One or more: offer the CRM variations once, with their cost                                                                                                       | The template needs no CRM; a team that has one usually wants at least to know whether the company is already in it                                          |

Checked before moving on, not after the deploy:

- `market`: every facet value is an id from an autocomplete, titles are quoted, and the three
  job-change filters are still in every URL
- `search_size`: counted for the URLs actually being deployed, each under 2,500
- `slack_channel`: the id resolves to the channel the operator named, and the Slack connector can
  post to it

## What you can change

The code is a worked example. These reshapes are expected, and the agent offers them rather than
waiting to be asked. Every one costs something; that is what makes it a variation and not the default.

| Variation             | When it is right                                                                                 | How                                                                                                                                  | What it costs                                                                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `crm_lookup`          | A CRM is connected and the team wants to know, on the post, whether the company is already in it | Add the CRM connector, the lookup script, and one account lookup before the post (`references/crm-adaptation.md`)                    | A CRM lookup per qualified person, and one more connector to keep authorized. Nothing is written                                                        |
| `crm_routing`         | The CRM is where the team works, and a task on the right owner beats a Slack message             | Replace the post with the routed CRM writes in `references/crm-adaptation.md`: create, alert the deal owner, welcome at a customer   | Owner IDs, a CSM field, association types and a LinkedIn field to resolve; an email lookup per person; writes that a mistake leaves in the CRM          |
| `cadence`             | The market is small and a weekly signal matters, or the budget is tight and monthly is enough    | Change the cron added when opening up (`infra/models/new-hires.ts`), or add none and sync on demand                                  | Weekly roughly doubles the extraction spend of the default for the same people found; monthly halves it and the team hears about a new hire weeks later |
| `split_search`        | The counted search is above 2,500                                                                | One URL per region or headcount band in `urls` (`infra/models/new-hires.ts`), each counted                                           | More URLs to keep in sync with the ICP; overlapping splits extract the same person twice and bill both                                                  |
| `channel_per_segment` | Different teams own different segments (regions, tiers)                                          | Branch on the qualifier's `fit_tier` or the search URL's facet and lock one channel id per branch (`infra/plays/route-new-hires.ts`) | One channel id per branch to resolve and keep current                                                                                                   |
| `find_email`          | The team wants the work email on the post, ready for its own sequencer                           | Add Cargo's native Find Email tool after the gate and put the email on the post (`infra/plays/route-new-hires.ts`)                   | One email lookup per qualified person                                                                                                                   |
| `draft_first_touch`   | The team wants a first email written, not just the signal                                        | Add a writing agent after the gate and put its draft in the post (`infra/plays/route-new-hires.ts`)                                  | One more LLM call per qualified person, and copy that has to be reviewed before it is trusted. The play still sends nothing                             |

## What should not change

However far you adapt, these hold. Ask for one anyway and the agent tells you what breaks, then does
it if you still want it, and records why under `## Decisions` in your copy of this file.

- **The three job-change filters stay in every search URL.** (`infra/models/new-hires.ts`)
  Recently changed jobs, under a year at the company, under a year in the position. Remove one and
  internal promotions at long-tenured employees flood in, read as new hires, and fill the channel
  with people who have been at the company for a decade.
- **Enrich the company first, and stop when there is no domain.** (`infra/plays/route-new-hires.ts`)
  A Sales Navigator lead has a company URL, not the firmographics the qualifier judges on. A company
  page with no website is rarely an operating business, and every CRM variation matches on the
  domain.
- **The qualifier's verdict gates the post.** (`infra/plays/route-new-hires.ts`,
  `infra/agents/icp-qualifier.ts`) Without the gate every new hire in the market is posted, and the
  channel stops being read within a week.
- **The ICP lives in the workspace context, not in the prompt.** (`infra/agents/icp-qualifier.ts`)
  In the prompt, changing who qualifies becomes a deploy, and the search and the qualifier drift
  apart because they no longer read the same file.
- **The channel is locked in the play.** (`infra/plays/route-new-hires.ts`) A channel computed per
  run, or chosen by an agent, can land a prospect's name in a customer's shared channel.
- **`changeKinds: ["added"]` stays.** (`infra/plays/route-new-hires.ts`) Each sync re-extracts the
  whole search. Without `added`, every sync re-posts everyone in it and re-pays for every
  enrichment and every qualifier call.
- **The model ships with no schedule.** (`infra/models/new-hires.ts`) The cadence is added when
  opening up. Deleting a live schedule later does not clear it, so the pilot never carries one.
- **The play ends at the Slack post.** (`infra/plays/route-new-hires.ts`) Sending belongs to the
  team's own sequencer, after a person has read the post. A play that sends on a job-change signal
  mails people in their first week with nobody reviewing it.

## Done when

- each deployed search URL was counted with `searchPersonMetrics`, sits under 2,500, and keeps the
  three job-change filters
- the pilot synced ten rows whose columns match the workflow input
- every run in the pilot ended in a named status, and every `posted` run is shown with its Slack
  message
- a `not_icp` run shows the qualifier's rationale, and posted nothing
- every post landed in the channel the operator named, and nowhere else
- `node --import tsx evals/contract.mjs` passes against the adapted resources
- after opening up, the next sync created runs only for people new since the previous one

## What it costs

Fetch live prices before every estimate: `cargo-ai connection integration get salesNavigator`,
`linkedin`, and the LLM connector's model. Quote the lookup time with the estimate.

**Extraction is the main spend, and it repeats.** `fetchLeadSearch` bills per extracted lead, and
it is not incremental: every sync extracts the whole search again, including the people already in
the model. "Changed jobs" spans roughly the last 90 days, so a sync every two weeks re-pays for most
of the previous sync to find the ones who are new. One sync costs the counted search (capped at
`limit` per URL) times the per-lead price; a month costs that times the number of syncs.

**Qualifying is per new person, and only new people.** Each run pays one company enrichment, and
each company with a domain adds one qualifier call. The Slack post carries no per-call price of its
own. The CRM variations add their own lookups and, on `crm_routing`, an email lookup per person.

**Counting is cheap and comes first.** One `searchPersonMetrics` call per candidate URL tells you
what a sync will extract before anything is extracted.

## Composes into

`find-work-email` or `enrich-linkedin-profile` for the people the team decides to contact, and
`agentic-engagement` to hold the conversation once a person reads the post and the team writes
first.
`track-job-changes` is the sibling for people already in your CRM.
