---
name: pontx-nager-date
description: Use for Nager.Date Community API v4 public-holiday integration, country or holiday lookups, commercial-use eligibility checks, and direct read-only SDK or CLI workflows.
---

# Nager.Date Community API v4

Start with live Pontx discovery rather than copying API fields into an
application. Use the universal CLI to resolve the current product, Endpoint,
Schema, and package guidance:

```bash
pontx-hub search "public holidays for a country" --type endpoint --json
pontx-hub show <returned-resource-id>
pontx-hub sdk nager-date
```

Use `@pontx/nager-date` in application code and `pontx-nager-date` for an
optional local script. Nager.Date Community API v4 is a public service for
public-holiday information. It is a caller-directed service: keep upstream
responses in the caller's application and do not treat Hub documentation as a
proxy, cache, or holiday-data portal.

## Check use eligibility before integration

Nager.Date Community API terms allow private or non-profit projects and require
active sponsorship for commercial use. Confirm the project's entitlement with
the provider before scheduling production reads, redistributing data, or
building a user-facing calendar. Do not guess a sponsorship status from a
successful response.

The Community API does not require a credential in the official v4 contract.
That does not remove the terms boundary, justify bulk collection, or permit an
application to use unbounded retries. Keep calls narrow, cache only where the
provider terms and your application policy permit, and surface upstream
availability separately from date-calculation logic.

## Make reads reproducible

Resolve the current endpoint and input constraints first, then preview the
exact caller-directed request locally:

```bash
pnpm exec pontx-nager-date list apis
pnpm exec pontx-nager-date call <controller> <method> --dry-run
```

The product has only read endpoints, so no mutation confirmation is needed.
Still review the rendered path, country/subdivision code, year, and date/time
assumptions before executing. Treat an empty successful response as its own
documented outcome, not as a transport failure or a reason to invent data.

## Few-shot workflows

### Scenario 1: Plan a country-holiday lookup

**User:** "Which public holidays should our US rollout calendar exclude in
2026?"

**Approach:** Check commercial-use eligibility first, discover the current
year-and-country endpoint and holiday schema, preview a narrow local read, and
return only the fields needed for the caller's calendar policy.

### Scenario 2: Check today's automation window

**User:** "Should this country's daily job run today?"

**Approach:** Resolve the current holiday-status endpoint, confirm the country
or subdivision and UTC-offset semantics, and distinguish each documented
success status. Do not substitute a local timezone guess for the requested
offset.

### Scenario 3: Adopt it in a commercial product

**User:** "Add Nager.Date to our paid scheduling app."

**Approach:** Stop before implementation to confirm active provider
sponsorship. Once eligibility is confirmed, retrieve the current SDK and
contract facts, add a narrow read path, and keep upstream data out of Hub or
other public aggregation layers.
