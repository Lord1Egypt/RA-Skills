---
name: inbound-qualification
description: 'Qualify and route inbound demo requests from your website form: each submission runs a Cargo tool that identifies the company by work email, qualifies it against your ICP, lands the account and contact in the shared models, posts it to Slack, and answers with a booking link or a thank-you; an optional play then tiers and summarises each qualified contact. Triggers: "add a demo form to our website", "handle inbound leads", "route website form submissions", "qualify inbound demo requests", "contact form that books meetings", "inbound lead flow", "Cargo public form", "tier each demo request and summarise it". Cargo project, defineTool, publicForm, form-sdk, definePlay, gtm_accounts, gtm_contacts. Skip when: you want visiting companies that fill nothing in, which is visitor-identification; no site yet, which is website-building first; or leads from a list, which is find-b2b-leads.'
version: "0.2.2"
compatibility: "Requires @cargo-ai/cli with @cargo-ai/cdk 1.0.98 or later (token-valued app env), @cargo-ai/form-sdk 1.0.3 or later in the website app, a website on Cargo Hosting (website-building), Node.js 22.18 or later, and a Cargo workspace."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/inbound-qualification
metadata:
  author: getcargo
  source: cookbook
  personas:
    - marketing
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

# Inbound qualification

## The outcome

Someone asks for a demo on the website, and within seconds their company is identified and
qualified, they land in the workspace's accounts and contacts, the team hears about it in Slack,
and the page answers them: a booking link if they fit, a thank-you otherwise. There is no backend
to run and no form vendor: the form is a Cargo tool.

Five pieces make it:

1. **A tool with a public form.** `defineTool("inbound_form", { workflow, publicForm })`. The
   workflow's input is the form's fields; `publicForm` allows only the site's origin and sets the
   spam guards. Each submission runs the workflow.
2. **The workflow.** Refuse a personal email before anything is paid; identify the company from
   the email domain with LinkedIn company data; apply the ICP rules; upsert the account into
   `gtm_accounts` and the contact into `gtm_contacts`; post one Slack message; return the answer.
3. **The shared GTM models.** `gtm_accounts` and `gtm_contacts`, declared exactly as every pipeline
   declares them, so whatever else the project installs reads the same inbound contacts.
4. **The form on the site.** Rendered with the site's own markup and run headless through
   `@cargo-ai/form-sdk`, loaded once the page has hydrated. The tool's uuid arrives as the
   app env token `inboundForm.uuid`.
5. **Deep research, after the page has answered.** A play on `gtm_contacts`, shipped disabled,
   runs once for each contact the form marked `qualified`: an agent reads the ICP and the tiering
   rubric from the workspace context, researches the company and the person's role with web
   search, and returns a tier and a three-sentence brief. The play writes `inbound_tier`,
   `inbound_brief`, `inbound_rationale` and `inbound_researched_at` onto the contact and posts a
   short note to the same channel. It never runs on the submission path, so the visitor never
   waits on it.

**Two things worth knowing before you start.** The company is enriched, never the person: the
person already said who they are. And the server's minimum fill time counts from when the SDK
loaded, which is why the site loads it once the page has hydrated: a form loaded on a lost focus
event would stamp and submit in the same moment and be refused as a bot.

## Example

> Add a demo form to www.fabrikam.example: qualified companies get our booking link, the rest a thank-you, and the sales channel hears about every request.

Illustrative output, fictional records:

```text
tool:inbound_form        deployed   public form on https://www.fabrikam.example
POST /contact            ada@northwind.example    -> qualified      (320 employees, United States)
  gtm_accounts           northwind.example        upserted
  gtm_contacts           ada@northwind.example    lead_source website, inbound_status qualified
  #inbound               "New inbound, qualified from Ada Lovelace at Northwind"
  page                   "Thanks, let's find a time."  [Book a demo]
play research_qualified_leads (minutes later, once enabled)
  gtm_contacts           ada@northwind.example    inbound_tier A, inbound_brief written
  #inbound               ":mag: Ada Lovelace: tier A. Head of RevOps at Northwind, ..."
POST /contact            sam@gmail.com            -> work_email_required   (nothing paid or written)
```

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job is
to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if
not, this is enough.

