# Reddit Community Module Rules

## 1. Module Scope

Use this module for subreddit info, subreddit feed, community highlights, rules/style, settings, post channels, mute status, and user active subreddit context.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Subreddit baseline and feed

- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_subreddit_info.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_subreddit_feed.md`
- Purpose: Retrieve subreddit profile information and its content feed.

### Best Suited For

- community overview
- subreddit activity monitoring
- content stream review
- post candidate collection

### Routing Rules

- Use subreddit info for profile/baseline.
- Use subreddit feed for current or ordered content.
- Preserve post IDs for post detail/comment workflows.

## 3. Governance, posting rules, and community configuration

- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_subreddit_style.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_subreddit_settings.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_subreddit_post_channels.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/check_subreddit_muted.md`
- Purpose: Retrieve rules, style, settings, post channels, and mute status.

### Best Suited For

- posting feasibility checks
- moderation/policy review
- community setup analysis
- channel selection

### Routing Rules

- Use the specific governance endpoint that matches the question.
- Keep rules/settings/channel facts separate from performance or discussion evidence.
- Do not infer moderation policies beyond returned data.

## 4. Highlights and active community context

- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_community_highlights.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_user_active_subreddits.md`
- Purpose: Retrieve highlighted community content or communities where a user is active.

### Best Suited For

- community highlights review
- user interest mapping
- community-affinity analysis

### Routing Rules

- Use highlights for featured or important community content.
- Use active subreddits after a username is known.
- Do not present active communities as exhaustive interests unless the API defines coverage.

## 5. Common Workflows

- Community report: subreddit info -> feed -> rules/settings/highlights as needed.
- Posting policy review: subreddit info -> rules/style -> settings/channels.
- User-community map: user active subreddits -> subreddit info for selected communities.
