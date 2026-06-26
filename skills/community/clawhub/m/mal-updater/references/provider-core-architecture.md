# MAL-Updater provider/core architecture

Date: 2026-03-20

This note describes the initial provider-agnostic refactor that separates MAL-Updater's common core from provider-specific source integration code.

## Goals

- keep mapping, review queue, ingestion, sync planning, recommendations, and MAL writes in the common core
- isolate provider-specific auth/session/fetch/normalization code behind a provider module boundary
- preserve existing Crunchyroll behavior and operator commands while introducing a future-proof provider API
- create a clean landing zone for HIDIVE implementation

## New core seams

### Provider-neutral snapshot contract

Common normalized contract now lives under:
- `src/mal_updater/contracts/provider.py`

Key exported dataclasses:
- `ProviderSnapshot`
- `SeriesRef`
- `EpisodeProgress`
- `WatchlistEntry`

Notes:
- `contracts/crunchyroll.py` now aliases the generic contract for backward compatibility
- `validation.py` now validates a generic provider snapshot instead of enforcing `provider == "crunchyroll"`

### Provider registry

New registry module:
- `src/mal_updater/provider_registry.py`

Purpose:
- register provider modules by slug
- resolve providers from generic CLI entrypoints
- list available provider slugs for argument parsing

### Provider interface types

New type definitions:
- `src/mal_updater/provider_types.py`

Important types:
- `ProviderCapabilities`
- `ProviderFetchResult`
- `ProviderModule` protocol

These describe the minimal contract expected from provider modules:
- provider identity
- capability declaration
- normalized snapshot fetching
- normalized snapshot file writing

## Provider modules

### Crunchyroll provider module

New module:
- `src/mal_updater/providers/crunchyroll.py`

Current behavior:
- wraps the existing Crunchyroll auth/fetch implementation
- exposes the provider via the new provider registry
- returns normalized provider-neutral snapshot results
- preserves existing incremental boundary behavior through the provider wrapper

### HIDIVE provider skeleton

New module:
- `src/mal_updater/providers/hidive.py`

Current behavior:
- declares HIDIVE capabilities based on live reconnaissance
- registers the provider slug
- intentionally raises `NotImplementedError` for fetch/write until HIDIVE implementation lands

This provides a stable target for future implementation without pretending support already exists.

## CLI changes

### New generic commands

Added:
- `provider-auth-login --provider <slug>`
- `provider-fetch-snapshot --provider <slug>`

Current behavior:
- `provider-fetch-snapshot` dispatches through the provider registry
- `provider-auth-login` currently supports only Crunchyroll and returns a clear not-yet-implemented message for other providers

### Compatibility preserved

Existing Crunchyroll commands still exist and behave the same:
- `crunchyroll-auth-login`
- `crunchyroll-fetch-snapshot`

Implementation note:
- `crunchyroll-fetch-snapshot` now delegates to the generic provider-fetch path under the hood

## What remains intentionally unchanged

These common-core areas still operate on normalized provider data and did not need a behavioral rewrite in this slice:
- `db.py`
- `ingestion.py`
- `mapping.py`
- `sync_planner.py`
- `recommendations.py`
- MAL auth/client/write flows

Some naming still reflects the original Crunchyroll-first evolution (for example a few planner/review labels), but the data model already keys everything by `provider`, which keeps the architecture transition safe.

## Why this refactor shape fits both Crunchyroll and HIDIVE

### Crunchyroll characteristics
- stateful auth bootstrap
- provider-local runtime artifacts (refresh token, device id, session state, sync boundary)
- incremental history/watchlist fetching
- transport-specific pacing and retry behavior

### HIDIVE characteristics
- bearer-token login + refresh model
- multiple useful data surfaces (history, continue-watching, favourites, future watchlists)
- likely less provider-local state than Crunchyroll, but richer token lifecycle handling

The provider boundary intentionally does **not** assume one auth style or one fetch shape.
It only requires the provider to emit a normalized snapshot contract the core understands.

## Recommended next implementation slice

1. move provider-specific status/bootstrap reporting behind provider-aware helpers
2. build smarter lane-specific daemon budgeting/cost modeling on top of the new generic source-provider defaults
3. implement HIDIVE auth/session manager and snapshot fetcher under `providers/hidive.py`
4. add richer watchlist fields (`list_id`, `list_name`, `list_kind`) to normalized ingestion/storage once HIDIVE watchlist enumeration is fully understood

## Current state

After this refactor slice:
- MAL-Updater has a real provider/core architecture spine
- Crunchyroll is now represented as a provider module instead of the only implicit source model
- HIDIVE has a registered placeholder module and confirmed recon docs
- existing test suite remains green
