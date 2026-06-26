# mx-auto Learning Guide

Use this guide only for complex requests that combine trigger, sandbox, or script operations.

## Routing

- Trigger list/run requests: read `references/triggers.md`.
- Existing browser sandbox tab/snapshot requests: read `references/sandbox.md`.
- Local script list/show/run requests: read `references/scripts.md`.

## Shared Rules

- Prefer auto-discovery before asking for Runtime URL, app home, or token.
- Store app home and other non-secret defaults only.
- Never store, print, or copy the Runtime admin token value.
- Use exact names for execution targets; do not fuzzy-match a trigger or script when running it.
- Ask only after Runtime discovery or target resolution fails.

## Failure Framing

Clearly distinguish:

- Runtime unavailable
- Runtime unauthorized or token file missing
- target resolution/cache miss
- command execution failure
- sandbox no-match or multiple-match disambiguation
