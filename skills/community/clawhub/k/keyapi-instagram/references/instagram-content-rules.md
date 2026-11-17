# Instagram Content Module Rules

## 1. Module Scope

Use this module for post detail, shortcode/media ID conversion, comments, replies, likes, hashtag posts, music posts, Reels search, and Explore section content.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Post detail and identifier conversion

- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_post_info.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/shortcode_to_media_id.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/media_id_to_shortcode.md`
- Purpose: Retrieve post detail and normalize post identifiers.

### Best Suited For

- post URL analysis
- shortcode/media ID normalization
- preparing comment/reply/like workflows
- selected content enrichment

### Routing Rules

- Use post info when the user provides a post URL or shortcode.
- Convert identifiers only when a downstream endpoint requires the other form.
- Preserve both shortcode and media ID when returned.

## 3. Comment, reply, and like analysis

- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_post_comments.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_comment_replies.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_post_likes.md`
- Purpose: Retrieve discussion and engagement-account evidence for a post.

### Best Suited For

- comment review
- reply thread expansion
- liker sampling
- audience reaction evidence

### Routing Rules

- Use comments before replies; replies require a known comment ID.
- Use likes only when liked-by data is directly useful.
- For sentiment or theme analysis, collect enough comments but stop when the evidence target is met.

## 4. Hashtag, music, and Reels content research

- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_hashtag_posts.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_music_posts.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/search_reels.md`
- Purpose: Retrieve content around a hashtag, audio track, or Reels keyword.

### Best Suited For

- topic content research
- audio trend checks
- Reels discovery
- creative examples for a niche

### Routing Rules

- Resolve hashtag or music identifiers through discovery rules when only text is known.
- Use Reels search when the user specifically asks for Reels or short-video examples.
- Enrich selected posts with post info/comments rather than all results.

## 5. Explore section content

- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_explore_sections.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_section_posts.md`
- Purpose: Browse Explore sections and retrieve posts inside a selected section.

### Best Suited For

- Explore surface review
- section-based content discovery
- creative/category scanning

### Routing Rules

- Use explore sections before posts by section when the section ID is unknown.
- Do not treat Explore output as a general ranking unless the docs define the ordering.

## 6. Common Workflows

- Post report: post info -> comments -> selected replies -> likes only if useful.
- Hashtag research: discovery resolves hashtag -> posts by hashtag -> selected post info/comments.
- Music trend review: music discovery -> posts using music -> selected post details.
- Explore review: sections -> posts by selected section -> selected post enrichment.
