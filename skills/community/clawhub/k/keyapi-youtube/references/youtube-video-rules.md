# YouTube Video Module Rules

## 1. Module Scope

Use this module for YouTube video information, comments, sub-comments, related videos, streams info, and video-level reports.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Video detail baseline

- Documentation: `https://docs.keyapi.ai/en/youtube/get_video_info.md`
- Purpose: Retrieve detailed raw information for one video.

### Best Suited For

- video metadata report
- engagement/channel context
- selected search-result enrichment
- video URL or ID lookup

### Routing Rules

- Use when the user provides a video URL/ID or asks for detail on one video.
- Preserve video ID for comments, sub-comments, related videos, and streams info.
- Do not fetch comments/streams/related videos unless they support the user goal.

## 3. Comments and sub-comments

- Documentation: `https://docs.keyapi.ai/en/youtube/get_video_comments.md`
- Documentation: `https://docs.keyapi.ai/en/youtube/get_video_comment_replies.md`
- Purpose: Retrieve video comments and replies to comments.

### Best Suited For

- audience reaction analysis
- comment evidence
- discussion expansion
- sentiment/theme sampling

### Routing Rules

- Use comments first.
- Use sub-comments only after a selected comment provides the required context.
- Respect continuation tokens exactly as documented.
- Stop when enough evidence has been collected.

## 4. Related videos and recommendation context

- Documentation: `https://docs.keyapi.ai/en/youtube/get_related_videos.md`
- Purpose: Retrieve recommended related content for a video.

### Best Suited For

- adjacent content discovery
- competitor/video cluster research
- recommendation context

### Routing Rules

- Use related videos for content adjacency, not as proof of global ranking.
- Enrich selected related videos with video information only when needed.

## 5. Streams and playback formats

- Documentation: `https://docs.keyapi.ai/en/youtube/get_video_streams.md`
- Purpose: Retrieve playback/format information for a video.

### Best Suited For

- format inspection
- download/playback option analysis
- technical media checks

### Routing Rules

- Use only when format, stream, or playback URL data is explicitly needed.
- Keep stream/format facts separate from content performance facts.

## 6. Common Workflows

- Video report: video information -> comments -> selected sub-comments -> related videos if needed.
- Audience analysis: video information -> comments -> sub-comments for selected high-value threads.
- Media inspection: video information -> streams info.
