---
name: mnemospark-lite
description: Use this skill when OpenClaw needs to store files in mnemospark-lite, pay the x402 upload flow, complete uploads, list wallet-scoped uploads, fetch download details, mint share links, or delete uploads. This is the OpenClaw-specific skill for mnemospark-lite HTTP workflows, local wallet/runtime discovery, and reliable x402 payment handling.
---

# mnemospark Lite for OpenClaw

Use this skill to operate mnemospark-lite from OpenClaw.

**mnemospark-lite** gives any agent access to cloud storage through a simple paid HTTP workflow. Agents can upload files, list stored files, delete files, and generate shareable links that can be passed to another agent or a human. Humans can use the web app at **[https://app.mnemospark.ai/mnemospark-lite](https://app.mnemospark.ai/mnemospark-lite)** to view files, download them, delete them, and create share links from a friendly UI. It’s the same storage system, designed to work cleanly for both agents and people. Files are retained for 30 days and then automatically deleted.

## Workflow summary

Support these mnemospark-lite operations:
- upload a file and mint its share URL
- list uploads visible to the payer wallet scope
- fetch download details for a specific upload
- mint a 24-hour share URL for an existing upload
- delete one or more uploads

Use these endpoints as needed:
- `POST /api/mnemospark-lite/upload`
- `POST /api/mnemospark-lite/upload/complete`
- `GET /api/mnemospark-lite/uploads`
- `GET /api/mnemospark-lite/download/{uploadId}`
- `POST /api/mnemospark-lite/share`
- `POST /api/mnemospark-lite/delete`

## Inputs you need

Collect the minimum inputs for the requested operation.

Common inputs:
- `MNEMOSPARK_API_BASE_URL=https://api.mnemospark.ai`
- a funded x402-capable payer or existing mnemospark-compatible wallet

Upload inputs:
- file path on disk
- `tier`: one of `10mb`, `100mb`, `500mb`, `1gb`, `2gb`, `3gb`
- `contentType`
- file size in bytes

Bearer-scoped read/write inputs after upload:
- `Authorization: Bearer <token>`
- use `list_scope_bearer` from the paid upload flow when available

Entity inputs:
- `uploadId` for download/share/delete operations
- one or more `uploadId` values for delete

## OpenClaw environment hints

When running inside OpenClaw:
- if the mnemospark plugin is installed, the wallet key usually exists at `/home/ubuntu/.openclaw/mnemospark/wallet/wallet.key`
- some older or local setups may also have a legacy Blockrun wallet path, but do not assume it is the active mnemospark wallet
- for the plugin CLI, prefer an absolute invocation like `/usr/bin/node /home/ubuntu/.openclaw/extensions/mnemospark/dist/cli.js wallet`
- do not rely on `npx mnemospark` or cwd-sensitive paths when local install state may have drifted
- if you use the Python x402 client path, install the EVM extras, not only the base package: `pip install 'x402[evm]'`

## Canonical upload flow

When the user wants to upload a file, use this exact flow.

### 1) Probe the paid upload endpoint

Probe `POST ${MNEMOSPARK_API_BASE_URL}/api/mnemospark-lite/upload` without payment first when you need the x402 challenge.

Request body:

```json
{
  "filename": "example.txt",
  "contentType": "text/plain",
  "tier": "10mb",
  "size_bytes": 12
}
```

Read `PAYMENT-REQUIRED` or `x-payment-required`, base64-decode it, and preserve the advertised payment requirement.

The `402` JSON body may also include:
- `resource.url`
- `accepts`
- `extensions.bazaar`

For bazaar indexing and compatibility, preserve the advertised requirement and echo `extensions.bazaar` into the x402 `PaymentPayload` when your client supports that.

### 2) Submit the paid upload request

Retry the same `POST /upload` request with:
- `Content-Type: application/json`
- `PAYMENT-SIGNATURE: <base64-json>` or `x-payment: <base64-json>`

Prefer `PAYMENT-SIGNATURE` unless the runtime only supports `x-payment`.

Response fields can include:
- `data.uploadId`
- `data.uploadUrl`
- `data.completion_token`
- `data.list_scope_bearer`
- `data.publicUrl`
- `data.siteUrl`
- `metadata.payment.status`
- `metadata.payment.transactionHash`
- `metadata.payment.success`

### 3) Handle settlement polling correctly

The paid `POST /upload` may return:
- `200` immediately, or
- `202` with `error: settlement_pending`

If it returns `202`:
- retry the same paid request
- reuse the exact same payment payload
- do not regenerate, normalize, shrink, or rebuild the payment JSON
- poll about every 2 seconds
- use a timeout of about 60 seconds

### 4) Upload the file bytes

Send the file bytes with `PUT` to `data.uploadUrl`.

Example:

```bash
curl -T "example.txt" \
  -H "Content-Type: text/plain" \
  "<uploadUrl>"
```

### 5) Complete the upload

Call `POST ${MNEMOSPARK_API_BASE_URL}/api/mnemospark-lite/upload/complete` with only:

```json
{
  "uploadId": "<uploadId>",
  "completion_token": "<completion_token>"
}
```

Rules:
- do not send a payment header to `/upload/complete`
- send only `uploadId` and `completion_token`
- if the service returns `202`, poll every few seconds until `200` or timeout
- use a timeout of about 45–60 seconds

Successful completion should expose:
- `data.upload.publicUrl`
- `data.upload.siteUrl`
- `data.upload.status`

### 6) Verify at least one read path

After completion, verify at least one bearer-scoped read path:
- `GET /api/mnemospark-lite/uploads`
- `GET /api/mnemospark-lite/download/{uploadId}`

Use `Authorization: Bearer <list_scope_bearer>`.

This confirms the upload is visible to the payer-scoped APIs and can mint or expose a download URL.

## Critical reliability rule

When running under OpenClaw, use the x402 client-generated payload flow rather than hand-built JSON.

Use the exact payment payload generated by the x402 client library and base64-encode that JSON as-is.

Do not:
- rewrite the payload into a different version
- convert `eip155:8453` into `base`
- inject or remove fields unless you are explicitly debugging backend compatibility
- rebuild a smaller payload by hand when the x402 client already returned the full object

Use the raw x402 client payload for the paid `/upload` request, retry the same paid request on `202 settlement_pending` with the same payload, then call `/upload/complete` with only `uploadId` and `completion_token`.

Also capture these fields from the paid `/upload` response when present:
- `metadata.payment.status`
- `metadata.payment.transactionHash`
- `metadata.payment.success`

Those fields are the cleanest proof that facilitator settlement succeeded.

## Expected x402 payload shape

Successful runs used an x402-generated payload containing at least:
- `x402Version`
- `accepted`
- `resource`
- `payload.signature`
- `payload.authorization`

Example shape:

```json
{
  "x402Version": 2,
  "accepted": {
    "scheme": "exact",
    "network": "eip155:8453",
    "asset": "<asset>",
    "payTo": "<recipient>",
    "amount": "<amount>",
    "maxTimeoutSeconds": 3600,
    "extra": {
      "name": "USD Coin",
      "version": "2"
    }
  },
  "resource": {
    "url": "https://api.mnemospark.ai/api/mnemospark-lite/upload",
    "mimeType": "application/json",
    "description": "mnemospark-lite upload"
  },
  "payload": {
    "signature": "<eip3009-signature>",
    "authorization": {
      "from": "<payer-wallet>",
      "to": "<recipient>",
      "value": "<amount>",
      "validAfter": "<unix-seconds>",
      "validBefore": "<unix-seconds>",
      "nonce": "<bytes32>"
    }
  }
}
```

Treat later backend normalization or enrichment as a server concern, not a reason to mutate the client payload.

## List uploads

When the user wants to see uploads for the payer scope, call:
- `GET ${MNEMOSPARK_API_BASE_URL}/api/mnemospark-lite/uploads`
- `Authorization: Bearer <token>`

You typically receive the token as `list_scope_bearer` from the paid upload flow.

Expect `data.uploads[]` fields such as:
- `id`
- `filename`
- `contentType`
- `tier`
- `maxSize`
- `actualSize`
- `publicUrl`
- `status`
- `pricePaid`
- `expiresAt`
- `createdAt`

Notes:
- bearer scope is tied to the payer wallet
- `publicUrl` may be `null` until `/upload/complete`
- treat bearer tokens as credentials and store them appropriately for the runtime

## Download an upload

When the user wants download detail or a short-lived download URL, call:
- `GET ${MNEMOSPARK_API_BASE_URL}/api/mnemospark-lite/download/<uploadId>`
- `Authorization: Bearer <token>`

Expect:
- `data.upload`
- `data.upload.downloadUrl` when the upload is in a downloadable state

Notes:
- bearer access is wallet-scoped
- download URLs are short-lived presigned URLs
- do not assume the download URL is permanent

## Mint a share URL

When the user wants a 24-hour share link for an existing upload, call:
- `POST ${MNEMOSPARK_API_BASE_URL}/api/mnemospark-lite/share`
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

Body:

```json
{
  "uploadId": "<uploadId>"
}
```

Expect:
- `data.shareUrl`
- `data.expiresAt`

Notes:
- bearer access is wallet-scoped to the same payer scope as list/download
- the share URL is anonymous and expires after 24 hours
- recipients use the app flow to exchange the token for a short-lived download URL

## Delete uploads

When the user wants to delete one or more uploads, call:
- `POST ${MNEMOSPARK_API_BASE_URL}/api/mnemospark-lite/delete`
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

Body:

```json
{
  "uploadIds": ["<uploadId1>", "<uploadId2>"]
}
```

Expect:
- `data.deleted`
- `data.results[]` per upload ID

Notes:
- deletes are wallet-scoped
- process each result independently
- re-run `GET /uploads` to confirm removals

## Output expectations

Return or persist the most useful fields for the active task:
- `uploadId`
- `publicUrl`
- `siteUrl`
- `shareUrl` when minted separately
- `list_scope_bearer`
- `metadata.payment.status` when present
- `metadata.payment.transactionHash` when present
- `metadata.payment.success` when present  
