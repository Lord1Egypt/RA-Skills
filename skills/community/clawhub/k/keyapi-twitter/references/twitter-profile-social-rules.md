# Twitter/X Profile And Social Module Rules

## 1. Module Scope

Use this module for profile detail, profile resolution, timelines, media, followers, following, affiliates, follow checks, and live status.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Profile identity and baseline

- Documentation: `https://docs.keyapi.ai/en/twitter/screenname.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/about.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/screennames.md`
- Purpose: Resolve and retrieve Twitter/X profile metadata.

### Best Suited For

- profile validation
- handle/rest ID normalization
- account baseline reports
- batch profile enrichment

### Routing Rules

- Use user info or about profile according to the documented input shape.
- Use profiles by rest IDs when IDs are already known or batch enrichment is needed.
- Preserve handle/rest ID for timeline, media, social graph, and relationship endpoints.

## 3. Timeline, media, and live status

- Documentation: `https://docs.keyapi.ai/en/twitter/timeline.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/usermedia.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/broadcast.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/top_posts.md`
- Purpose: Retrieve account-authored content, media posts, live status, or inspiration-style posts.

### Best Suited For

- account activity audits
- media portfolio review
- live status checks
- recent post monitoring

### Routing Rules

- Use timeline for authored posts and users media for media-specific output.
- Use user live only when live/broadcast status matters.
- Enrich selected tweets with content rules if detailed tweet/thread/commentary is needed.

## 4. Followers, following, affiliates, and relationship checks

- Documentation: `https://docs.keyapi.ai/en/twitter/followers.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/following.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/affilates.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/checkfollow.md`
- Purpose: Inspect social graph or specific follow relationships.

### Best Suited For

- audience sampling
- following analysis
- affiliate account discovery
- relationship verification

### Routing Rules

- Use followers/following based on requested direction.
- Use affiliates only when affiliated account context is requested.
- Use check follow for one specific relationship.
- Enrich only selected related profiles unless broad graph traversal is approved.

## 5. Common Workflows

- Profile report: user info/about -> timeline/media -> followers/following/affiliates if requested.
- Relationship check: resolve source and target profiles -> check follow.
- Account activity audit: profile baseline -> timeline/media -> selected tweet detail/thread.
