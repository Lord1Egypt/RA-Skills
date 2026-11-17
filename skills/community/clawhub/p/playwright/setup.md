# Setup — Loading Preferences

Read this on first use. Do not interview the user.

## Your Attitude

Playwright fails loudly and precisely; almost every error names its own cause. Read the first line of the failure, get the trace, and fix the actual condition instead of widening timeouts. Ship automation someone else can debug at 2am.

## How To Load Preferences

1. Read `~/Clawic/data/playwright/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `language: typescript`, `runner_mode: test`, `default_browsers: [chromium]`, `headed_by_default: false`, `test_id_attribute: data-testid`, `ci_provider: github`, `scrape_delay_ms: 1000`.
3. Read `~/Clawic/data/playwright/memory.md` for prior context. Absence is fine; proceed without comment.
4. Read the repository before writing anything: `playwright.config.*`, existing specs, fixtures, `.auth/` patterns, and the package manager lockfile. **The repo's conventions outrank both defaults and stored preferences** — a stored `language: typescript` does not justify adding TypeScript to a JavaScript suite.

Work from defaults immediately. Never open with questions about setup, priorities, or how proactive to be.

## Recording Preferences (only when the user declares one)

- User names a language, browser set, test-ID attribute, CI provider, or a preferred path (suite vs script vs MCP) → update the matching key in `~/Clawic/data/playwright/config.yaml`.
- User states a stance (retry policy, whether staging URLs may be automated, reporter set, page-object style) → record it under the relevant preference area in `~/Clawic/data/playwright/memory.md`.
- User corrects earlier guidance → overwrite the stored value so the correction is not repeated.

If the user has said nothing, store nothing. An observation never overwrites a declared preference without confirmation.

## What Never Goes In The Preferences Folder

Credentials, `storageState` files, tokens, traces, videos, reports, and snapshots. Those belong to the repository (gitignored where sensitive) or the system temp dir. `~/Clawic/data/playwright/` holds preferences and observations only.

## Memory Format

Create `~/Clawic/data/playwright/memory.md` with this structure:

```markdown
# Playwright Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Context
<!-- Their stack, app under test, how the suite is run (local, CI provider, sharding) -->

## Pain Points
<!-- Recurring failures: flaky areas, slow suites, auth complexity -->

## Preferences
<!-- Conventions observed in their repo; how much explanation they want -->

---
*Updated: YYYY-MM-DD*
```

| Status | Meaning |
|---|---|
| `ongoing` | Still learning their suite and environment |
| `complete` | Their conventions and pain points are known |
