# Postqued MCP tool catalog

The remote server exposes 62 structured tools at `https://mcp.postqued.com/mcp`. Let the MCP client discover each tool's current input schema; use this catalog to choose the right operation and apply workflow safety.

## Contents

- [Shared conventions](#shared-conventions)
- [Workspaces and account context](#workspaces-and-account-context)
- [Connected accounts](#connected-accounts)
- [Content library](#content-library)
- [Calendar and publishing](#calendar-and-publishing)
- [Analytics](#analytics)
- [Engagement](#engagement)
- [Approvals and revisions](#approvals-and-revisions)
- [Collaboration and client review](#collaboration-and-client-review)

## Shared conventions

- Call `list_workspaces` first and pass the selected UUID as `workspaceId` to every scoped tool.
- IDs for accounts, content, posts, revisions, suggestions, invitations, publish requests, and publish targets are UUIDs unless the tool schema says otherwise.
- Use offset-bearing ISO 8601 timestamps, such as `2026-08-12T09:00:00Z`.
- Tool output is structured JSON under `result` and also includes a concise text representation.
- Read tools are non-mutating. Provider reads can contact external social networks.
- Write tools change Postqued state. Provider writes can create externally visible effects.
- Destructive tools can publish, cancel, hide, delete, disconnect, revoke, remove, approve, or otherwise replace state.

## Workspaces and account context

| Tool | Use |
| --- | --- |
| `list_workspaces` | Resolve the API-key principal, organization, and accessible client workspaces |
| `create_workspace` | Create a client workspace in the exact bound organization |
| `get_workspace_capabilities` | Check feature access before additive workspace/collaboration actions |
| `get_billing_status` | Read the workspace's billing state without changing it |
| `get_billing_usage` | Read current usage without changing billing |

`create_workspace` requires `organizationId` and `name`. Do not create a workspace when the user's intended organization or client name is ambiguous.

## Connected accounts

| Tool | Use |
| --- | --- |
| `list_accounts` | Resolve connected account IDs, platform, profile, and state |
| `get_creator_info` | Read live TikTok privacy choices, permissions, and duration constraints |
| `list_instagram_audio` | List selectable Instagram music or original sound |
| `search_reddit_subreddits` | Search communities available to the Reddit account |
| `get_reddit_restrictions` | Read live subreddit post types, flair, and restrictions |
| `search_linkedin_companies` | Search LinkedIn organizations available for publishing |
| `list_pinterest_boards` | List writable Pinterest boards |
| `disconnect_account` | Disconnect the account and revoke stored Postqued credentials |

Call provider helpers immediately before preparing or validating a platform-specific target. Confirm before `disconnect_account`.

## Content library

| Tool | Use |
| --- | --- |
| `start_content_upload` | Create an asset and get a presigned PUT URL |
| `complete_content_upload` | Validate and finalize uploaded bytes |
| `list_content` | Search and paginate ready workspace images/videos |
| `get_content` | Read one asset's metadata and media URL |
| `update_content` | Change filename or accessibility alt text |
| `delete_content` | Delete an asset |

Upload MIME types: `video/mp4`, `video/webm`, `video/quicktime`, `image/jpeg`, `image/png`, `image/webp`, `image/gif`.

`start_content_upload` returns a storage URL, method, headers, object key, and `contentId`. Upload the raw bytes to that URL without the Postqued bearer token, then pass the returned identifiers to `complete_content_upload`.

## Calendar and publishing

| Tool | Use |
| --- | --- |
| `publish_content` | Dry-run validation, immediate publishing, or scheduling for up to ten targets |
| `list_publish_requests` | List calendar activity, optionally within a complete start/end range |
| `get_publish_status` | Read durable request and per-target status |
| `cancel_publish` | Cancel all still-pending targets in a request |
| `cancel_publish_target` | Cancel one pending or scheduled target |
| `reschedule_publish_target` | Set a new dispatch time; `null` moves to immediate dispatch |
| `delete_publish_request` | Soft-delete a request from the workspace calendar |

`publish_content` accepts `workspaceId`, zero to 35 `contentIds`, one to ten platform-discriminated `targets`, `dryRun`, and `idempotencyKey`.

Always start with `dryRun: true`. A live call requires `dryRun: false` and a fresh UUID `idempotencyKey`. Read [platforms.md](platforms.md) for target options. Confirm before live publishing, scheduling, canceling, rescheduling, or deleting.

When filtering `list_publish_requests`, provide both `startDate` and `endDate` or neither.

## Analytics

| Tool | Use |
| --- | --- |
| `get_account_analytics` | Read post metrics for TikTok, Facebook, Instagram, Threads, or YouTube over 7, 30, or 90 days |
| `get_tiktok_videos` | Read paginated TikTok video metrics for week, month, or all time |

Resolve the connected `accountId` first. Treat provider analytics as point-in-time data and state the requested range in summaries.

## Engagement

| Tool | Use |
| --- | --- |
| `list_engagement` | Read recent provider comments in the workspace inbox |
| `reply_to_comment` | Reply through a connected account |
| `comment_on_post` | Add a new provider comment |
| `set_comment_hidden` | Hide or unhide a provider comment |
| `set_comment_liked` | Like or unlike a provider comment |
| `delete_comment` | Delete a provider comment where supported |

Read the inbox first. Confirm exact message text and destination before sending replies/comments. Confirm moderation and deletion actions.

## Approvals and revisions

| Tool | Use |
| --- | --- |
| `list_approval_posts` | List workspace posts and approval states |
| `create_approval_post` | Create a draft with assets and platform targets |
| `get_approval_post` | Read current revision, feedback, reviewers, and delivery state |
| `create_post_revision` | Create a revision from the current base revision/version |
| `create_post_suggestion` | Propose a selection-bound caption replacement |
| `accept_post_suggestion` | Apply a suggestion against the current revision/version |
| `decline_post_suggestion` | Decline a suggestion against the current revision/version |
| `comment_on_approval` | Add revision-bound approval feedback |
| `submit_for_approval` | Move the current revision into review |
| `request_post_changes` | Request changes with a required comment |
| `approve_post` | Approve the current revision |
| `schedule_approved_post` | Schedule the current approved revision |
| `publish_approved_post` | Publish the current approved revision immediately |

Draft/revision fields are `title`, optional `brief`, up to 35 `assetIds`, and up to 35 platform targets. Revision creation also requires `baseRevisionId` and `expectedVersion`.

Suggestions specify the current revision/version, target index, platform, `caption` field, selection offsets, original text, replacement text, and optional note.

All approval mutations use the latest `expectedRevisionId` and `expectedVersion`. Reread after conflicts. Confirm submission, change requests, approval, scheduling, and publishing.

## Collaboration and client review

| Tool | Use |
| --- | --- |
| `list_collaborators` | List active members and pending invitations |
| `invite_collaborator` | Invite an email with role and membership type |
| `revoke_collaborator_invitation` | Revoke a pending workspace invitation |
| `update_collaborator` | Change a collaborator role or membership type |
| `remove_collaborator` | Suspend workspace access |
| `list_post_reviewers` | List reviewers/invitations for one post |
| `invite_post_reviewer` | Invite client-review access for one post |
| `revoke_post_reviewer_invitation` | Revoke a pending reviewer invitation |
| `remove_post_reviewer` | Remove one post reviewer's access |
| `list_client_reviews` | List reviews assigned to the API-key owner |
| `get_client_review` | Read an assigned review and current concurrency state |
| `create_client_suggestion` | Propose a selection-bound caption replacement as reviewer |
| `comment_on_client_review` | Add assigned-review feedback; comment required |
| `request_client_changes` | Request changes as assigned reviewer; comment required |
| `approve_client_review` | Approve the assigned current revision |

Collaborator roles are `admin`, `editor`, `reviewer`, or `viewer`; membership type is `team` or `external`. Check workspace capabilities before additive collaboration actions. Confirm invitation emails, access changes, removals, client change requests, and approvals.
