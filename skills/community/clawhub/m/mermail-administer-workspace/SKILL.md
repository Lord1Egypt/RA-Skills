---
name: mermail-administer-workspace
description: Inspect Mermail AI, API, and email usage and manage workspaces, members, invitations, email domains, mailboxes, webhooks, and storage. Use for workspace administration, access changes, domain verification, mailbox provisioning or settings, webhook subscriptions and deliveries, storage checks, plan usage, RPM, or credits. Do not use for generic inbox work, composing mail, or third-party app execution.
metadata:
  openclaw:
    requires:
      env:
        - MERMAIL_API_KEY
    primaryEnv: MERMAIL_API_KEY
    homepage: https://docs.mermail.app/ai/skills
    emoji: "🏢"
---

# Mermail Workspace Administration

## Overview

Use this skill to turn authenticated Mermail workspace state into clear usage reports and safe administrative changes. Ground every decision in exact workspace, member, domain, mailbox, webhook, plan, usage, and storage evidence, and preserve the credential-bound workspace boundary.

Read [tools.md](references/tools.md) for the owned MCP tools and approval requirements. Read [ai-credits.md](references/ai-credits.md) for AI usage, reservations, and failure handling.
Read [webhooks.md](references/webhooks.md) before creating, changing, testing, retrying, deleting, or rotating a webhook.

## Preferred Deliverables

- Workspace usage summaries with current AI and API credits, email usage, storage, and relevant limits.
- Exact member, invitation, role, domain, mailbox, or settings change proposals showing current and intended state.
- Domain verification summaries with current status and the smallest safe next action.
- Mailbox provisioning results stating whether an existing mailbox was reused or one new mailbox was created for 10 provision credits.
- Webhook subscription and delivery reports that identify the exact workspace, webhook, selected event set, destination host, delivery state, and secret-rotation impact without revealing write-only values.
- Final verification reports that distinguish completed, pending, partially failed, blocked, and unverified changes.

## Workflow

1. Resolve the credential-bound workspace and the exact member, invitation, domain, or mailbox before reasoning about a change. Use stable IDs returned by list/get tools; never invent an ID or cross into another workspace.
2. Read and show the relevant current state first. Use `get_ai_credit_usage`, `list_ai_credit_events`, `get_api_credit_usage`, `get_email_usage`, or storage reads before a large or costly workflow when usage is material. Keep AI credits separate from API and mailbox provision credits.
3. Resolve ambiguity before writing. When multiple similarly named workspaces, members, domains, or mailboxes remain, present the smallest non-secret distinguishing metadata and ask the user to choose.
4. Always call `list_mailboxes` or `list_workspace_mailboxes` before `create_mailbox`. Reuse a suitable exact mailbox instead of provisioning a duplicate, and do not retry an uncertain create blindly.
5. Validate requested roles, invite recipients, domain names, mailbox addresses, and settings against the current live schema. `create_mailbox` requires `email` and `name` and costs 10 provision credits. For credential-bound MCP, `workspaceId` is optional when the live schema permits omission; pass the exact resolved workspace ID only when the transport or schema requires it.
6. Check role and plan prerequisites before proposing a write. Only an authorized workspace admin may call `update_mailbox_settings`, including changes to `settings.agentAutoResponse.mode`; `draft_for_review` and `automatic_triage` are mailbox response modes, not task-triager defaults. Never replace unrelated settings with a partial example. Do not bypass Developer-plan requirements for email-domain operations or imply that the skill elevates the authenticated credential's permissions.
7. Preview the exact access, routing, ownership, domain, mailbox, or usage impact before a write. For invitations and resends, identify the exact recipient and workspace and obtain approval before creating the external effect.
8. For webhook work, resolve the exact workspace and webhook with `list_webhooks`, `get_webhook`, and `list_webhook_deliveries`. Use `create_webhook`, `test_webhook`, `retry_webhook_delivery`, and `rotate_webhook_secret` only for their exact requested effects. A destination receives selected email content, so preview the destination host and exact event set. Treat destination URLs and Authorization values as write-only. A signing secret appears only once on creation or rotation; keep it in the secure result surface and never repeat it in chat or logs.
9. For `remove_workspace_member`, `delete_email_domain`, or any webhook create/update/delete/test/retry/secret rotation, obtain explicit approval, call `prepare_destructive_action` with the exact tool name and arguments, then execute once with the returned single-use token. For create, test, and delivery retry, preserve the same `idempotencyKey` and unchanged arguments after an uncertain response; read state before considering any new action.
10. Re-read the affected resource when a read endpoint exists. For webhook delivery work, inspect `list_webhook_deliveries` using the original webhook and delivery IDs. Report the tool result as unverified when no independent read is available; never infer success from narrative text or an uncertain response.

