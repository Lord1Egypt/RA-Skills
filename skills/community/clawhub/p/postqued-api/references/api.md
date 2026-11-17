# Postqued v2 REST API reference

Use this reference only for direct HTTP integration. Prefer the remote MCP server for agent workflows because its schemas, safety annotations, dry-run defaults, and structured outputs are machine-discoverable.

## Contents

- [Authentication and scope](#authentication-and-scope)
- [Endpoint map](#endpoint-map)
- [Upload workflow](#upload-workflow)
- [Direct publishing workflow](#direct-publishing-workflow)
- [Approval concurrency](#approval-concurrency)
- [Status and error handling](#status-and-error-handling)
- [Excluded interactive routes](#excluded-interactive-routes)

## Authentication and scope

```text
Base URL: https://api.postqued.com
OpenAPI:  https://api.postqued.com/v2/docs/openapi.json
Header:   Authorization: Bearer $POSTQUED_API_KEY
```

Use only `/v2` routes. API keys are bound to an organization. Every workspace operation requires an explicit `workspaceId` in the documented path, query, or JSON body. Organization operations require the exact bound `organizationId`.

Resolve context first:

```bash
curl --fail-with-body https://api.postqued.com/v2/mcp/context \
  -H "Authorization: Bearer $POSTQUED_API_KEY" \
  -H "Accept: application/json"
```

The response contains the machine principal and accessible organizations/workspaces. Never infer a workspace ID from a display name when multiple matches exist.

## Endpoint map

Consult the live OpenAPI document for exact request and response schemas. This map covers the customer-callable route families exposed through MCP.

### Context, workspaces, and billing

| Method | Path | Scope or purpose |
| --- | --- | --- |
| GET | `/v2/mcp/context` | API-key principal, organizations, and workspaces |
| POST | `/v2/organizations/:organizationId/workspaces` | Create a client workspace in the key's organization |
| GET | `/v2/billing/capabilities?workspaceId=...` | Read workspace capabilities |
| GET | `/v2/billing?workspaceId=...` | Read billing status |
| GET | `/v2/billing/usage?workspaceId=...` | Read current usage |

### Connected accounts and provider helpers

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/v2/integrations?workspaceId=...` | List connected accounts |
| GET | `/v2/integrations/:accountId/creator-info?workspaceId=...` | TikTok creator constraints |
| GET | `/v2/integrations/:accountId/instagram/audio?workspaceId=...` | Instagram audio choices |
| GET | `/v2/integrations/:accountId/reddit/subreddits?workspaceId=...` | Search Reddit communities |
| GET | `/v2/integrations/:accountId/reddit/restrictions?workspaceId=...` | Read subreddit restrictions |
| GET | `/v2/integrations/:accountId/linkedin/companies?workspaceId=...` | Search LinkedIn companies |
| GET | `/v2/integrations/:accountId/pinterest/boards?workspaceId=...` | List Pinterest boards |
| DELETE | `/v2/integrations/:accountId?workspaceId=...` | Disconnect an account |

### Content library

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v2/content/upload` | Create an asset and presigned upload |
| POST | `/v2/content/upload/complete` | Validate and complete an upload |
| GET | `/v2/content?workspaceId=...` | Search and paginate assets |
| GET | `/v2/content/:contentId?workspaceId=...` | Read asset metadata and URL |
| PATCH | `/v2/content/:contentId` | Update filename or alt text |
| DELETE | `/v2/content/:contentId?workspaceId=...` | Delete an asset |

The binary `/v2/content/:contentId/file` stream is not wrapped by MCP. Use the media URL returned by the metadata endpoint when appropriate.

### Calendar and publishing

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v2/publish` | Validate, publish, or schedule targets |
| GET | `/v2/publish?workspaceId=...` | List requests, optionally by complete date range |
| GET | `/v2/publish/:publishId?workspaceId=...` | Read durable request and target status |
| POST | `/v2/publish/:publishId/cancel?workspaceId=...` | Cancel pending targets in a request |
| POST | `/v2/publish/target/:targetId/cancel?workspaceId=...` | Cancel one pending target |
| PATCH | `/v2/publish/target/:targetId` | Reschedule one target |
| DELETE | `/v2/publish/:publishId?workspaceId=...` | Soft-delete a calendar request |

### Analytics and engagement

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/v2/analytics/posts?workspaceId=...&accountId=...` | Account post analytics |
| GET | `/v2/analytics/videos?workspaceId=...&accountId=...` | Paginated TikTok video analytics |
| GET | `/v2/engagement?workspaceId=...` | Read engagement inbox |
| POST | `/v2/engagement/comments/reply` | Reply to a provider comment |
| POST | `/v2/engagement/posts/comment` | Comment on a provider post |
| POST | `/v2/engagement/comments/hide` | Hide or unhide a comment |
| POST | `/v2/engagement/comments/like` | Like or unlike a comment |
| POST | `/v2/engagement/comments/delete` | Delete a comment |

### Approvals, revisions, and suggestions

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/v2/posts?workspaceId=...` | List approval posts |
| POST | `/v2/posts` | Create an approval draft |
| GET | `/v2/posts/:postId?workspaceId=...` | Read current post, revision, feedback, and delivery state |
| POST | `/v2/posts/:postId/revisions` | Create a concurrency-safe revision |
| POST | `/v2/posts/:postId/suggestions` | Suggest a caption edit |
| POST | `/v2/posts/:postId/suggestions/:suggestionId/accept` | Apply a current suggestion |
| POST | `/v2/posts/:postId/suggestions/:suggestionId/decline` | Decline a current suggestion |
| POST | `/v2/posts/:postId/comments` | Comment on the current revision |
| POST | `/v2/posts/:postId/submit` | Submit for approval |
| POST | `/v2/posts/:postId/request-changes` | Request changes |
| POST | `/v2/posts/:postId/approve` | Approve current revision |
| POST | `/v2/posts/:postId/schedule` | Schedule current approved revision |
| POST | `/v2/posts/:postId/publish` | Publish current approved revision |

### Collaboration and client review

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/v2/workspaces/:workspaceId/collaborators` | List members and pending invitations |
| POST | `/v2/workspaces/:workspaceId/invitations` | Invite a collaborator |
| POST | `/v2/workspaces/:workspaceId/invitations/:invitationId/revoke` | Revoke invitation |
| PATCH | `/v2/workspaces/:workspaceId/members/:userId` | Change role or membership type |
| DELETE | `/v2/workspaces/:workspaceId/members/:userId` | Suspend workspace access |
| GET | `/v2/posts/:postId/reviewers?workspaceId=...` | List post reviewers |
| POST | `/v2/posts/:postId/reviewer-invitations` | Invite a post reviewer |
| POST | `/v2/posts/:postId/reviewer-invitations/:invitationId/revoke` | Revoke reviewer invitation |
| DELETE | `/v2/posts/:postId/reviewers/:userId?workspaceId=...` | Remove post reviewer |
| GET | `/v2/client-reviews?workspaceId=...` | List reviews assigned to the key owner |
| GET | `/v2/client-reviews/:postId?workspaceId=...` | Read assigned review |
| POST | `/v2/client-reviews/:postId/suggestions` | Suggest a caption edit as client reviewer |
| POST | `/v2/client-reviews/:postId/comments` | Comment as assigned reviewer |
| POST | `/v2/client-reviews/:postId/request-changes` | Request client changes |
| POST | `/v2/client-reviews/:postId/approve` | Approve as client reviewer |

## Upload workflow

Start the upload:

```bash
curl --fail-with-body -X POST https://api.postqued.com/v2/content/upload \
  -H "Authorization: Bearer $POSTQUED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workspaceId": "WORKSPACE_UUID",
    "filename": "launch.mp4",
    "contentType": "video/mp4",
    "fileSize": 52428800
  }'
```

Upload bytes to the returned presigned URL using its returned method and headers. Do not attach the Postqued bearer token to that storage request. Then complete the upload:

```bash
curl --fail-with-body -X POST https://api.postqued.com/v2/content/upload/complete \
  -H "Authorization: Bearer $POSTQUED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workspaceId": "WORKSPACE_UUID",
    "contentId": "CONTENT_UUID",
    "key": "RETURNED_OBJECT_KEY",
    "filename": "launch.mp4",
    "contentType": "video/mp4",
    "size": 52428800,
    "width": 1080,
    "height": 1920,
    "durationMs": 30000
  }'
```

Supported upload MIME types are `video/mp4`, `video/webm`, `video/quicktime`, `image/jpeg`, `image/png`, `image/webp`, and `image/gif`.

## Direct publishing workflow

Validate first:

```bash
curl --fail-with-body -X POST https://api.postqued.com/v2/publish \
  -H "Authorization: Bearer $POSTQUED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workspaceId": "WORKSPACE_UUID",
    "contentIds": ["CONTENT_UUID"],
    "targets": [{
      "platform": "instagram",
      "accountId": "ACCOUNT_UUID",
      "intent": "publish",
      "caption": "Launch day.",
      "dispatchAt": "2026-08-12T09:00:00Z",
      "options": { "postType": "reel" }
    }],
    "dryRun": true
  }'
```

After confirming the validated request, repeat it with `dryRun: false` and a fresh UUID header:

```text
Idempotency-Key: 4b5c6467-95ef-49ec-af42-3a69be565bbb
```

Do not omit the idempotency key for live publishing. Reuse the same key only when retrying the exact same request body. Poll `GET /v2/publish/:publishId?workspaceId=...` until every target is terminal.

## Approval concurrency

Mutation bodies for revisions, suggestions, comments, transitions, approval, scheduling, and approved publishing carry the current concurrency values:

```json
{
  "workspaceId": "WORKSPACE_UUID",
  "expectedRevisionId": "CURRENT_REVISION_UUID",
  "expectedVersion": 4
}
```

Creating a revision uses `baseRevisionId` plus `expectedVersion`. Reread the post after a conflict and never replay stale mutation values blindly.

## Status and error handling

Publish request states include `pending`, `processing`, `completed`, `partial_failed`, `failed`, and `canceled`. Target states include `queued`, `scheduled`, `processing`, `sent`, `published`, `failed`, and `canceled`.

Errors use HTTP status plus a JSON `code` and safe message. Handle at least:

- `400`: invalid input or missing explicit machine scope
- `401`: missing, invalid, expired, or revoked credentials
- `402`: subscription or capability required
- `403`: organization, workspace, role, or provider denial
- `404`: scoped resource not found
- `409`: idempotency, workflow-state, or revision-version conflict
- `429`: rate limited; honor retry information
- `5xx`: transient server/provider failure; inspect durable state before retrying writes

## Excluded interactive routes

Do not automate these as ordinary API-key MCP calls: sign-in, API-key administration, social OAuth connection handshakes and callbacks, invitation acceptance, checkout or billing-portal redirects, inbound webhooks, API docs, and recursive Assistant chat. These require a human browser flow, provider callback, inbound transport, or separate identity transition.
