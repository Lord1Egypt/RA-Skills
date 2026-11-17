---
name: oo-twitter
description: "X (Twitter) (x.com). Use this skill for ANY X (Twitter) request — reading, creating, updating, and deleting data. Whenever a task involves X (Twitter), use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "X (Twitter)"
  author: "OOMOL"
  version: "1.0.7"
  services: ["twitter"]
  icon: "https://static.oomol.com/logo/third-party/Twitter.svg"
---

# X (Twitter)

Operate **X (Twitter)** through your OOMOL-connected account. This skill calls the `twitter` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected X (Twitter). **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "twitter" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "twitter" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_list_member` — Add a user account as a member of an X List. [write]
- `add_post_to_bookmarks` — Add a Tweet to bookmarks for the authenticated user account. [write]
- `bookmarks_by_user` — Get bookmarked Tweets for a user account.
- `create_compliance_job` — Create a compliance job using app-only auth. [write]
- `create_dm_conversation` — Create a new group Direct Message conversation with an initial message. [write]
- `create_list` — Create a new X List for the authenticated user account. [write]
- `creation_of_a_post` — Create a Tweet for the authenticated X user. [write]
- `delete_dm` — Delete a Direct Message event from the authenticated user account. [destructive]
- `delete_list` — Delete a List owned by the authenticated user account. [destructive]
- `follow_list` — Follow an X List from the authenticated user account. [write]
- `follow_user` — Follow a target user from the authenticated user account. [write]
- `followers_by_user_id` — Get followers for a user account.
- `following_by_user_id` — Get followed accounts for a user account.
- `full_archive_search` — Search the full public Tweet archive using app-only auth.
- `get_compliance_job` — Get a compliance job by job ID using app-only auth.
- `get_compliance_jobs` — List compliance jobs using app-only auth.
- `get_dm_conversation_events` — Get Direct Message events for a one-to-one conversation with a participant.
- `get_dm_event` — Get a Direct Message event by event ID and optional expanded objects.
- `get_list` — Get a List by List ID and optional expanded owner objects.
- `get_list_followers` — Get users who follow a given X List.
- `get_list_members` — Get users who are members of a given X List.
- `get_media_upload_status` — Get the processing status for a chunked X media upload.
- `get_muted_users` — Get muted accounts for a user account.
- `get_post_retweeters_action` — Get users who retweeted a given Tweet ID.
- `get_post_retweets` — Get Tweet objects that retweeted a given Tweet ID.
- `get_recent_dm_events` — Get recent Direct Message events for the authenticated user account.
- `get_space_by_id` — Get a Space by Space ID and optional expanded objects.
- `get_space_posts` — Get Tweets that were shared in a given X Space.
- `get_space_ticket_buyers` — Get ticket buyers for a ticketed X Space.
- `get_spaces_by_creators` — Get Spaces created by up to 100 user accounts.
- `get_spaces_by_ids` — Get up to 100 Spaces by Space ID and optional expanded objects.
- `get_user_by_id` — Get a public X user profile by user ID and optional expanded objects.
- `get_user_followed_lists` — Get Lists followed by a user account.
- `get_user_list_memberships` — Get Lists that include a given user as a member.
- `get_user_owned_lists` — Get Lists owned by a given user account.
- `get_user_pinned_lists` — Get Lists pinned by a given user account.
- `get_users_by_ids` — Get up to 100 public X user profiles by user ID and optional expanded objects.
- `hide_replies` — Hide or unhide replies for a Tweet authored by the authenticated X user.
- `list_post_likers` — Get users who liked a given Tweet ID.
- `list_posts_timeline_by_list_id` — Get Tweets from a given X List timeline.
- `mute_user` — Mute a target user from the authenticated user account. [destructive]
- `pin_list` — Pin an X List for the authenticated user account.
- `post_delete_by_post_id` — Delete a Tweet authored by the authenticated X user. [destructive]
- `post_lookup_by_post_id` — Get a public Tweet by Tweet ID and optional expanded objects.
- `post_lookup_by_post_ids` — Get up to 100 public Tweets by Tweet ID and optional expanded objects.
- `recent_search` — Search recent Tweets from the last seven days using X search syntax.
- `remove_list_member` — Remove a user account from an X List. [destructive]
- `remove_post_from_bookmarks` — Remove a Tweet from bookmarks for the authenticated user account. [destructive]
- `retrieve_dm_conversation_events` — Get Direct Message events for a Direct Message conversation ID.
- `retrieve_posts_that_quote_a_post` — Get Tweets that quote a given Tweet ID.
- `returns_post_objects_liked_by_the_provided_user_id` — Get Tweets liked by a user account.
- `retweet_post` — Retweet a Tweet from the authenticated user account. [write]
- `search_full_archive_counts` — Count Tweets over the full public archive using app-only auth.
- `search_recent_counts` — Count recent Tweets from the last seven days using X search syntax.
- `search_spaces` — Search X Spaces by query text and optional Space filters.
- `send_a_new_message_to_a_user` — Send a new Direct Message to a user account. [write]
- `send_dm_to_conversation` — Send a new Direct Message to an existing conversation. [write]
- `unfollow_list` — Unfollow an X List from the authenticated user account. [destructive]
- `unfollow_user` — Unfollow a target user from the authenticated user account. [destructive]
- `unlike_post` — Unlike a Tweet from the authenticated user account. [destructive]
- `unmute_user` — Unmute a target user from the authenticated user account. [destructive]
- `unpin_list` — Unpin an X List for the authenticated user account. [destructive]
- `unretweet_post` — Undo a Retweet from the authenticated user account. [destructive]
- `update_list` — Update List attributes for a List owned by the authenticated user account. [write]
- `upload_large_media` — Upload a video or other large media file to X from a temporary HTTP URL using chunked media upload. [write]
- `upload_media` — Upload a single image to X and return the created media identifiers. [write]
- `user_home_timeline_by_user_id` — Get the reverse chronological home timeline for a user account.
- `user_like_post` — Like a Tweet from the authenticated user account. [write]
- `user_lookup_by_username` — Get a public X user profile by username and optional expanded objects.
- `user_lookup_by_usernames` — Get up to 100 public X user profiles by username and optional expanded objects.
- `user_lookup_me` — Get the currently authenticated X user profile and optional expanded objects.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change X (Twitter) state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — X (Twitter) is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/twitter
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- X (Twitter) homepage: https://x.com
- API documentation: https://docs.x.com/x-api/introduction
