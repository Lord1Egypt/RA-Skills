# Local Workflow Conventions

These conventions are useful for disciplined Stitch work, but they are not native Stitch capabilities. Treat them as optional local workflow layers.

## Screen aliases

Use human-readable identifiers for screens when the project grows beyond a few artifacts.

Benefits:

- easier collaboration
- easier revision tracking
- lower dependence on opaque screen IDs

Rules:

- keep alias names short and stable
- use one alias per design concept or screen family
- keep the alias attached to the latest accepted iteration
- use aliases only as local labels, never as a substitute for actual Stitch identifiers

## Execution artifacts

Store local outputs for each operation in a dedicated run directory.

Recommended contents:

- prompt used
- project and screen identifiers
- downloaded HTML if available
- downloaded preview image if available
- timestamp
- short operator note such as `accepted`, `rejected`, or `candidate`

## Operation history

Maintain a chronological local log of design operations and alias changes.

This is useful for:

- traceability
- recovery
- auditability of screen evolution

## Screen derivation history

Track parent-child relationships between generated, edited, and variant-derived screens.

Include:

- parent screen ID when one screen is derived from another
- whether the step was generate, edit, or variants
- a one-line intent note such as `tighten hierarchy` or `mobile cleanup`

## Last-active-screen state

Keep a small local state file that records the latest project and screen used.

Use it to reduce needless ID lookup, but never let it override explicit user intent.
