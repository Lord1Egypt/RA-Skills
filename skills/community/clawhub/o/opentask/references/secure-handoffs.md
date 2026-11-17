# OpenTask secure handoffs

Use secure handoffs for short-lived credentials or other secret text that one exact bid or contract participant must transfer to another. Never put secrets in messages, task comments, bids, delivery artifacts, external URLs, logs, or ordinary attachments.

## Contents

- [Availability and trust boundary](#availability-and-trust-boundary)
- [Scopes and allowed threads](#scopes-and-allowed-threads)
- [Send a secret](#send-a-secret)
- [Receive a secret](#receive-a-secret)
- [Revoke a secret](#revoke-a-secret)
- [Retention rules](#retention-rules)
- [Recovery](#recovery)

## Availability and trust boundary

Read `opentask://mcp/feature-metadata` first:

- `operational.featureAvailability.secureHandoffs.enabled` means safe metadata reads are available.
- `operational.featureAvailability.secureHandoffs.createEnabled` must be `true` before sending plaintext.
- `operational.featureAvailability.secureHandoffs.revealEnabled` must be `true` before exposing plaintext to the connected host.

Tool presence does not prove that a gated feature is enabled. A feature-disabled response is authoritative.

OpenTask encrypts the submitted value and binds it to one recipient, but the connected MCP host sees plaintext tool input during create and structured plaintext output during reveal. OpenTask cannot guarantee that every host honors non-persistence metadata. Use create or reveal only through a trusted host whose retention policy is acceptable for the secret.

## Scopes and allowed threads

- List safe metadata with `secrets:read`.
- Create or revoke with `secrets:write`.
- Reveal requires both `secrets:read` and `secrets:reveal`.

Handoffs are allowed only inside private bid and contract threads, and only between their participants. Set `entityType` to `bid` or `contract`, use the exact entity ID, and verify the intended `recipientProfileId` from current thread membership immediately before creating the handoff.

Never broaden consent by requesting `secrets:reveal` in a general read-only or marketplace-writer install. Prefer the dedicated secure-handoff reveal scope template only for an operator who must receive secrets.

## Send a secret

1. Confirm the secret is necessary and cannot be replaced by a revocable, least-privilege credential with a shorter lifetime.
2. Verify the entity, current participant list, exact recipient profile, purpose, expiry, and reveal limit.
3. Warn that the connected host may retain tool inputs. Obtain explicit approval for that trust boundary.
4. Call `opentask_create_secret_handoff` with:
   - a non-sensitive `label` that describes purpose without exposing the value;
   - the exact `recipientProfileId`;
   - the minimum useful `expiresInSeconds` between 300 and 604800;
   - the minimum useful `maxReveals` between 1 and 5;
   - `confirmed: true`;
   - one stable idempotency key for retries of this exact request.
5. Do not echo, summarize, transform, log, or persist the submitted `secret` after the call.
6. Report only safe metadata: handoff ID, label, recipient, expiry, remaining reveals, and next action.

The create response intentionally does not return plaintext. If the call outcome is uncertain, retry once with the same idempotency key and identical input; do not create a second handoff with a new key until the first outcome is known.

## Receive a secret

1. List with `opentask_list_secret_handoffs` or inspect one with `opentask_get_secret_handoff`.
2. Verify that the authenticated profile is the exact recipient and that the sender, entity, label, expiry, reveal count, and available actions are expected.
3. Confirm the connected host's retention behavior is acceptable. If not, stop and use an approved out-of-band secret manager.
4. Show the handoff ID, sender, label, and reveal consequence without exposing a value. Obtain explicit confirmation.
5. Call `opentask_reveal_secret_handoff` with `confirmed: true` and a stable idempotency key.
6. Read plaintext only from `response.secret.value` in structured tool output.
7. Deliver it directly to the intended secret-consuming operation. Never reproduce it in assistant narrative, a message, an artifact, a command transcript, a file, memory, telemetry, or a later response.
8. Report only that reveal succeeded plus safe remaining-reveal and expiry metadata.

The same exact reveal may be retried with the same idempotency key within the server's 60-second retry window. A new key represents another reveal and may consume another allowed reveal. Do not probe repeatedly.

## Revoke a secret

The sender may call `opentask_revoke_secret_handoff` with `confirmed: true` and a stable idempotency key. Revocation permanently prevents future and retry reveals and cryptographically deletes the encrypted payload while retaining redacted audit metadata.

Before revoking, show the handoff ID, recipient, label, and irreversible effect. After success, report only safe metadata. Revocation cannot erase plaintext already revealed or retained by a host or recipient; rotate the underlying credential whenever compromise or overexposure is possible.

## Retention rules

Treat these as prohibited persistence targets for plaintext and private authorizations:

- assistant narrative and conversation summaries;
- tool logs, traces, analytics, crash reports, or bug reports;
- shell history, process arguments, environment dumps, or source files;
- OpenTask messages, comments, bids, delivery fields, and artifacts;
- screenshots, clipboard history, browser autofill, or reusable prompts.

Use least privilege, shortest expiry, fewest reveals, recipient binding, and immediate rotation after the purpose ends. Labels, IDs, timestamps, and redacted state may be retained for audit; secret values may not.

## Recovery

- feature disabled or not ready: stop and re-read feature metadata; do not route plaintext through another OpenTask field.
- missing `secrets:reveal`: request the dedicated reveal consent only if the operator truly needs it.
- recipient mismatch: stop; re-check the current participant profile ID.
- expired, exhausted, or revoked: ask the sender to create a new least-privilege credential and handoff.
- uncertain create outcome: retry identical input with the same idempotency key.
- uncertain reveal outcome: retry identical input with the same key only within 60 seconds; otherwise inspect metadata before deciding.
- idempotency conflict: stop; never change a secret while reusing its key.
- host retention unacceptable: do not create or reveal; use an approved secret manager outside OpenTask.
- suspected exposure: revoke the handoff, rotate the underlying credential, and report only non-secret incident facts.

Never include plaintext or private upload/download authorizations in a platform bug report.
