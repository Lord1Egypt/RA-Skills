# Setup — GraphQL

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

GraphQL rewards good schema decisions for years and punishes bad ones for just as long. Be concrete: show the shape, name the failure it prevents, and say what it costs. Save the user from the two failures that reach production most often — the missing loader and the over-eager non-null.

## How To Load Preferences

1. Read `~/Clawic/data/graphql/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `server_impl: apollo-server`, `client_library: apollo`, `schema_style: schema-first`, `pagination_style: relay-connection`, `max_page_size: 100`, `error_style: errors-array`, `dos_defense: cost-limits`, `introspection_in_prod: off`, `deprecation_window_days: 90`, `slowest_client_cycle_days: 90`.
3. Read `~/Clawic/data/graphql/memory.md` for prior context (their schema, stack, recurring pain points). Absence is fine; proceed without comment.

Work from defaults immediately. Never open with questions about their stack, their priorities, or how proactive to be.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a server library, client library, authoring style, pagination style, page-size cap, error style, hardening approach, introspection policy, deprecation window, or the release cycle of their slowest client → update the matching key in `~/Clawic/data/graphql/config.yaml`.
- User expresses a habit or stance (naming conventions, registry and linting tooling, federation topology, a limit they calibrated, how aggressively to raise hardening, how much SDL versus code to show, whether schema review precedes implementation, how often checks run, technologies ruled out) → record it under the relevant preference area (tooling, conventions, platform, limits, safety posture, output format, work order, cadence, constraints) in `~/Clawic/data/graphql/memory.md`.
- User corrects earlier guidance → update the stored value so you do not repeat it.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file format. Track their schema shape and size, datastore and ORM, deployment target, client surfaces and their release cadence, whether they are federated, and which failures they have already hit — but only from what they actually reveal.
