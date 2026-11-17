# Facebook Profile Content Module Rules

## 1. Module Scope

Use this module for public Facebook profile/page posts, Reels, and photos.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Posts, Reels, and photos

## 2. Posts, Reels, and photos

- Documentation: `https://docs.keyapi.ai/en/facebook/profile_posts.md`
- Documentation: `https://docs.keyapi.ai/en/facebook/profile_reels.md`
- Documentation: `https://docs.keyapi.ai/en/facebook/profile_photos.md`
- Purpose: Retrieve public posts, Reels, and photos from a profile/page.

### Best Suited For

- public content audits
- page activity summaries
- Reels review
- photo evidence collection

### Routing Rules

- Resolve the profile/page first when identity is ambiguous.
- Choose posts, Reels, or photos based on requested surface.
- Paginate only until requested evidence or top N is satisfied.
- Preserve post/media identifiers for reporting.

## 3. Common Workflows

- Content audit: profile/page detail -> posts/Reels/photos as requested -> summarize factual activity.
