---
name: postqued-api
description: Operate Postqued through its remote MCP server or v2 REST API. Use for social content uploads, multi-platform publishing and scheduling, calendar status, analytics, engagement, approval workflows, revisions, caption suggestions, client reviews, collaborators, connected accounts, workspaces, and billing capability checks. Trigger whenever an agent needs to read or change Postqued data, publish to supported social platforms, or integrate Postqued into an automated workflow. For OpenClaw setup and more information, see https://postqued.com/openclaw.
---

# Postqued API

Use Postqued's remote MCP server for agent workflows. Use the v2 REST API only when MCP is unavailable or the caller explicitly needs HTTP integration.

## Connect

Create an organization-bound API key in the Postqued app. Store it as `POSTQUED_API_KEY`; never print, log, commit, or place it in query parameters.

Use this MCP endpoint:

```text
https://mcp.postqued.com/mcp
```

Send the key on every MCP or REST request:

```text
Authorization: Bearer $POSTQUED_API_KEY
```

Use these REST endpoints:

```text
Base URL: https://api.postqued.com
OpenAPI:  https://api.postqued.com/v2/docs/openapi.json
```

Never call legacy `/v1` routes.

## Resolve scope first

1. Call `list_workspaces` through MCP, or `GET /v2/mcp/context` through REST.
2. Select the organization and client workspace that match the user's request.
3. Ask when the intended workspace is ambiguous. Never guess between client workspaces.
4. Include the explicit `workspaceId` in every workspace operation.
5. Include the exact organization ID when creating a workspace.

API keys are bound to one organization. Cross-organization access is denied. Normal workspace roles and plan capabilities still apply.

## Choose a workflow

### Inspect or report

Use read tools freely within the selected workspace. Prefer live provider helpers before preparing platform-specific content:

- `get_creator_info` for TikTok privacy and duration constraints
- `list_instagram_audio` for selectable Instagram audio
- `search_reddit_subreddits` and `get_reddit_restrictions` for Reddit
- `search_linkedin_companies` for LinkedIn organization posting
- `list_pinterest_boards` for Pinterest destinations

Read [references/mcp-tools.md](references/mcp-tools.md) for the complete 62-tool catalog and input conventions.

### Upload content

1. Call `start_content_upload` with `workspaceId`, filename, MIME type, and known size.
2. Upload the file bytes to the returned presigned URL with the returned method and headers. Do not send the Postqued API key to the storage URL.
3. Call `complete_content_upload` with the returned `contentId` and object `key`, plus final media metadata.
4. Call `get_content` if final state or media URL is needed.

Use the same presigned upload flow for images and videos. The old multipart `/v1/content/upload-image` workflow no longer applies.

### Publish or schedule directly

1. Resolve account IDs with `list_accounts`.
2. Resolve live platform constraints with the relevant provider helper.
3. Upload media and collect `contentIds` when required.
4. Call `publish_content` with `dryRun: true` first.
5. Show the validated targets, captions, destinations, and times to the user.
6. Obtain confirmation before a real publish or schedule unless the user already explicitly approved the exact action.
7. Call `publish_content` with `dryRun: false` and a fresh UUID `idempotencyKey`.
8. Poll `get_publish_status` until the durable request and target states become terminal.

Never retry a timed-out live publish with a new idempotency key until the original request status has been checked. Read [references/platforms.md](references/platforms.md) for target schemas and platform options.

### Use approvals

Prefer the approval workflow when content requires team or client review:

1. Create a draft with `create_approval_post`.
2. Read it with `get_approval_post` before each mutation.
3. Use the latest revision ID and version for revisions, suggestions, comments, transitions, scheduling, and publishing.
4. Use `create_post_suggestion` when a reviewer should propose a caption edit without changing the revision directly.
5. Submit, request changes, or approve only after confirming the current state.
6. Schedule or publish only the current approved revision.

Treat `expectedRevisionId` and `expectedVersion` as optimistic-concurrency guards. On conflict, reread the post and reconsider the mutation; never blindly overwrite newer work.

### Manage engagement, people, or access

Read before changing provider comments, collaborators, invitations, roles, or reviewers. Obtain explicit confirmation before actions that:

- publish, reschedule, cancel, hide, delete, disconnect, revoke, or remove;
- send a comment, reply, or invitation to another person;
- approve work or request changes on someone's behalf.

Invitation acceptance, social OAuth connection, sign-in, API-key administration, checkout, and billing-portal redirects remain interactive browser flows and are intentionally not MCP tools.

## Safety rules

- Treat all provider-facing writes as externally visible.
- Default publishing to dry-run validation.
- Use one fresh UUID idempotency key per distinct live publish request.
- Preserve current revision/version values for approval mutations.
- Check `get_workspace_capabilities` before additive workspace or collaboration actions when entitlement is uncertain.
- Use `get_billing_status` and `get_billing_usage` only for read-only account context; do not attempt checkout through MCP.
- Poll durable Postqued state instead of assuming provider success from an accepted request.
- Do not expose raw access tokens, presigned URLs, API keys, or private response fields in user-facing output.
- Summarize API errors by status, code, and safe message. Do not fabricate success after a timeout or partial failure.

## References

- Read [references/mcp-tools.md](references/mcp-tools.md) when choosing tools or constructing tool inputs.
- Read [references/platforms.md](references/platforms.md) when creating publishing or approval targets.
- Read [references/api.md](references/api.md) only for direct REST integration, endpoint routing, statuses, and error handling.