## Write Safety

- Preserve workspace boundaries, existing access, routing, domain configuration, and mailbox settings unless the user explicitly asks to change them.
- Treat role changes, invitations, domain changes, mailbox provisioning, and settings updates as writes. Show the exact target and intended effect before acting when the user's request is not already explicit.
- Treat member removal, domain deletion, and webhook create/update/delete/test/retry/secret rotation as destructive. Require fresh exact approval and a matching single-use `prepare_destructive_action` token.
- Never send a test event, retry a delivery, or rotate a signing secret merely to check status. Use the webhook and delivery reads. After a timeout or unknown result, reuse the original idempotency key only for the exact same create/test/retry request and do not broaden its destination, event set, or payload.
- Do not expose full webhook destination URLs, Authorization values, signing secrets, or selected email content in summaries. Secret rotation invalidates the previous secret; state that operational impact before approval.
- Do not call or invent `delete_workspace`; the current MCP catalog does not expose it.
- Do not infer ownership transfer, silently change another member's role, expose credentials or DNS secrets, or convert an ambiguous name into an administrative target.
- Make one authorized mailbox provision after discovery. On conflict, re-list and reuse only an exact suitable concurrent match; do not loop through write retries.
- Stop on authorization, plan, credit, or rate-limit failures such as `401`, `402`, `403`, or `429`. Explain the actionable cause without exposing secrets or bypassing the restriction.
- On `ai_credits_exhausted` or `ai_credit_accounting_unavailable`, stop new generation/automation and surface the returned renewal or recovery state. `ai_action_in_progress` and unknown outcomes must be reconciled using the original request identity, never replaced with another generation or send.
- Respect the live schema and authenticated role over examples in this skill. A skill guides tool use; it never grants workspace or Developer-plan permissions.

## Output Conventions

- Identify the workspace and affected resource with stable IDs plus the smallest useful human-readable label.
- Present usage with exact values, units, limits, and measurement windows returned by Mermail; do not estimate missing data.
- For proposed changes, show a concise current → intended diff and state whether approval is still required.
- For invitations, report the exact recipient and status without exposing tokens or private delivery metadata.
- For domains, report the normalized domain, verification state, plan restriction, and next safe action without exposing DNS secrets.
- For mailbox creation, report normalized email, stable `public_id`, reused or provisioned state, and the 10-credit cost when creation occurred.
- For webhooks, report the stable webhook/delivery IDs, destination host only, event set, enabled state, attempt status, and timestamps. State whether a create or rotation returned a new secret without echoing it.
- Distinguish `completed`, `pending`, `partial_failure`, `blocked`, and `unverified`; include the exact remaining action for non-terminal states.

## Example Requests

- "Show this workspace's API credits, email usage, and storage."
- "Show AI credits used, reserved, remaining, and their renewal time."
- "As a workspace admin, switch this support inbox from Draft for review to Automatic triage after previewing its current settings."
- "Invite alex@example.com to this workspace as a member."
- "Change this member from viewer to admin after showing me the impact."
- "Add and verify example.com as an email domain."
- "Create support-eu@mermail.app only if an exact usable mailbox does not already exist."
- "List failed webhook deliveries for this workspace without retrying them."
- "Create an email webhook for the selected events after showing the exact destination and approval boundary."
- "Rotate this webhook signing secret once and tell me which integration must be updated."
- "Remove the selected member from this workspace."
