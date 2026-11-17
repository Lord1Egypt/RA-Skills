# Workflow recipes

## Private buyer-provider workflow

1. Register immutable buyer, provider, optional evaluator, and auditor identities.
2. Create a session with expiry and deterministic identifiers.
3. Seal the proposal for the provider and journal its commitment.
4. Record agreement terms and evaluator requirements.
5. Authorize an externally reviewed settlement intent.
6. Confirm only an observed settlement reference.
7. Start execution and seal the deliverable for the buyer.
8. Accept or dispute through the authorized role.
9. Compose, verify, and publish the receipt commitment.
10. Settle or refund through the application's external wallet and RPC boundary.

## Encrypted agreement room

- Grant room access only to named participants.
- Address each envelope to its intended recipient.
- Rotate keys when membership changes.
- Revoke grants explicitly.
- Keep ciphertext, keys, and private metadata out of public journals.
- Use selective disclosure for approved fields instead of revealing the full payload.

## Receipt presentation

- Commit to terms, deliverable, settlement reference, outcome, participant identities, session, timestamp, and protocol version.
- Verify the complete commitment bundle first.
- Construct a presentation that reveals only approved fields and proofs.
- Reject mismatched domains, salts, bindings, or receipt digests.

## Existing integration review

Check:

- role-to-operation authorization;
- state-transition guards;
- idempotency and replay handling;
- expiry and nonce handling;
- recipient and network binding;
- encrypted payload addressing;
- grant revocation;
- receipt verification;
- separation between observed settlement and claimed funds movement.
