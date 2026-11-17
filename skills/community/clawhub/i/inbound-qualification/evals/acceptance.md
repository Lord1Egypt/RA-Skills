# Acceptance

## Before deploy

- The website exists on Cargo Hosting, and `publicForm.allowedOrigins` is exactly its canonical
  origin (no trailing slash).
- The ICP rules in `infra/tools/inbound-form.ts` match `context/`, and one live
  `enrichCompanyFromDomain` on a known customer returned the ISO country codes they use.
- `slackChannelId` is a channel id the Slack connector resolves, and `bookingUrl` is the team's
  scheduling page.
- A `gtm_accounts` or `gtm_contacts` another pipeline declares is imported, not duplicated.
- `site/` is copied into the app, `@cargo-ai/form-sdk` is a dependency of the app, `/contact/` is
  linked, and the app's `defineApp` env has `NEXT_PUBLIC_CARGO_FORM: inboundForm.uuid`.
- The privacy page has a contact form section the operator reviewed.
- `node --import tsx evals/contract.mjs` passes from this skill's folder.
- `npm run check && cargo-ai project plan` pass; the plan shows the tool, the models, the connectors and
  the app update.

## After deploy

- `/contact/` in a private window sets no `cargo_anon_id` cookie until a submission, and its one
  call before then is the form schema.
- A personal-email submission shows "Please use your work email"; the run makes no enrichment call
  and writes no row.
- A work-email submission from a company that fits shows the booking link; one that does not
  shows the thank-you. Each upserts the account and the contact (`account_id`, `lead_source`
  `website`, `inbound_status`, the UTMs, `marketing_consent`) and posts once to the channel.
- A second submission from the same email updates the contact instead of adding one.
- A submission from a preview URL is refused with 403; one sent before `minFillMillis` is refused.

## Deep research

- `research_qualified_leads` is deployed disabled. Run by hand on one contact with
  `inbound_status` `qualified`, it writes `inbound_tier`, `inbound_brief`, `inbound_rationale` and
  `inbound_researched_at` onto that contact and posts one note to the channel; the run ends in
  success.
- A second manual run on the same contact creates no run: `inbound_researched_at` is set.
- A `not_qualified` contact is never picked up.
- Every fact in the brief traces to the contact, the company row or a listed source.
