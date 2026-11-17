---
name: popcorn-temporal-anchor
description: Verify a settled payload-bound time checkpoint before a time-sensitive cross-node action. Use when a task has an execution window or when exact bytes must be checked against a signed witness interval.
---

# Verify the settled checkpoint first

Use the public STOP packet before making a network or payment call. It exercises
the complete signature, digest, time-window, and one-byte-tamper boundary with
no wallet and no private key.

## Required sample-first sequence

1. Fetch or load
   `examples/witness/evaluation-packet.production.json`.
2. Verify its ES256 signature, nonce binding, and exact 228-byte payload digest
   with `verify/typescript` or `verify/python`.
3. Compare `witness_window_utc` with `execution_window_utc` and require `STOP`.
4. Mutate byte offset 226, verify again, and require
   `witness_payload_digest_does_not_match_expected`.
5. Only if a later live task needs a fresh checkpoint should the agent consider
   `POST https://767-2676.com/v1/receipt` under participant-local payment
   policy.

From the repository root, run the full free check:

```bash
node --disable-warning=ExperimentalWarning --experimental-strip-types examples/witness/verify-settled-sample.mjs
```

Require this output and exit code 0:

```text
cryptographic_verification=valid
schedule_overlap=false
local_policy_outcome=stop
error_code=witness_payload_digest_does_not_match_expected
```

## Public inputs

- Human demonstration: `https://767-2676.com/demo`
- STOP packet: `https://raw.githubusercontent.com/violetclaire/popcorn-temporal-anchor/main/examples/witness/evaluation-packet.production.json`
- PROCEED packet: `https://raw.githubusercontent.com/violetclaire/popcorn-temporal-anchor/main/examples/witness/evaluation-packet.proceed-002.production.json`
- Expected outcomes: `https://raw.githubusercontent.com/violetclaire/popcorn-temporal-anchor/main/examples/witness/evaluation-outcomes.json`
- TypeScript verifier: `https://github.com/violetclaire/popcorn-temporal-anchor/tree/main/verify/typescript`
- Python verifier: `https://github.com/violetclaire/popcorn-temporal-anchor/tree/main/verify/python`

The STOP sample contains these fixed facts:

- task: `verify a time-bound availability inquiry`
- execution window: `2026-08-30T20:00:00.000Z` to
  `2026-08-30T20:05:00.000Z`
- witness window: `2026-08-31T05:02:06.007Z` to
  `2026-08-31T05:02:26.007Z`
- signature result: valid
- overlap: false
- local outcome: stop
- reason: `checkpoint_after_schedule_closed`

Do not rewrite these values or modify the signed packet.

## Decision boundary

Verify the signature and exact payload digest before evaluating time. Then apply
participant-local policy to the complete signed witness interval:

- If the digest does not match, stop.
- If the witness interval does not overlap the execution interval, stop.
- If uncertainty crosses a schedule boundary, recheck or stop according to
  participant-local policy.
- A valid signature or an overlapping interval never grants authorization.

POPCORN proves the fingerprint and the interval. The holder decides.

## Hard boundaries

- No authorization is granted.
- No task, schedule, identity, availability, or pricing state is stored by the
  node.
- No identity, delivery, execution, outcome, nonce uniqueness, or replay
  prevention is proven.
- Keep the exact payload and all task state in participant-local storage.
- Never fabricate or replay a payment proof.
- Never treat a valid signature as permission.

## Fresh evidence for a later live task

Only enter this section after the settled sample passes and a later live task
actually requires a new checkpoint.

1. Read `https://767-2676.com/agent/offer` and the canonical
   `https://767-2676.com/SKILL.md`.
2. Confirm the task has an `execution_window_utc` and participant-local policy
   explicitly permits the payment.
3. Hash the retained exact payload locally. Send only its SHA-256 digest, a
   fresh 32-byte nonce, and an optional predecessor-attestation digest.
4. Require the challenged resource URL to equal
   `https://767-2676.com/v1/receipt`; do not pay a redirect or copied origin.
5. Select a compatible x402 v2 requirement by scheme, network, and asset. Do
   not assume array order.
6. Verify the returned ES256 JWS, exact digest, nonce, predecessor, node, and
   signed witness interval before applying participant-local policy.

The live checkpoint costs `$0.001` USDC on Base mainnet. It is optional for a
new live task and is never required to run the public samples.
