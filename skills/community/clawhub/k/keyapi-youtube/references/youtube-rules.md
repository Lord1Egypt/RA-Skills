# YouTube Rules

Use this file for platform-level routing boundaries, identifier discipline, and output expectations. Use module files for scenario-specific workflows.

## Entity Scope

videos, Shorts, comments, sub-comments, streams, related videos, search results, trending videos, channels, channel IDs, channel URLs, channel videos, and search suggestions

## Identifier Discipline

- Resolve channel IDs, channel handles/URLs, video IDs, comment IDs, continuation tokens, and search queries explicitly.
- Use channel ID/URL conversion endpoints only when the workflow needs a different channel identifier form.
- Use sub-comment endpoints only after a comment result provides the required comment context.

## Scenario Module Routing

- Use `youtube-video-rules.md` for video information, comments, sub-comments, streams info, related videos, and video-level reports.
- Use `youtube-channel-rules.md` for channel description, channel videos, channel search, and channel ID/URL conversion.
- Use `youtube-search-trends-rules.md` for general search, filtered search, video search, Shorts search, trending videos, and search suggestions.
- If a request spans multiple modules, load the smallest set of module files needed and confirm report scope before broad multi-endpoint execution.

## Documentation Hints

- Filter `https://docs.keyapi.ai/llms.txt` for links under `https://docs.keyapi.ai/en/youtube/`.
- Treat endpoint titles as search hints, not stable tool names.
- Extract the current REST method and `/v1/...` path from the endpoint docs page before calling the API.
- Use examples from the docs page only after replacing sample identifiers with user-provided or resolved identifiers.

## Output Guidance

- For video reports, separate video metadata, comments, sub-comments, streams, and related-video context.
- For channel reports, separate channel profile, channel videos, and search-discovered channels.
- For search/trend work, state the surface and filters used.
- For reports, organize findings by entity, evidence, limitations, and recommended follow-up calls.
