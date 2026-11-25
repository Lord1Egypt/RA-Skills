---
name: kadenzo-social-scheduling
description: Schedule, review and change social media posts through the Kadenzo MCP server, and read post analytics and social listening. Use when the user asks to post, schedule, queue, reschedule or cancel content on Instagram, TikTok, X, LinkedIn, Facebook, YouTube, Pinterest, Threads, Bluesky, Telegram or Mastodon, or asks how their posts or brand mentions are doing.
---

# Scheduling social posts with Kadenzo

Kadenzo is a hosted social media scheduler. The `kadenzo` MCP server
acts on the user's own Kadenzo account (sign in when your agent asks). The
MCP server needs a Professional or Enterprise plan; a 403 error means the
plan doesn't include it, so explain that instead of retrying.

## Before scheduling

1. Call `list_accounts` and use the ids it returns. If more than one account
   matches what the user said (two Instagram accounts, say), ask which one.
2. Confirm the user's time zone before turning "tomorrow at 9" into an ISO
   8601 time, and say the final local time back to them.
3. Kadenzo only schedules for a future time. If the user wants it out "now",
   schedule it a few minutes ahead and tell them.
4. Run `schedule_post` with `validate_only: true` first. It checks network
   limits (character counts, media rules, X daily caps) without creating
   anything.
5. Show the final text, accounts and time, and get a clear yes before the real
   `schedule_post`. Do the same before `update_post`, `cancel_post` or
   `post_comment`.

## Writing the post

- Write for each network rather than pasting one caption everywhere. Per-network
  text goes in `platform_content`, keyed by platform.
- `generate_content` drafts captions with Kadenzo's AI writer if the user wants
  options to pick from.
- `get_best_times` suggests slots from the account's own posting history.
- Media must be a public URL (Google Drive and Dropbox share links work).

## Checking results

- `list_posts` and `get_post` show what's queued, published or failed, with a
  per-account status.
- `get_account_analytics` and `get_post_analytics` read performance.
- `list_mentions`, `get_listening_analytics` and `get_share_of_voice` cover
  social listening for the keywords set up in Kadenzo.

## Network notes

- LinkedIn posts go to personal profiles, not Company Pages.
- X is metered per account: a daily post cap and a monthly cap on posts with
  links, both set by plan. A validation error names the limit.
- Instagram carousels take 2 to 10 items.

Docs: https://studio.kadenzo.app/developers · Plans: https://kadenzo.app/pricing
