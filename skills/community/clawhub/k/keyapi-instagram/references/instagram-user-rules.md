# Instagram User Module Rules

## 1. Module Scope

Use this module for Instagram user discovery, profile qualification, user content portfolios, Stories, Highlights, tagged/reposted content, followers/following, related profiles, and similar users.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. User discovery and profile qualification

- Documentation: `https://docs.keyapi.ai/en/instagram/search_users.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/general_search.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_user_info.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/user_id_to_username.md`
- Purpose: Find candidate accounts and retrieve a stable profile baseline.

### Best Suited For

- creator discovery
- brand/profile validation
- username to user-ID normalization
- shortlist enrichment

### Routing Rules

- Use search users for explicit profile discovery.
- Use general search when the user wants a broader Instagram search surface.
- Use get user info when username or URL-like input is available.
- Use get user info by user ID when a workflow starts from an ID.
- Preserve username and user ID for all downstream user content and graph calls.

## 3. Profile content portfolio audit

- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_user_posts.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_user_reels.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_user_tagged_posts.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_user_reposts.md`
- Purpose: Collect a profile content portfolio by surface.

### Best Suited For

- creator content audits
- Reels portfolio review
- tagged-post evidence
- repost/share behavior analysis

### Routing Rules

- Choose posts, Reels, tagged posts, or reposts based on the requested content surface.
- Do not fetch every surface by default; confirm sections for broad profile reports.
- Preserve post shortcode/media ID for post detail, comments, likes, and conversion workflows.

## 4. Stories and highlight review

- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_user_stories.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_user_highlights.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_highlight_stories.md`
- Purpose: Retrieve active Stories, highlight collections, or stories inside a selected highlight.

### Best Suited For

- fresh story checks
- profile highlight audits
- ephemeral content review

### Routing Rules

- Use active stories only when current Story content matters.
- Use user highlights before highlight stories when the highlight ID is unknown.
- Stories may expire; missing Stories should not be presented as historical proof.

## 5. Audience and relationship exploration

- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_user_followers.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_user_following.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_related_profiles.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_similar_users.md`
- Purpose: Inspect relationship lists or expand discovery through related/similar accounts.

### Best Suited For

- audience sampling
- following/follower checks
- creator expansion
- competitive account discovery

### Routing Rules

- Use followers/following only when relationship lists are explicitly requested.
- Use related or similar profiles for discovery before considering broad graph traversal.
- Enrich only selected discovered accounts unless the user approves a larger crawl.

## 6. Common Workflows

- Profile report: search or direct user info -> selected content surfaces -> stories/highlights or relationship endpoints only if requested.
- Creator discovery: search users/general search -> related/similar users -> user info for selected accounts.
- Portfolio audit: user info -> user posts/Reels/tagged/reposts -> post module enrichment for selected content.
