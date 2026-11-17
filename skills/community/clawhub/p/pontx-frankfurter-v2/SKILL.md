---
name: pontx-frankfurter-v2
description: Integrate Frankfurter v2 through Pontx for reference-rate conversion, provider-pinned compliance, auditable time series, attribution, and large exports. Use for FX or central-bank rate tasks.
---

# Frankfurter v2

Use this skill for daily reference exchange-rate work. Frankfurter v2 returns
daily reference exchange rates, not executable trading quotes.

## Load the current contract

Do not memorize Endpoint names, parameters, response fields, providers, auth,
generated symbols, or package versions. Resolve them for the current task:

```bash
pontx-hub search "Frankfurter v2 <capability>" --type endpoint --json
pontx-hub show <returned-resource-id>
pontx-hub sdk frankfurter-v2
```

Use `@pontx/frankfurter-v2` for application integration. Use
`pontx-frankfurter-v2` only for a single-product script, and derive its current
commands from SDK metadata rather than guessing.

Use the flat collection form shown by the live contract:

```bash
pontx-hub frankfurter-v2 preview <api-name> <named-options>
pontx-hub frankfurter-v2 call <api-name> <named-options>
```

Preview the resolved request first. Execute the unchanged GET only when the
user explicitly approves live retrieval. Never expose or invent a credential.

## Choose rate semantics first

Clarify the pair or quote set, observation date or range, intended use, and
required provider before constructing a request.

The default v2 result blends providers, while provider filtering is required
when a specific official source controls a tax, accounting, or compliance
calculation. Ask which jurisdiction or publishing authority controls the rule.
Never silently replace a missing provider-specific observation with the blend.

A pinned provider can publish on a different cadence, so its latest observation
can lag the blended result. Report the returned observation date and do not
relabel it as today's rate. When attribution is requested, retain contributor
information; a peg-derived row may not have provider attribution.

## Integrate deliberately

- Fetch the rate only and keep the monetary amount in application code. Use
  decimal-safe arithmetic for accounting, round at the declared business
  boundary, and format the target currency for the user's locale.
- For an audit, retain the normalized query, provider, observation date,
  retrieval time, and raw response used by the calculation.
- For long ranges, narrow quotes and providers and choose weekly or monthly
  grouping when daily resolution is unnecessary. For large responses, choose a
  streaming representation from the live contract instead of buffering the
  full export.
- If live retrieval fails, re-inspect the current contract and preserve the
  required provider semantics while choosing a smaller request.
- Handle every non-success response explicitly. Validate identifiers through
  the current contract instead of inventing a currency or provider key.

If product guidance conflicts with Pontx metadata, stop and surface the
conflict. Do not bypass the catalog with a guessed request.

## Few-shot workflows

### Scenario 1: Display conversion

**User:** "Show an approximate EUR value for a USD cart total."

**Approach:** Apply the rate-semantics and local-conversion workflow above,
inspect the live single-pair contract, preview it, and retrieve only after
explicit approval. Preserve the returned observation context.

### Scenario 2: Auditable official rate

**User:** "Convert an invoice using the authority required by our jurisdiction."

**Approach:** Apply the provider-selection and audit workflow above, ask for the
controlling authority if absent, preview the exact live contract, and do not
silently change its semantics.

### Scenario 3: Large attributed history

**User:** "Analyze a decade of monthly rates with attribution under a memory
limit."

**Approach:** Apply the large-range workflow above after inspecting current
grouping, attribution, provider, and representation support. Preserve rate
semantics while verifying dates and ordering.
