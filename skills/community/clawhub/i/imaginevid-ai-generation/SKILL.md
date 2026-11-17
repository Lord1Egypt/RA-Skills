---
name: imaginevid-ai-generation
description: Use ImagineVid's authenticated agent generation tools to create image, video, or music outputs across the current capability catalog. Use when a user asks to generate media, choose an ImagineVid model, upload a local asset, quote credits, submit a generation, or check its status.
---

# ImagineVid AI Generation

Use the capability catalog, not provider-specific APIs. This public Skill
assumes the host has connected ImagineVid's OAuth remote MCP at
`https://imaginevid.io/api/mcp`. Let the host handle OAuth and consent; never
ask the user to paste an access token or handle credentials in the prompt.
Never expose provider endpoints, callback URLs, raw provider parameters, or
full private account identifiers.

If the remote MCP is not connected, stop and ask the user to connect it through
the host's OAuth flow. Do not substitute an arbitrary API endpoint.

## About ImagineVid

[ImagineVid](https://imaginevid.io) is an AI creation platform for generating
images, videos, and music. Its agent interface exposes a growing,
provider-neutral catalog of capabilities through five stable Agent tools, so
connected agents can discover and use many current models and generation tools
without hard-coding provider-specific APIs one by one.

## Workflow

1. **Discover.** Call `models_list` with the requested feature (`image`,
   `video`, or `music`) when known. Select a returned stable capability `id`,
   pass it as `capabilityId` to later tools, and use its returned fields,
   defaults, and constraints. Do not invent a model or capability that the
   catalog did not return.
2. **Prepare owned assets.** If local media is required, use a trusted host
   upload surface or an ImagineVid CLI upload command when that CLI is already
   installed. Keep the returned owner-scoped `assetId`. Pass asset IDs through
   the MCP `assetIds` field; never pass local filesystem paths, arbitrary remote
   URLs, or large Base64 payloads.
3. **Quote.** Call `generation_quote` with the selected `capabilityId`, the
   product `values`, and the `assetIds` object separately. Keep the exact
   `prompt`, `values`, and `assetIds` request for the create step. Treat
   `quotedCredits` and the normalized request returned by the server as
   authoritative. Never calculate or choose a price locally. Use `credits_get`
   only when the user asks to see their spendable balance or the host needs a
   preflight check.
4. **Confirm.** Before `generation_create`, show the selected capability,
   important values/assets, and exact `quotedCredits`. Ask the human for
   explicit approval to spend that amount. A vague request to generate is not
   credit confirmation. If the server reports `quote_changed`, show the new
   quote and ask again.
5. **Create once.** Generate a stable `clientRequestId` before calling
   `generation_create`. Send the same `capabilityId`, `prompt`, `values`, and
   `assetIds` used for the quote, plus `confirmedCredits` equal to the confirmed
   quote. Submit exactly once for that request. Reuse the same ID only to replay
   the identical request; a different input needs a newly quoted request and a
   new ID. Never retry after a timeout, network ambiguity, or provider timeout.
6. **Poll.** Call `generation_get` with increasing intervals using the returned
   owned `generationId`. Report only the status, safe error, and result
   URLs/metadata it returned. Do not claim a model, output, or success that the
   tools did not return. Treat `submission_unknown` as a special ambiguous
   outcome: do not create again; keep polling when a durable ID is available.

## Guardrails

- `submission_unknown` means the provider may have accepted the one submission:
  do not retry and do not refund. Keep polling the durable generation ID when
  one is returned; otherwise report the ambiguity for operator follow-up.
- `insufficient_credits` stops the workflow. Do not retry, silently downgrade,
  or suggest a locally computed price.
- `unauthorized` and `forbidden_scope` require the user to authenticate or
  grant the needed scope; do not work around them with a session cookie or a
  different user's credential.
- `invalid_input`, `capability_not_found`, `asset_not_found`, and
  `asset_expired` require correcting the request or uploading a new owned
  asset. Do not substitute a provider URL.
- `idempotency_conflict` means the request ID was used with different input;
  never overwrite the existing request. Re-quote the corrected request with a
  new stable ID.
- A provider failure is not proof that a duplicate is safe. Surface the safe
  server error and wait for a new human-approved attempt.

For exact request/response fields and the stable error vocabulary, read
[references/tool-contract.md](references/tool-contract.md). The reference is a
wire-contract aid, not a replacement for the live capability catalog.
