---
name: managing-content-calendar
description: "Reviews and reorganizes the social media content calendar in Postify: lists scheduled, draft, published, and failed posts, finds gaps in the posting schedule, and reschedules a post after confirmation. Use when the user asks 'what's scheduled next week', 'show my upcoming posts', 'move Friday's post to Monday 9am', 'reschedule this post', 'where are the gaps in my posting schedule', 'which posts failed', or wants a social media planner or posting calendar overview. Never publishes or deletes."
---

# Postify content calendar

Work the user's Postify calendar through the `postify` MCP server. All tools operate on the organization behind the connected account.

## Connecting and calling the tools

Every tool in this skill comes from the `postify` MCP server, the Postify connector, and is written here as `postify:<tool>`.

- **Tools listed by name:** call them directly, for example `postify:list_posts`.
- **Only `postify:search_tools` and `postify:execute_typescript` listed (Code Mode, the default):** call `postify:search_tools` first, then call each tool inside `postify:execute_typescript` as `external_<tool>` (for example `external_list_posts`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `postify:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects Postify and approves that scope.
- **No `postify` tools at all:** Postify is not connected yet. Install the Postify power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `postify:list_posts`: posts with id, status (`draft`, `scheduled`, `published`, `failed`), scheduled datetime, and target channels. Filter by status or date range when the tool offers it.
- `postify:get_schedule`: scheduled posts in a date window (`from`, `to`, `limit` up to 50).
- `postify:get_post`: the full content of one post when the list summary is not enough.
- `postify:list_channels`: connected social accounts (platform, handle, connection status). Use it to name channels correctly instead of guessing.
- `postify:reschedule_post`: move a scheduled post to a new datetime. Content is unchanged.

## Workflow

1. Call `postify:list_channels` once so you know which platforms exist.
2. Call `postify:get_schedule` for the window the user cares about (default: today through the next 7 days). Use `postify:list_posts` when the user also wants drafts, published, or failed posts.
3. Present the calendar grouped by day, then by channel. Show status and local time. Mark failed posts first.
4. For gaps, compare against the user's stated cadence (ask once if unknown) and list the empty days per channel.
5. To move a post, confirm the post id and the new time with the user, then call `postify:reschedule_post`. Echo the new datetime back.

## Rules

- Never call `postify:publish_now` or `postify:delete_post` from this skill. Moving and reviewing only.
- Times: the server returns ISO 8601 datetimes. Convert to the user's timezone when you present them and say which timezone you used.
- If `postify:list_posts` returns nothing, say so plainly and offer the `drafting-social-posts` skill.
