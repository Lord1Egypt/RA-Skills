# Postproxy Skill

An Agent Skill for managing social media posts across multiple platforms using the [Postproxy API](https://postproxy.dev/).

## Overview

This skill enables AI agents to create, manage, and schedule social media posts, comments, and direct messages across Facebook, Instagram, TikTok, LinkedIn, YouTube, X/Twitter, Threads, Pinterest, Bluesky, Telegram, and Google Business through the Postproxy API.

## Documentation Structure

The skill uses progressive disclosure: [SKILL.md](SKILL.md) holds the quick start and an index, and detailed endpoint documentation lives in focused rule files that agents load only when needed:

- [rules/profiles.md](rules/profiles.md) — profiles, follower/engagement stats, placements
- [rules/posts.md](rules/posts.md) — create, schedule, threads, update, delete
- [rules/queues.md](rules/queues.md) — posting queues, timeslots, priorities
- [rules/analytics.md](rules/analytics.md) — per-post performance metrics
- [rules/comments.md](rules/comments.md) — post comments and Google Business reviews
- [rules/messages.md](rules/messages.md) — direct messages (chats, reactions, edits)
- [rules/platforms.md](rules/platforms.md) — platform-specific parameters and limits
- [rules/webhooks.md](rules/webhooks.md) — webhook endpoints, events, signature verification
- [rules/errors.md](rules/errors.md) — error formats and async failure statuses
- [rules/sdks.md](rules/sdks.md) — official SDKs for 7 languages

## Installation

Install this skill using the `skills` CLI:

```bash
npx skills add postproxy/postproxy-skill
```

Or install to specific agents:

```bash
npx skills add postproxy/postproxy-skill -a cursor -a claude-code
```

## Setup

Before using this skill, you need to:

1. Get your Postproxy API key from [https://app.postproxy.dev/api_keys](https://app.postproxy.dev/api_keys)
2. Set it as an environment variable:

```bash
export POSTPROXY_API_KEY=your_api_key_here
```

## Usage Examples

Once installed, your AI agent can use this skill to:

### Create a post across multiple platforms

```
Create a post saying "Check out our new feature!" and publish it to Twitter, LinkedIn, and Threads
```

### Create a thread (tweet chain)

```
Create a thread on Twitter about our product launch with 4 posts explaining the features
```

### Schedule a post

```
Schedule a post for tomorrow at 9 AM saying "Good morning! Here's today's update" to Twitter
```

### Create a draft with media

```
Create a draft post with the image from ./screenshot.png and the text "New product launch" for Instagram
```

### Get post stats

```
Show me the stats for my last 3 posts
```

```
How did my Instagram posts perform this week?
```

### Get profile stats

```
Show me follower growth for my Bluesky account over the last month
```

```
What are my latest follower counts across all profiles?
```

### List placements

```
What Facebook pages can I post to?
```

```
Show me my LinkedIn placements
```

### Queue management

```
Show me all my posting queues
```

```
Create a queue called "Weekday Mornings" for profile group pg123, timezone America/New_York, with timeslots Monday through Friday at 9am
```

```
Add a post to queue q1abc with high priority: "Check out our latest feature!" to Twitter and LinkedIn
```

```
Pause queue "morning updates"
```

```
What's the next available slot for queue "morning updates"?
```

### Comment management

```
Show me the comments on my latest Instagram post
```

```
Reply to the top comment on post abc123 saying "Thanks for the kind words!"
```

```
Hide the negative comment cmt_xyz on my Facebook post
```

```
Like the first comment on my Facebook post abc123
```

### Direct messages

```
Show me my recent Instagram DM conversations
```

```
Reply to the latest message in chat chat_xyz789 saying "Yes, we ship worldwide!"
```

```
Send a direct message with the image ./flyer.png to the participant in chat chat_xyz789
```

```
Privately reply to comment cmt_abc123 on post abc123 with the discount details
```

### Google Business reviews

```
List recent reviews on my Google Business profile
```

```
Reply to the latest 5-star review on my Google Business location with "Thanks so much!"
```

### Google Business local posts

```
Post an event on Google Business for our anniversary party on June 15
```

```
Create a Google Business offer with code BEANS20 running through end of June
```

### Webhooks

```
Create a webhook at https://example.com/hooks for all post publishing events
```

```
Show me the recent webhook deliveries and whether any failed
```

### List and manage posts

```
Show me all my scheduled posts
```

```
Delete the post with ID 12345
```

### Update posts

```
Update post abc123 to say "Updated content!" instead
```

```
Reschedule post abc123 for next Monday at 10am
```

```
Change the YouTube privacy on post abc123 to unlisted
```

### Delete from social platforms

```
Delete post abc123 from Twitter only
```

```
Remove post abc123 from all social platforms but keep it in Postproxy
```

```
Delete post abc123 everywhere — DB and platforms
```

## Supported Platforms

- Facebook
- Instagram
- TikTok
- LinkedIn
- YouTube
- X/Twitter
- Threads
- Pinterest
- Bluesky
- Telegram
- Google Business

## Features

- ✅ Create posts with text and media
- ✅ Create thread posts (tweet chains) on Twitter, Threads, and Bluesky
- ✅ Schedule posts for future publication
- ✅ Create drafts for review before publishing
- ✅ Upload local files as media attachments
- ✅ Publish drafts when ready
- ✅ Update existing drafts and scheduled posts (body, schedule, profiles, media, platforms, threads)
- ✅ Delete posts (DB only, or DB + social platforms)
- ✅ Delete posts from individual social platforms while keeping the DB record
- ✅ List profiles and posts
- ✅ Get post stats and performance metrics over time
- ✅ Get profile stats (follower growth + engagement timeseries)
- ✅ List placements (Facebook pages, LinkedIn orgs, Pinterest boards, Telegram channels, Google Business locations)
- ✅ Platform-specific parameters (Instagram Reels, YouTube titles, Telegram parse_mode, Google Business events/offers, etc.)
- ✅ Bluesky rich-text auto-detection (mentions, hashtags, link cards)
- ✅ Telegram bring-your-own-bot publishing to channels
- ✅ Google Business local posts (standard, event, offer formats with CTAs)
- ✅ Queue management (create, update, pause, delete queues)
- ✅ Add posts to queues with priority-based scheduling
- ✅ Weekly timeslot configuration with timezone and jitter support
- ✅ Comment management (list, create, reply, delete)
- ✅ Hide/unhide and like/unlike comments
- ✅ Reply to Google Business reviews via Profile Comments API
- ✅ Async comment operations with status tracking
- ✅ Direct messages — list chats, read/send messages, attachments (Facebook, Instagram, Telegram, Bluesky)
- ✅ React to / edit DMs, archive chats, and private-reply to comments via DM
- ✅ Comment attachments and author metadata (verified status, follower count)
- ✅ Webhooks — 25+ event types with HMAC-SHA256 signature verification, retries, and delivery logs
- ✅ Documented error formats and async failure statuses
- ✅ Official SDKs for Node/TypeScript, Python, Go, Ruby, PHP, Java, and .NET

## Safety

This skill acts on real, connected social media accounts. The skill instructs agents to:

- **Confirm before going public or irreversible** — publishing posts/comments, sending DMs, and deleting content on platforms require summarizing the action (content, targets, scope) and getting explicit user confirmation first. Drafts are preferred when intent is unclear.
- **Distinguish deletion modes** — removing a post from Postproxy's DB leaves it live on the platforms; deleting *on platform* is irreversible.
- **Protect private communications** — DM contents are only read/sent on explicit request and never forwarded to other tools or services without consent. Private replies initiate contact outside Meta's 24h window and require confirmation.
- **Protect credentials** — the API key and webhook secrets are never logged, echoed, or committed. Webhook payloads can include private content, so only user-controlled HTTPS endpoints should be registered.
- **Pin placements** — Facebook posts without an explicit placement go to a random connected page, so placements are always resolved and confirmed first.

## API Documentation

For detailed API documentation, visit [https://postproxy.dev/](https://postproxy.dev/)

## Requirements

- Postproxy API key (get one at [https://app.postproxy.dev/api_keys](https://app.postproxy.dev/api_keys))
- Environment variable `POSTPROXY_API_KEY` must be set

## License

See the repository for license information.

## Related Links

- [Postproxy Website](https://postproxy.dev/)
- [Postproxy API Documentation](https://postproxy.dev/)
- [Skills.sh Directory](https://skills.sh/)
