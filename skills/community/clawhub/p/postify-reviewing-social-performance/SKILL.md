---
name: reviewing-social-performance
description: "Reports how social posts performed in Postify: posts delivered, delivery rate, failures, per-channel stats, and the best times to post on each platform. Use when the user asks 'how did last month go', 'which channel performs best', 'show my social media analytics', 'how many posts went out', 'why did posts fail', 'when should I post on Instagram', or wants a social media performance report. Read-only."
---

# Postify performance review

Read the workspace's delivery analytics and turn them into a short, honest report.

## Connecting and calling the tools

Every tool in this skill comes from the `postify` MCP server, the Postify connector, and is written here as `postify:<tool>`.

- **Tools listed by name:** call them directly, for example `postify:list_posts`.
- **Only `postify:search_tools` and `postify:execute_typescript` listed (Code Mode, the default):** call `postify:search_tools` first, then call each tool inside `postify:execute_typescript` as `external_<tool>` (for example `external_list_posts`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `postify:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects Postify and approves that scope.
- **No `postify` tools at all:** Postify is not connected yet. Install the Postify power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `postify:get_analytics`: workspace analytics for delivered posts: post counts, delivery rate, per-channel stats, for a date range.
- `postify:suggest_optimal_time`: suggested posting times per platform from the workspace's own publish history. No model call, no external data.
- `postify:list_posts`: to name the specific posts behind a number when the user asks "which ones".

## Workflow

1. Agree the window (default: the last 30 days). Call `postify:get_analytics` for it.
2. Report in this order: total posts delivered, delivery rate, failed posts, then a per-channel table sorted by volume.
3. If there were failures, call `postify:list_posts` filtered to `failed` for the window and list them with their channel and datetime so the user can act.
4. Call `postify:suggest_optimal_time` for each platform the user publishes on and give the top suggestion per platform.
5. Close with at most three concrete next steps drawn from the numbers.

## Rules

- Only report numbers the tools returned. If a metric is missing, say it is not available in Postify analytics.
- Do not compare the user to industry benchmarks; there are none in the data.
- This skill only reads. Never call `postify:create_draft`, `postify:reschedule_post`, `postify:publish_now`, or `postify:delete_post` from it.
