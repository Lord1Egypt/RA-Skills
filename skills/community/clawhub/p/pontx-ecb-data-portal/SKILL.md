---
name: pontx-ecb-data-portal
description: Integrate ECB Data Portal statistics through Pontx. Use for dataflows, DSDs, codelists, series keys, frequency-aware periods, bounded or incremental retrieval, availability, and SDMX formats.
---

# ECB Data Portal

Use this skill when an ECB statistics task needs SDMX discovery, query design,
incremental ingestion, or representation choices beyond the API metadata.

## Start with the current contract

Do not copy Endpoint names, parameters, Schemas, formats, generated symbols,
auth, or versions into a durable answer. Resolve the current facts through
Pontx:

```bash
pontx-hub search "<ECB dataset, series, or integration goal>" --json
pontx-hub show <returned-resource-id>
pontx-hub sdk ecb-data-portal
```

Use `@pontx/ecb-data-portal` for application code. Use
`pontx-ecb-data-portal` only for a single-product script after inspecting its
current contract. Hub can discover and preview this product but does not proxy
its live requests.

Preview the exact bounded request before any live retrieval:

```bash
pontx-hub ecb-data-portal preview <controller> <api-name> <named-options>
```

Execute through the caller-owned SDK or product CLI only when the user
explicitly approves the unchanged GET. Keep credentials and tokens out of
arguments, source, logs, and generated examples.

## Discover structure before data

When the series is unfamiliar, identify the dataflow, inspect its DSD, and load
the required codelists. The API series key follows DSD dimension order, uses
dots between dimensions, empty segments for wildcards, and plus signs for
alternative values. Validate order and codes rather than guessing them.

Reporting-period syntax depends on the selected series frequency.

## Bound and synchronize retrieval

- Bound every broad wildcard query through the live contract before retrieval.
  Observation limits apply to every matching series and are not cursor
  pagination; partition a large job by non-overlapping keys or periods.
- The portal can enumerate matching series without returning observations. Use
  the availability-only mode shown by the live contract before downloading data.
- Choose the representation deliberately: a processing format for applications,
  tabular output for analysis, or SDMX output for SDMX tooling. Inspect current
  media types and compression options through `pontx-hub show`.
- For recurring ingestion, retain a successful checkpoint and inspect the live
  change-detection contract. Apply additions, revisions, and deletions rather
  than treating a response as append-only.

## Handle failures and meaning

Interpret an empty or no-match result using the live contract rather than as
proof that the entire dataset is absent. Correct invalid requests or
representations before retrying; retry temporary failures only with bounded
backoff.

Do not silently aggregate frequencies. Preserve series metadata so observations
retain their statistical meaning. Document any application transformation.
Do not present an observation as real-time, unrevised, or suitable for a
financial decision without current authoritative support.

## Few-shot workflows

### Scenario 1: Latest observation

**User:** "Get the latest monthly USD/EUR ECB value."

**Approach:** Apply the discovery and bounded-retrieval workflow above, preview
the resulting single-series request, and retrieve only after explicit approval.
Report the result's period and revision context.

### Scenario 2: Series availability

**User:** "Which daily currencies against EUR exist? Do not download values."

**Approach:** Apply the structure-discovery and availability workflow above to
a deliberate bounded query. Treat an empty result as local to that query.

### Scenario 3: Incremental ingestion

**User:** "Keep our ECB mirror current without full downloads."

**Approach:** Apply the bounded synchronization workflow above, persist only a
successful checkpoint, process each update atomically, and never invent a page
token or advance after partial failure.
