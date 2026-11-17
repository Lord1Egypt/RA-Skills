# Package selection

## Default

Use `@p-acp/sdk` for most integrations. It provides role clients, session coordination, transport abstractions, workflow storage, retry, serialization, readiness checks, and orchestration.

## Lower-level packages

- `@p-acp/protocol`: lifecycle models, guarded state transitions, journals, replay, policies, and invariants.
- `@p-acp/schemas`: discovery, agreement, settlement, delivery, receipt, disclosure, JSON Schema, validation, and versioning.
- `@p-acp/privacy-adapters`: encrypted rooms, envelopes, key wrapping, grants, rotation, metadata policies, audits, and selective disclosure.
- `@p-acp/settlement-solana`: unsigned settlement intent creation, encoding, verification, RPC observation, confirmation, safety policy, wallet-flow planning, and diagnostics.
- `@p-acp/receipt-proof`: canonical receipt commitments, composition, verification, disclosure, registries, binding policies, commitment trees, and presentations.

## Environment

- Node.js 20 or newer.
- ESM modules.
- TypeScript declarations ship with the npm packages.
- Begin with `npm install @p-acp/sdk` unless the project deliberately uses only lower-level packages.
- Inspect the installed package version and repository docs instead of assuming an older API surface.

## Selection rules

- Do not install every package independently when the SDK already supplies the required surface.
- Do not use the settlement adapter merely to display payment copy.
- Do not use receipt commitments as a substitute for encrypted payload handling.
- Do not claim a hosted privacy service is required for deterministic local examples.
