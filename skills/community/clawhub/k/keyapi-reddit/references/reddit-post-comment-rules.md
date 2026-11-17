# Reddit Post And Comment Module Rules

## 1. Module Scope

Use this module for single or batch Reddit post detail, post comments, sub-comments, and discussion-thread analysis.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Single and batch post detail

- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_post_details.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_post_details_batch.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_post_details_batch_large.md`
- Purpose: Retrieve detail for one or multiple Reddit posts.

### Best Suited For

- post verification
- thread context baseline
- batch enrichment of search/feed results
- comparison across known post IDs

### Routing Rules

- Use single post detail for one post.
- Use batch max 5 or large batch max 30 only when the user provides or approves multiple IDs.
- Preserve post IDs for comments and follow-on enrichment.
- Do not batch unrelated posts without a comparison or report goal.

## 3. Top-level comments and discussion evidence

- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_post_comments.md`
- Purpose: Retrieve comments under a specified post.

### Best Suited For

- discussion analysis
- sentiment/theme evidence
- audience reaction review
- thread summary

### Routing Rules

- Fetch post detail first when the post context is unknown.
- Use comment pagination or continuation exactly as documented.
- Stop when enough evidence is collected for the requested summary.

## 4. Sub-comments and reply expansion

- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_comment_replies.md`
- Purpose: Retrieve replies under a specific comment node.

### Best Suited For

- deep thread analysis
- controversy/reply chain review
- expanding high-value comments

### Routing Rules

- Use only after comments reveal a comment node with the required continuation cursor/context.
- Expand selected comments, not every comment, unless the user approves deep traversal.
- Keep nested replies separate from top-level comments in summaries.

## 5. Common Workflows

- Post report: single post detail -> comments -> selected sub-comments.
- Search/feed enrichment: discovery module returns post IDs -> batch post details -> comments for selected posts.
- Comparison: batch post details -> normalize metrics and subreddit context -> selected comment evidence.
