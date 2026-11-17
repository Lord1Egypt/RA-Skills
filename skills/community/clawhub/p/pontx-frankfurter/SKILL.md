---
name: pontx-frankfurter
description: Maintain legacy Frankfurter v1 integrations through Pontx. Use for existing v1 applications, reproducible dated reference-rate work, or deciding whether new provider-aware work should move to pontx-frankfurter-v2.
---

# Frankfurter v1

Use this skill for tasks that explicitly depend on Frankfurter v1. For a new
integration, first decide whether the provider-aware v2 product is a better fit.

## Choose the contract before coding

Frankfurter v1 is superseded by v2 but remains available. Keep v1 when an
existing integration explicitly depends on the v1 contract.

Prefer `pontx-frankfurter-v2` for new work that needs provider selection,
attribution, broader history, grouping, or streaming. Treat migration as an
application contract change: compare both live contracts, explain the
differences, and obtain approval before changing a parser or request.

## Resolve live facts through Pontx

Do not memorize Endpoint names, parameters, Schemas, auth, generated symbols,
or package versions. Load only what the task needs:

```bash
pontx-hub search "Frankfurter v1 <capability>" --type endpoint --json
pontx-hub show <returned-resource-id>
pontx-hub sdk frankfurter
```

Use the published `@pontx/frankfurter` package for application code. Use
`pontx-frankfurter` only for a single-product script, after inspecting its
current contract through `pontx-hub sdk frankfurter`.

For a request, use the controller and API name returned by Pontx:

```bash
pontx-hub frankfurter preview <controller> <api-name> <named-options>
pontx-hub frankfurter call <controller> <api-name> <named-options>
```

Preview first. Execute the unchanged read only when the user explicitly asks
for live retrieval. Never expose or invent a credential; recheck the selected
resource if current metadata says authentication is required.

## Preserve v1 semantics

- V1 dates are interpreted in UTC, and latest means the latest available
  working day rather than the user's current calendar day.
- Use an explicit completed date rather than `today` for a reproducible report.
- Filtering target currencies makes a v1 time-series response smaller and
  faster. Ask for only the currencies required by the calculation.
- Perform amount conversion in application code. Use decimal-capable arithmetic
  for accounting and round only at the declared business boundary.
- Describe the values as reference exchange rates, not guaranteed execution or
  settlement prices.
- Keep version-specific adapters separate. A parser should not guess which
  contract produced a response.

If the product guidance and the current Pontx contract differ, stop and surface
the conflict. Use `show` and `sdk` for executable facts; do not work around the
catalog with a guessed URL or signature.

## Few-shot workflows

### Scenario 1: Maintain a legacy application

**User:** "Our service already imports `@pontx/frankfurter`; add CAD and JPY
without migrating."

**Approach:** Keep v1, inspect the live SDK and selected Endpoint, preserve the
existing application contract, and preview any live read. Do not introduce v2
facts or a fixed package version.

### Scenario 2: Select a compliance-ready source

**User:** "Build a new report that must identify the central bank behind each
rate."

**Approach:** Apply the v2-routing decision above, load its live contract, and
ask which authority controls the calculation before generating integration
code.

### Scenario 3: Prepare a reproducible series

**User:** "Prepare, but do not run, a v1 date-range request for an audit."

**Approach:** Apply the reproducibility and response-size workflow above,
inspect the current time-series contract, then show the exact preview without
executing it.
