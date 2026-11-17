---
name: pontx-open-exchange-rates
description: Use for direct Open Exchange Rates integration, plan-aware historical-rate retrieval, currency-conversion safeguards, and caller-owned App ID handling.
---

# Open Exchange Rates

Use this skill when an application needs Open Exchange Rates data through a
caller-directed integration. Resolve the current API contract instead of
memorizing request fields, generated method names, or package versions:

```bash
pontx-hub search "Open Exchange Rates <capability>" --type endpoint --json
pontx-hub show <returned-resource-id>
pontx-hub sdk open-exchange-rates
```

Use `@pontx/open-exchange-rates` for application code. Use
`pontx-open-exchange-rates` for a product-local script after checking the
current SDK guidance. Keep the App ID credential in the caller environment;
never paste it into chat, source control, or a command transcript.

## Keep reads caller-directed

Use the local SDK or CLI rather than trying to execute the supplier request
through Hub. First produce a redacted local preview, verify the chosen
resource and plan, and perform a live read only after explicit approval. A
read-only API does not make a credential safe to disclose.

Open Exchange Rates passes the caller's unique App ID as an HTTPS query
parameter. Let the SDK or CLI construct that request from the environment
rather than interpolating the value into application logs.

## Choose a plan-aware workflow

Time-series requests are currently available only to Enterprise and Unlimited
plans. Time-series requests have a maximum query period of one month. Split a
long report into bounded monthly reads, select only the required currencies,
and account for the request quota before approving execution.

Currency conversion requests are currently available only to the Unlimited
plan. Validate converted values before using them in a transaction-processing
system. Treat results as application input that needs the caller's own
financial controls, rounding policy, and approval boundary.

If a requested capability, plan, or execution path conflicts with the current
Pontx resource, stop and report the discrepancy instead of guessing a URL or
falling back to an undocumented request.

## Few-shot workflows

### Scenario 1: Prepare a local rate integration

**User:** "Add a latest-rates lookup to our Node service, but do not call the
provider yet."

**Approach:** Discover the current resource and SDK guidance, generate local
SDK code that reads an environment-held credential, then show a redacted
preview. Do not execute or expose the App ID.

### Scenario 2: Plan a historical report

**User:** "Prepare an eight-week EUR report for the currencies our finance team
uses."

**Approach:** Check plan eligibility, divide the work into bounded monthly
time-series reads, filter to the requested currencies, estimate quota impact,
and present previews. Execute only the unchanged approved reads.

### Scenario 3: Review a conversion workflow

**User:** "Use Open Exchange Rates to calculate a checkout total."

**Approach:** Check that the caller has the required plan, keep the request
local, preview it without a credential, and require the application's own
validation and rounding decision before any financial transaction proceeds.
