---
name: "p-acp-agent-commerce"
description: "Build and review private A2A commerce workflows with P-ACP packages, privacy boundaries, Solana settlement plans, and receipt proofs."
---

# P-ACP Agent Commerce

Build and review private agent-to-agent commerce integrations with P-ACP.

## Workflow

1. Inspect the target project before editing.
   - Confirm Node.js 20 or newer.
   - Confirm ESM compatibility.
   - Read the project's package manager, TypeScript configuration, wallet integration, and test setup.
   - Identify whether the task needs a complete workflow or one lower-level P-ACP package.

2. Select the smallest suitable integration layer.
   - Start with `@p-acp/sdk` for buyer, provider, evaluator, auditor, transport, retry, and workflow orchestration.
   - Use `@p-acp/protocol` for guarded lifecycle events, journals, replay, and invariants.
   - Use `@p-acp/schemas` for exchanged records, validation, JSON Schema, and version negotiation.
   - Use `@p-acp/privacy-adapters` for encrypted agreement rooms, grants, key rotation, redaction, and selective disclosure.
   - Use `@p-acp/settlement-solana` for unsigned Solana settlement intents and external-wallet verification.
   - Use `@p-acp/receipt-proof` for receipt commitments, disclosure bundles, and verification.
   - Read [package selection](references/package-selection.md) when choosing packages.

3. Model the commerce lifecycle before writing UI code.
   - Define participants and immutable roles.
   - Define discovery, negotiation, agreement, authorization, execution, submission, acceptance or dispute, and settlement transitions.
   - Guard every transition by current state, actor role, sequence, expiry, and cause.
   - Keep retry and replay behavior deterministic.

4. Define the privacy and evidence boundary.
   - Keep requirements, negotiation messages, work orders, deliverables, evaluator notes, keys, and disclosure grants private.
   - Publish or exchange only the commitments and references required for verification.
   - Address encrypted payloads to explicit recipients.
   - Rotate or revoke grants when participant access changes.
   - Read [workflow recipes](references/workflow-recipes.md) before implementing encrypted delivery or selective disclosure.

5. Keep settlement authorization external.
   - Prepare and verify unsigned Solana settlement plans.
   - Bind session, network, mint, amount, recipient, expiry, nonce, and fee payer into the reviewed intent.
   - Hand the reviewed plan to the consuming application's selected wallet.
   - Do not load keypairs, request seed phrases, sign transactions, broadcast transactions, or claim that funds moved.
   - Read [safety boundaries](references/safety-boundaries.md) for every settlement task.

6. Produce verifiable completion evidence.
   - Commit to terms, deliverable, settlement reference, outcome, participants, session, timestamp, and protocol version.
   - Verify the receipt before presenting or disclosing selected fields.
   - Keep private content out of receipts and public logs.

7. Validate behavior.
   - Add tests for invalid roles and states, replay, expiry, wrong recipients, tampered ciphertext, commitment mismatches, revoked disclosure, and terminal finality.
   - Run the target project's typecheck, lint, build, and behavioral tests.
   - Report what is implemented, what remains external, and which network or settlement rail is actually supported.

## Output expectations

When scaffolding an integration, provide:

- selected P-ACP packages and why;
- lifecycle and participant map;
- privacy/evidence boundary;
- implementation changes;
- wallet and settlement boundary;
- tests and validation results;
- remaining provider, RPC, wallet, or hosted-service dependencies.

Use current product language: P-ACP is the Private Agent Commerce Protocol. Solana settlement is currently supported through the Solana adapter. Treat multichain support as an intended direction unless another adapter is present and verified.
