---
name: manage-post-queue
description: Review, edit, publish, reschedule, cancel or troubleshoot posts in Auto Poster AI. Use when the user asks what is scheduled, wants to change or delete a post, approve a draft, check if a post went live, or find out why a post failed.
---

# Manage the post queue

Uses `autoposter_list_posts`, `autoposter_get_post`, `autoposter_get_post_status`, `autoposter_update_post`, `autoposter_publish_draft` and `autoposter_delete_post`.

## Tasks

- **What is coming up:** `autoposter_list_posts` with `state: "scheduled"`, or `drafts`, `queued`, `pending_approval`, `posted`, `failed`. Use `search` for a caption keyword. Show a short table: ID, platform, text start, time, state.
- **Did it publish:** `autoposter_get_post_status`. When posted it returns live links. Give the user the link.
- **Edit or reschedule:** `autoposter_update_post` with only the fields that change (`content`, `scheduledAt` + `timezone`, `mediaIds`, `firstComment`, `threadComments`, `title`, `visibility`). Previous values are overwritten and cannot be undone, so show the old and new text and confirm first. Posts already published or in processing cannot be edited. If the API key cannot publish directly, an edited scheduled post goes back to `pending_approval`.
- **Publish a draft now:** show the exact text and accounts, get a yes, then `autoposter_publish_draft`. Needs a key with direct publish permission; if it is refused, tell the user an approver must approve it.
- **Cancel or delete:** `autoposter_delete_post`. Name the post and ask for confirmation first, one post at a time. Never bulk delete from a vague request like "clear the queue".

## Failed posts

1. `autoposter_get_post_status` for the error.
2. Check it against `autoposter_get_rules` (too long, wrong media format, missing video for a reel).
3. Fix with `autoposter_update_post`, or recreate with `schedule-social-posts` if the post cannot be edited.
4. If the error points to a disconnected account, tell the user to reconnect it in Auto Poster AI. You cannot do that.

## Rules

- Always take the ID from `autoposter_list_posts`. Never guess one.
- Confirm before any edit, publish or delete.
