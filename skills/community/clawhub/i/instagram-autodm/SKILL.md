---
name: instagram-manager
description: Manage an Instagram creator or business account through the InstantDM MCP tools — triage and reply to comments, answer DMs, monitor and reply to ad comments, pull account/post insights and follower trends, and work with the linked Facebook Page. Use whenever the user asks to check Instagram engagement, reply to followers, review comments, send DMs, report on Instagram performance, or handle comments on their Meta ads.
---

# Instagram Manager (InstantDM)

You manage a real Instagram account through InstantDM's MCP tools. Every send reaches a real person and costs the user 1 InstantDM credit. Work carefully.

## Ground rules

1. **Start every session with `whoami`** — confirms the connection, shows which Instagram account you're operating, the plan, and remaining credits. If it errors, walk the user through getting a key at app.instantdm.com/api-integration and connecting `https://openapi.instantdm.com/mcp?auth=<key>`.
2. **Never send without approval.** Before calling `reply_to_comment`, `send_dm`, `reply_to_ad_comment`, `reply_to_fb_comment`, or `trigger_flow`, show the user the exact text and the exact target (username/comment), and get explicit confirmation. For batches, present the full batch and state the total credit cost against the balance from `whoami`.
3. **Stop on 402 or 429.** 402 = credits exhausted → stop, link the user to app.instantdm.com to top up; never retry. 429 = hourly limit → stop the batch and report what was sent and what remains; never spin.
4. **Never mass-send identical text** to many users — it endangers the creator's Instagram account. Vary drafts, keep batches small.
5. **Ads tools** need the account connected via Facebook Login. On a `reconnect_required` error, tell the user to reconnect in InstantDM settings — don't retry.
6. Don't paste long private conversation contents into outputs unless the user asked to see them.

## Workflows

### Morning engagement triage
1. `whoami`, then `list_posts` (first page is usually enough).
2. `list_comments` on the recent posts with comment activity.
3. Classify each comment: **question**, **lead** (buying intent), **praise**, **spam/negative**.
4. Draft replies — public reply for praise/questions others benefit from seeing; `visibility: private_dm` for pricing, links, or anything personal. Match the creator's tone from earlier replies.
5. Present the drafts as a table (comment → proposed reply → visibility) for approval, then send only the approved ones.
6. Tag leads with `create_or_update_contact` (e.g. tags: ["lead"]).

### Inbox follow-up
1. `list_conversations`, note unread and recent threads.
2. `get_conversation` on threads needing a reply; summarize each thread's state.
3. Draft replies, get approval, `send_dm`.

### Weekly performance report
1. `get_account_insights` (days: 7) for the week's totals and follower series.
2. `list_posts`, then `get_post_insights` on the week's posts.
3. Report: headline numbers with week context, top and bottom posts with a hypothesis why, and 2-3 concrete recommendations (format, topic, timing). Plain language, no filler metrics.

### Ad comment monitoring
1. `list_ad_accounts` → `list_ads` (each ad shows spend/impressions and its Instagram media).
2. `list_ad_comments` per active ad.
3. Flag questions and negative comments first — unanswered ad comments burn ad spend.
4. Draft replies (public for product questions; `private_dm` for pricing/support), get approval, `reply_to_ad_comment`.

### Facebook Page pass
Same triage pattern with `list_fb_page_posts` → `list_fb_page_comments` → `reply_to_fb_comment`.

## Notes

- Pagination: list tools accept `cursor`; pass the previous result's `paging.cursors.after`.
- `get_conversation` returns full text only for the ~20 most recent messages per thread (Instagram limitation).
- `disable_automation` pauses ALL the account's automations, not one contact — only on explicit request.
