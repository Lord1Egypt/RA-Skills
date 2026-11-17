---
name: pontx-dropbox-sign
description: Integrate Dropbox Sign eSignature workflows through Pontx. Use for signature requests, templates, embedded signing, callbacks, test mode, document downloads, or HelloSign migrations.
---

# Dropbox Sign

Use this skill for eSignature workflow and safety decisions. Use Pontx for the
current Endpoint, request, Schema, credential, SDK, and CLI facts.

## Resolve the workflow first

- A non-embedded request emails signers a link to a Dropbox Sign-hosted signing
  page. Embedded signing keeps the signing experience inside your app.
- Use a template for a repeatable document with stable signer roles, fields,
  and formatting; otherwise inspect the current direct-request workflow.
- Inspect the live auth contract and choose the least-privileged credential
  path for the integration's account-ownership model.
- Distinguish a test, a production design, and an explicitly approved send. An
  integration example never authorizes sending a document.

Embedded and OAuth integrations require app approval before production, while
non-embedded integrations do not require app approval. Verify the current
account plan and approval state before changing test behavior.

## Discover through Pontx

```bash
pontx-hub search "Dropbox Sign <capability>" --type endpoint --json
pontx-hub show <returned-resource-id>
pontx-hub sdk dropbox-sign
```

Use `@pontx/dropbox-sign` for application code and `pontx-dropbox-sign` for an
explicitly requested single-product script. Hub proxying is disabled, so live
requests originate in the caller-owned SDK or CLI process.

Keep credentials in the environment or a credential manager, never in source,
arguments, logs, callback dumps, or examples. Preview every mutation locally:

```bash
pontx-dropbox-sign call <controller> <api-name> ... --dry-run
pontx-dropbox-sign call <controller> <api-name> ... --confirm '<token>'
```

Show the redacted preview and obtain explicit approval before confirming the
unchanged request. A changed document, signer, template, field, or option
requires a new preview token.

## Apply the product workflow

Test-mode signature requests are non-binding and watermarked but remain visible
to requester and signer accounts. Use controlled addresses and non-sensitive
documents, and keep test mode until production use is explicitly approved.

For templates, supplied custom-field names must match the template's merge-field
names. Handle documented success or error callbacks when creating or updating a
template. For embedded signing, generate the expiring signer URL only when the
signer is ready to open the embedded page.

## Verify callbacks before trust

Dropbox Sign callbacks normally arrive over HTTPS as `multipart/form-data` with
the event payload in the `json` field. Verify the event HMAC with the account's
API key before trusting any field, using an official helper when
available or a constant-time comparison.

Callbacks can be duplicated or arrive out of order, and signed completion is
separate from final-file readiness. Deduplicate and process idempotently, derive
state from verified events, and wait for the downloadable event before fetching
final files. After durably accepting a verified event, return HTTP 200 with
`Hello API Event Received`.

## Protect documents and signers

Inspect the live contract before choosing an upload or download representation.
Treat returned files and signing URLs as sensitive; do not print or forward
them.

Minimize retention of documents, signer emails, callback bodies, and signing
URLs. Apply the application's approved access and deletion policy.

## Few-shot workflows

### Scenario 1: One-off NDA in development

**User:** "Show a safe Node example for an NDA, but do not send it."

**Approach:** Follow the non-embedded test workflow above, inspect the live SDK
contract, use controlled non-sensitive inputs, produce a product-CLI dry run,
and stop for approval.

### Scenario 2: Repeatable onboarding agreement

**User:** "Send the same agreement weekly with different names and teams."

**Approach:** Follow the template workflow above, inspect its current contract,
preview a controlled test send, and require plan, approval, signer, document,
and retention checks before production.

### Scenario 3: Callback review

**User:** "Our handler parses JSON, trusts event_type, and downloads at
all-signed."

**Approach:** Apply the callback verification, acknowledgement, idempotency, and
final-file workflow above; keep logs redacted and perform no live download.