1. **Install it: the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/inbound-qualification` writes the tool and models to
   `infra/inbound-qualification/` and this procedure, with the `site/` files, to
   `.claude/skills/inbound-qualification/`. No project yet?
   `cargo-ai project init <dir> --cookbook inbound-qualification && cd <dir> && npm install`.
   **If you are reading this from the project's `.claude/skills/`, the install already happened;
   start at step 2.**
2. **Reconcile it with what is already declared.** The website must already be declared, usually
   by `website-building`. A `gtm_accounts` or `gtm_contacts` another pipeline declares is the same
   model: import that one and delete this copy. A Slack or LinkedIn connector the project already
   has is rewired to.
3. **Wire the site.** Follow [form](references/form.md): copy `site/` into the website app, add
   the dependency and the env token, link the contact page.
4. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about (say what breaks, then do it if they still want it); _What you can change_ is what you
   offer unprompted; _What you will be asked_ is the floor, and you derive before you ask. Record
   what you changed and why under a `## Decisions` section in your copy of this file.
5. **Plan, then stop.** `node --import tsx evals/contract.mjs` from this skill's folder, then
   `npm run check && cargo-ai project plan` from the project root, show the diff, and deploy only on
   an explicit yes: `cargo-ai project deploy`. If the project deploys from CI, the merged pull request
   is the deploy; do not also deploy from a laptop.
6. **Verify.** Walk _Done when_ line by line with real submissions, and report each with evidence.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked.

