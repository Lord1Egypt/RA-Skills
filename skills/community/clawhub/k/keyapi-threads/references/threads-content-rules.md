# Threads Content Module Rules

## 1. Module Scope

Use this module for Threads user posts, replies, reposts, post detail, and comments.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. User activity portfolio
3. Post detail and comments

## 2. User activity portfolio

- Documentation: `https://docs.keyapi.ai/en/threads/fetch_user_posts.md`
- Documentation: `https://docs.keyapi.ai/en/threads/fetch_user_replies.md`
- Documentation: `https://docs.keyapi.ai/en/threads/fetch_user_reposts.md`
- Purpose: Retrieve user authored posts, replies, and reposts.

### Best Suited For

- profile activity audit
- reply behavior review
- repost behavior review

### Routing Rules

- Choose posts, replies, or reposts based on requested surface.
- Do not fetch all surfaces by default; confirm sections for broad reports.
- Enrich selected posts with post detail/comments if needed.

## 3. Post detail and comments

- Documentation: `https://docs.keyapi.ai/en/threads/fetch_post_detail.md`
- Documentation: `https://docs.keyapi.ai/en/threads/fetch_post_comments.md`
- Purpose: Inspect a post and retrieve discussion comments.

### Best Suited For

- post analysis
- comment evidence collection
- audience reaction review

### Routing Rules

- Fetch post detail before comments when context is unclear.
- Use comments only when discussion or audience reaction matters.
- Keep post facts separate from comment observations.

## 4. Common Workflows

- Profile activity: user info -> posts/replies/reposts -> selected post comments.
- Post report: post detail -> comments.
