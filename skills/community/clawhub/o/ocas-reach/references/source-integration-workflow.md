# Source Integration Workflow

Use this when <operator> provides a new candidate source for Reach.

## Default stance

When <operator> gives a new source for `ocas-reach`, integrate it into the runtime registry unless there is a hard blocker. Discovery-only cataloging is insufficient.

## Required workflow

1. Evaluate the source quickly against Reach criteria: authority, structured access, auth, rate limits, license/terms, citation path, and query shape.
2. If no hard blocker exists, add a runtime source entry in `scripts/sources.yml`.
3. Use a generic source entry when simple REST action templates are enough.
4. Write a custom connector under `scripts/sources/<slug>.py` when the source needs parsing, static dataset access, response hydration, source-directory extraction, snapshots, or other non-trivial logic.
5. Add `references/sources/<slug>.md` with actions, params, terms, citation rules, and gotchas.
6. Update `references/sources/index.md` in the appropriate auth/routing section.
7. Validate by running `python scripts/reach.py sources`, `python -m py_compile` on changed connector files, and at least one representative `python scripts/reach.py query <slug> <action> ...` call.
8. If the source has a hard blocker, still register it when useful so Reach fails explicitly. Example: auth-required APIs should declare `auth: required`, `env_var`, and `account_url` rather than remaining only in discovered notes.

## Hard blockers

A hard blocker is something that prevents runtime use despite normal agent effort, such as:

- Required credentials or API key not yet provisioned.
- Paid account or terms acceptance requiring <operator>'s decision.
- Legal/terms restriction incompatible with Reach use.
- No stable machine-readable access after verification.

## Do not stop at discovery

`references/discovered-apis.md` is not the endpoint when <operator> explicitly supplies a source. Use it only as background or for sources that fail integration criteria. The expected final state is a registered source or an explicit hard-blocker registration/error path.

## Pattern examples from July 2026

- `metmuseum`: live REST API, no auth → custom connector + registry + source reference + live query validation.
- `dahd_open_data`: source-directory page, WordPress JSON endpoint usable despite public page redirect → custom parser connector, not object-level factual source.
- `walters_art`: API v1 closed, but static CSV files available → custom static-dataset connector rather than REST.
- `harvard_art_museums`: key required → registered with `auth: required`, `env_var`, and `account_url`; runtime query fails explicitly until key exists.