| Input                                     | Kind    | How it is answered                                                                              | Why it matters                                                                                            |
| ----------------------------------------- | ------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| ICP rules (`infra/tools/inbound-form.ts`) | derived | the ICP in `context/`: headcount band and ISO country codes, confirmed with one live enrichment | Decides who sees the booking link. Rules nobody can read back are the reason inbound stops being trusted. |
| site origin (`publicForm.allowedOrigins`) | derived | the website app's `site.json` `canonicalUrl`, without the trailing slash                        | Every other origin is refused with 403. A missing origin is a form that never submits.                    |
| Slack channel (`infra/settings.ts`)      | asked   | the channel's id, resolved through the Slack connector's autocomplete                           | Every submission and every research note is posted there and only there.                                  |
| booking link (`bookingUrl`)               | asked   | the team's scheduling page                                                                      | What a qualified visitor is sent to, on the page, while they are still on it.                             |
| privacy disclosure                        | asked   | the operator's reviewed page, with a contact form section                                       | The form collects personal data. This skill never writes legal text.                                      |
| tiering rubric (deep research)            | derived | the ICP and the account tiering rubric in `context/` (account-scoring's, when installed)        | What the research agent tiers against. With no rubric it tiers on the ICP alone and says so.              |
| enable the research play                  | asked   | after a pilot: run `research_qualified_leads` by hand on one qualified contact, read the note   | Each run pays for an agent call. It ships disabled, and `added` does not backfill while it was off.       |

Checked before moving on, not after the deploy:

- the ICP rules match `context/`, and one live `enrichCompanyFromDomain` on a known customer
  returned the ISO country code the rules use
- `allowedOrigins` is exactly the canonical origin
- the Slack channel id resolves through the connector
- `node --import tsx evals/contract.mjs` passes against the adapted graph

## What you can change

The code is a worked example. These reshapes are expected, and the agent offers them rather than
waiting to be asked. Every one costs something.

| Variation               | When it is right                                          | How                                                                                                                                          | What it costs                                                                              |
| ----------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `crm-backed`            | Contacts belong in HubSpot, Salesforce or Attio           | Replace the two `model.upsert` calls with the CRM connector's upsert (matched on domain and email), same fields ([data](references/data.md)) | The worked example no longer deploys on a bare workspace; CRM properties must exist first. |
| `agent-qualification`   | The ICP does not reduce to headcount and country          | Replace the rules with an agent that reads the ICP from `context/` and returns a verdict and a reason                                        | Each submission pays for a model call, and the answer is less predictable.                 |
| `owner-routing`         | More than one rep takes inbound                           | Assign `owner_id` on the contact by territory or round robin before the Slack post, and mention the owner                                    | An owner table to keep current, and a fallback when nobody matches.                        |
| `turnstile`             | Spam gets through the honeypot, time-trap and rate limit  | `publicForm.spam.captchaProvider: "turnstile"`, the site key, `captchaSecret: env("TURNSTILE_SECRET")`, the widget on the page               | A third-party script on the page, with its own privacy disclosure.                         |
| `accept-personal-email` | A form that is not about the company (newsletter, events) | Drop the free-mail refusal, skip enrichment for those domains                                                                                | No company to qualify or route; those contacts arrive without an account.                  |
| `no-deep-research`      | The form's rules and the Slack post are enough            | Delete `infra/plays/research-qualified-leads.ts`, `infra/agents/lead-researcher.ts` and the Anthropic connector                              | No tier or brief on the contact; the team researches by hand.                              |
| `research-every-submitter` | Not-qualified leads are worth a look too               | Drop the `inbound_status` condition from the research play's filter                                                                         | An agent call per submission, including the ones the rules already turned away.            |

## What should not change

However far you adapt, these hold. Ask for one anyway and the agent tells you what breaks, then does
it if you still want it, and records why under `## Decisions` in your copy of this file.

- **The public form allows only the site's origin.** (`infra/tools/inbound-form.ts`) `*` lets any
  page on the internet submit into the workspace and spend its credits.
- **Nothing is paid or written before the cheap checks.** A personal email is refused before the
  enrichment call; the paid call comes before any write.
- **The company is enriched, never the person.** No person lookup, no personal email or phone
  search on a submitter.
- **The shared models stay shared.** `gtm_accounts` and `gtm_contacts` keep their exact definition;
  what only inbound needs is an added column under a plain name.
- **No CAPTCHA secret in the repository.** It goes through `env()`.
- **The SDK loads once the page has hydrated.** (`site/components/inbound-form.tsx`) Its load
  time is what the minimum fill time counts from. Loaded on a focus event, a focus before hydration
  is lost and the visitor's submission is refused as a bot. Its id cookie is set only on submit.
- **Research never runs on the submission path.** (`infra/plays/research-qualified-leads.ts`) The
  form's workflow calls no agent; the research is a separate play on the contact row. Inside the
  form's workflow it would hold the page answer for as long as the research takes, and a slow
  search would show the visitor a spinner instead of a booking link.
- **Workflow bodies stay plain.** Calls, writes and template strings. A body is parsed from source,
  and optional chaining (`?.`) passed check and plan, then failed a live run with
  `OptionalMemberExpression … got "MemberExpression"`. The contract rejects `?.` and `??` in the
  research play's compiled expressions.
- **Marketing email only with the box ticked.** `marketing_consent` is recorded per contact; a
  demo request alone is not consent to a newsletter.

## Done when

- `node --import tsx evals/contract.mjs` passes: one tool whose public form is enabled for exactly
  the canonical origin with no CAPTCHA secret in code, a workflow that refuses personal email
  before the enrichment call and writes only `gtm_accounts` and `gtm_contacts`, both models
  matching the shared definitions
- the plan shows the tool, the models and the connectors, and the app update with the env token
- a work-email submission on the live site returns the right answer on the page, upserts the
  account and the contact (with `account_id`, `lead_source` `website`, `inbound_status`), and
  posts once to the Slack channel
- a personal-email submission is refused on the page, with no enrichment call and no row written
- a submission from another origin is refused with 403, and one sent faster than the minimum fill
  time is refused
- loading the contact page sets no `cargo_anon_id` cookie until a submission
- the privacy page has a contact form section the operator reviewed
- the research play, run by hand on one qualified contact, wrote `inbound_tier`, `inbound_brief`,
  `inbound_rationale` and `inbound_researched_at` onto it and posted one note; a second manual run
  on the same contact did nothing
- every fact in the brief traces to the record or a listed source

## What it costs

Each submission from a work email pays for one LinkedIn company enrichment; a refused personal
email pays nothing. Read the live price from the integration (`cargo-ai connection integration get
linkedin`) and say it per submission. The server's rate limit caps a single address at ten
submissions a minute, and the origin allow-list keeps other sites from spending it. The models and
the Slack post add nothing. The deep research, once enabled, adds one agent run per qualified
contact (LLM tokens on the Anthropic connector plus up to four web searches); a not-qualified or
personal-email submission never reaches it.

## Composes into

`website-building` (the site the form sits on), `visitor-identification` (the companies that read
the site without filling the form in), `account-scoring` (its tiering rubric is the one the research
tiers against, so an inbound lead and a sourced account are tiered alike), `score-leads` (inbound
contacts scored against the ICP before a rep calls), and `agentic-engagement` (a follow-up to a contact who ticked the consent box).
