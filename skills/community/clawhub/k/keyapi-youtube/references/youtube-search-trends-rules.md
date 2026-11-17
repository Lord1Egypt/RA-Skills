# YouTube Search And Trends Module Rules

## 1. Module Scope

Use this module for YouTube general search with filters, video search, Shorts search, trending videos, channel search, and search suggestions.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Search suggestions and query expansion

- Documentation: `https://docs.keyapi.ai/en/youtube/get_search_suggestions.md`
- Purpose: Generate YouTube search suggestions from a seed query.

### Best Suited For

- keyword expansion
- topic ideation
- search intent exploration

### Routing Rules

- Use before search when the user asks for query ideas or wants a broader topic map.
- Do not present suggestions as ranking evidence.

## 3. Video and filtered search

- Documentation: `https://docs.keyapi.ai/en/youtube/search_video.md`
- Documentation: `https://docs.keyapi.ai/en/youtube/get_general_search.md`
- Purpose: Search YouTube videos or run advanced filtered search.

### Best Suited For

- video discovery
- topic research
- filtered search by upload time/duration/type/features/sort
- candidate video collection

### Routing Rules

- Use search video for simple video queries.
- Use general search with filters when the user specifies upload time, duration, content type, features, or sort.
- Enrich selected videos through video rules.

## 4. Shorts-specific discovery

- Documentation: `https://docs.keyapi.ai/en/youtube/get_shorts_search.md`
- Purpose: Search YouTube Shorts using the native Shorts search surface.

### Best Suited For

- short-form video research
- Shorts creator/content discovery
- short-video trend examples

### Routing Rules

- Use this when the user explicitly asks for Shorts.
- Follow continuation guidance because first responses may include mixed content.
- Enrich selected Shorts through video rules when details/comments are needed.

## 5. Trending videos and channel discovery

- Documentation: `https://docs.keyapi.ai/en/youtube/get_trending_videos.md`
- Documentation: `https://docs.keyapi.ai/en/youtube/search_channel.md`
- Documentation: `https://docs.keyapi.ai/en/youtube/search_channels.md`
- Purpose: Retrieve trending videos or search channels.

### Best Suited For

- market trend scan
- current popular video monitoring
- creator/channel discovery

### Routing Rules

- Use trending videos for current market attention.
- Use channel search endpoints for creator/channel discovery.
- Route selected videos to video rules and selected channels to channel rules.

## 6. Common Workflows

- Topic research: suggestions -> video/filtered search -> selected video detail/comments.
- Shorts research: Shorts search -> selected video information/comments.
- Trend scan: trending videos -> selected video detail -> channel enrichment if needed.
- Channel discovery: channel search -> channel description/videos.
