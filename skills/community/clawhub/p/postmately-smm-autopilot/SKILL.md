---
name: smm-autopilot
description: Run social media on autopilot for a small business. Turn a website or a topic into a month of posts, carousels and videos, get approval, schedule through Postmately MCP, and measure what worked. Use when the user asks to run SMM, build a content plan, generate posts, or automate social media.
---

# SMM Autopilot

This skill turns one link or topic into a repeatable social media system:
a content plan, posts, carousels, videos, approval, scheduling and a
measurement loop. It uses Postmately MCP for generation and publishing.

## Setup

1. Create an API key in Postmately under Settings, then API.
2. Keep it in the environment as `POSTMATELY_API_KEY`. Never print it or
   commit it.
3. Connect MCP: `https://api.postmately.com/mcp` with
   `Authorization: Bearer $POSTMATELY_API_KEY`.

## Workflow

### 1. Discover the channels

Call `list_channels`. Use only channels with `canPublish: true`. Read
`rules`: `maxChars`, `mediaRequired`, `maxImages`, `maxVideos`.

Ask for one primary channel and one measurable goal for the month:
12 posts, 30 site visits or 10 leads. Do not start with five networks.

### 2. Build the plan

Use four buckets:

- utility: answer a customer question;
- process: show how the work is done;
- trust: show a person, result or review;
- sale: offer, price, booking.

Create 12 to 16 topics for the month from the website, prices, reviews,
FAQs and before/after photos. Keep the mix: two utility, one process,
one trust and one sale for every five posts.

### 3. Generate the assets

Call `get_credits` first. A carousel costs 20 credits and a branded video
costs 60. Use `make_carousel` with a website link or topic, then poll
`get_carousel` until `status` is `ready`. Use `make_video` for a branded
vertical video and poll `get_video` until `state` is `ready`.

If the user already has final images or clips, use `import_media` and
skip generation. Do not spend credits when the files already exist.

For a video edited on this machine, `list_clips` (or `GET https://api.postmately.com/v1/clips`,
no key) is Postmately's free hook gallery: people reacting, 1080x1920, with
meta to pick by (fits, mood, setting, a phone in hand, sample lines). The two
formats that travel furthest on TikTok are a hook and an app demo
(`fits=hook-demo`, then the product's screens) and a hook and a wall of text
(`fits=wall`). Recipes: https://postmately.com/skills/postmately-video/SKILL.md

### 4. Validate before writing

Call `validate_post` with the channel, text and media ids. Read `issues`
and fix them. Never guess a platform rule.

### 5. Draft, approve, schedule

Create the post with `create_post` and `when: "draft"` unless the user
explicitly said to publish or gave a time. Show the draft and wait for a
clear yes. Then use `when: "next_slot"`, `when: "now"` or an ISO time
with a time zone.

Publishing is public and cannot be undone. A draft is the default.

### 6. Measure and iterate

Use `get_post`, `get_post_metrics`, `get_channel_insights` and
`get_analytics_overview`. Compare the four buckets. Keep the formats that
got views, saves, clicks or replies. Replace the weak ones next month.

## Guardrails

- No fake reviews, engagement farming or purchased followers.
- No misleading claims, fake before/after or invented numbers.
- No auto-publish without explicit approval.
- Respect each platform's rules and the workspace's channel limits.
- Do not ask for or print the API key.
- Do not use the skill to post from accounts the user does not own.

## Example prompts

- "Take postmately.com and build a month of Telegram posts for a small
  SaaS. Draft everything, do not publish."
- "Make three carousels from this link and show them for approval."
- "Review last month's posts and tell me which bucket worked best."
- "Turn this customer question into a post, a carousel and a short
  video, then schedule the best one for next week."
