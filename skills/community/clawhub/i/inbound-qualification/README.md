# Inbound qualification: qualify and route demo requests from your website

To qualify inbound demo requests, wire the website's demo form to a Cargo tool: each submission is
matched to its company by work email, checked against your ICP, landed in the shared go-to-market
accounts and contacts, posted to Slack, and answered on the page with a booking link or a thank-you.
A personal email address is refused on the page before anything is paid for or written.

```sh
cargo-ai project add cookbook/inbound-qualification
```

```text
visitor submits /contact/ (headless form SDK, the site's own markup)
  -> public form API: origin, honeypot, time-trap, rate limit
  -> tool inbound_form: personal email? -> company from LinkedIn -> ICP rules
       -> gtm_accounts + gtm_contacts -> Slack
  <- booking link or thank-you, when the run finishes (async: the SDK polls)

later, for each contact marked qualified (play research_qualified_leads, ships disabled)
  -> agent: ICP + tiering rubric from context, web research -> tier, brief
  -> inbound_tier / inbound_brief / inbound_rationale / inbound_researched_at on the contact
  -> one note to the same Slack channel
```

## Why it is built this way

**A tool, not a backend.** Cargo tools take a public form: the workflow's input is the field list,
`publicForm` holds the origin allow-list and the spam guards, and each submission runs the
workflow. Nothing else to host.

**The shared GTM models.** The account and the contact land in `gtm_accounts` and `gtm_contacts`,
declared exactly as every pipeline declares them, so the worked example deploys on a bare
workspace and other pipelines read the same inbound contacts. A CRM is the `crm-backed` variation.

**Cheapest refusal first.** A personal email is refused before the paid company lookup; the lookup
comes before any write. The company is enriched, never the person.

**Rules, not a model call.** Headcount band and countries from the ICP: free, explainable, the
same answer twice. An agent judgement is a variation.

**Research after the answer.** The deep research is a separate play on the contact row, never
part of the form's workflow, so the visitor never waits on a model call. It ships disabled and
runs once per qualified contact.

**The SDK loads after hydration.** Its load time is what the server's minimum fill time counts
from, so it loads when the form becomes usable. It sets its id cookie only on submit, so a visitor
who never submits gets none.

## Placeholders (edit before deploy)

1. **ICP rules**: `icpMinEmployees`, `icpMaxEmployees`, `icpCountries` in `infra/tools/inbound-form.ts`.
2. **Booking link**: `bookingUrl`.
3. **Slack channel**: `slackChannelId` in `infra/settings.ts`, shared by the form and the research
   note.
4. **Origin**: `publicForm.allowedOrigins`, the site's canonical origin.

## Files

| Path                               | What it is                                              |
| ---------------------------------- | ------------------------------------------------------- |
| `infra/tools/inbound-form.ts`      | The tool, its workflow and its public form              |
| `infra/plays/research-qualified-leads.ts` | The deep-research play, shipped disabled         |
| `infra/agents/lead-researcher.ts`  | The research agent: tier and brief, as JSON             |
| `infra/settings.ts`                | The Slack channel both post to                          |
| `infra/connectors/anthropic.ts`    | The model the research agent runs on                    |
| `infra/models/gtm-accounts.ts`     | The shared GTM accounts model                           |
| `infra/models/gtm-contacts.ts`     | The shared GTM contacts model, with the inbound columns |
| `infra/connectors/linkedin.ts`     | LinkedIn company data on Cargo's credits                |
| `infra/connectors/slack.ts`        | The Slack workspace the inbound channel lives in        |
| `site/components/inbound-form.tsx` | The form, headless, loading the SDK after hydration     |
| `site/app/contact/page.tsx`        | The page that holds it                                  |
| `references/form.md`               | Wiring the site, the spam checks, privacy               |
| `references/data.md`               | The rows, querying, the `crm-backed` mapping            |
| `evals/contract.mjs`               | Graph contract                                          |

## Verify

```sh
node --import tsx inbound-qualification/evals/contract.mjs
```
