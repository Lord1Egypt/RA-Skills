# Workspace administration tool map

## Usage and discovery

- `get_ai_credit_usage`, `list_ai_credit_events`, `get_api_credit_usage`, `get_email_usage` — AI credit allowance, charged/reserved/remaining amounts, mode, renewal, and bounded event history are separate from API and provision credits. See [ai-credits.md](ai-credits.md).
- `list_workspaces`, `get_workspace`, `get_workspace_storage`
- `list_workspace_members`, `list_email_domains`
- `list_workspace_mailboxes`, `list_mailboxes`, `get_mailbox`, `get_mailbox_storage`
- `list_webhooks`, `get_webhook`, `list_webhook_deliveries` — workspace-admin reads for subscriptions and delivery attempts. Keep destination URLs, Authorization values, signing secrets, and selected email content out of summaries.

## Administrative writes

- `update_workspace`, `update_member_role`
- `invite_workspace_member`, `resend_workspace_invite` — require an exact-recipient preview and approval
- `add_email_domain`, `verify_email_domain` — require Developer-plan access
- `create_mailbox` — list first; `body` requires `email` and `name`, while `workspaceId` is optional for credential-bound MCP when the live schema permits omission. Pass the exact resolved workspace ID when CLI, REST, or another live transport requires it. Make one explicitly authorized provision with no blind write retry.
- `update_mailbox_settings` — mailbox-admin only. For email response behavior, inspect existing settings and modify only the intended `settings.agentAutoResponse.mode` (`draft_for_review` or `automatic_triage`), preserving the remaining policy and mailbox settings. Use the live input schema and verify with `get_mailbox`; this is separate from `set_default_task_triager`.
- `create_webhook`, `update_webhook` — workspace-admin only. The destination receives selected email content. Preview the destination host and exact events; destination URLs and Authorization values are write-only. `create_webhook` returns a signing secret only once and requires a stable `idempotencyKey`.
- `test_webhook`, `retry_webhook_delivery` — workspace-admin external effects. Use one exact webhook/delivery target. Preserve the same `idempotencyKey` and arguments after an uncertain response instead of generating a second delivery.
- `rotate_webhook_secret` — workspace-admin secret rotation. The replacement secret is returned only once and invalidates the prior secret; disclose this impact before execution without copying either secret into chat.

## Destructive

- `remove_workspace_member`, `delete_email_domain`, `create_webhook`, `update_webhook`, `delete_webhook`, `test_webhook`, `retry_webhook_delivery`, `rotate_webhook_secret`

Require explicit approval and a single-use token from `prepare_destructive_action`. The current MCP catalog does not expose `delete_workspace`; do not invent or call that removed tool.
