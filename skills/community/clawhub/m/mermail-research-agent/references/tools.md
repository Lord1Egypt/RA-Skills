# Research agent tool contracts

This persona composes existing capabilities. It adds no customer, order, billing, report-storage, or entitlement API. CMC tools are external provider capabilities, not Mermail tools or additions to Mermail's catalog.

Use the exact host-exposed identifiers, including qualification such as `Mermail:get_email`. Pass `query` and `body` as native JSON objects. Do not guess tool names or call a missing tool under another namespace.

| Operation | Existing tools | Contract to read when used |
| --- | --- | --- |
| Resolve workspace/mailbox | `list_workspaces`, `list_mailboxes`, `get_mailbox`; `create_mailbox` only if authorized | [Workspace tools](../../mermail-administer-workspace/references/tools.md) |
| Select/read customer thread | `list_emails`, `search_emails`, `get_email`, `get_email_context`, `get_thread` | [Inbox tools](../../mermail-manage-inbox/references/tools.md) |
| Read selected private attachment | `download_attachment` | [Inbox security](../../mermail-manage-inbox/references/security.md) |
| Draft and reply | `save_draft`, `reply_to_email` | [Composition tools](../../mermail-compose-email/references/tools.md) |
| Purchase selected additional data | `get_paybox_connection`, `paybox_pay_x402`, `paybox_get_request`; discovery/contract tools only when available | [x402 tools](../../mermail-x402-agent/references/tools.md) and [wallet workflow](../../mermail-agent-wallet/SKILL.md) |

## Mail and attachments

- Full-profile Mermail access is needed for drafting/replies. The restricted agent-inbox profile is not a research-business execution surface. API-key mail access never unlocks PayBox.
- Prefer mailbox `public_id` as `mailboxId`. On a reply, use the exact source `emailId`; recipients remain explicit even though threading headers are set server-side.
- Draft content is the string `body.body`; send/reply content is `body.text` and/or `body.html`, with required `body.from`. Preserve source thread metadata where the live draft schema supports it. Include `source_draft_id` when sending a selected draft under the live schema.
- `get_email_context` supports bounded cursor pagination; default this workflow to eight relevant messages and 10,000 normalized characters per message, recording truncation.
- Verify exact `mailboxId`, `emailId`, and `attachmentId`, MIME type, size, and clean scan context before download. MCP binary responses are limited to 1 MiB. Report that limit; do not switch to guessed storage URLs.
- There is no general report upload or attachment-generation tool in this persona. Use available host tooling only for an explicitly requested artifact; obey the live send attachment schema and authorized data destination.

## Financial capability and failure handling

Read [x402 workflow](../../mermail-x402-agent/SKILL.md) before any purchase. On an eligible full-profile OAuth session, resolve/call `get_paybox_connection` as that workflow requires, then inspect live schemas. An omitted discovery entry alone does not prove unavailability; an actual unavailable tool is a blocker, not permission to forge a call. Only the owner can connect/reauthorize PayBox; eligible members execute through the owner's connection with their invoking identity retained for audit.

The research skill does not collect customer payments, issue invoices, check a billing provider, transfer funds, or refund orders. The owner supplies verified entitlement evidence outside email-derived claims.

Preserve structured errors (`code`, safe `details`, and `Retry-After`). A validation failure calls for correcting the exact invalid field, not broadening authority. Respect access, credit, rate, and recipient limits. On an uncertain external write, perform one bounded authoritative state check; stop dependent effects if still unresolved. Never auto-retry a send-like write or create a replacement payment.

Log only necessary order/operation IDs, report version, timestamp, safe status/error codes, and amounts. Do not create a logging service or log customer bodies, attachments, signed proofs, credentials, or raw provider responses.
