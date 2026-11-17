# Instagram Rules

Use this file for platform-level routing boundaries, identifier discipline, and output expectations. Use module files for scenario-specific workflows.

## Entity Scope

users, usernames, user IDs, posts, Reels, Stories, Highlights, followers, following, comments, likes, hashtags, music, explore sections, places, cities, locations, and reposts

## Identifier Discipline

- Resolve usernames, user IDs, shortcodes, media IDs, comment IDs, highlight IDs, music IDs, hashtag IDs, and location/place identifiers explicitly.
- Convert between shortcode and media ID only when a downstream endpoint requires the other form.
- Stories are freshness-sensitive and may expire; do not treat missing stories as historical proof.

## Scenario Module Routing

- Use `instagram-user-rules.md` for user search, profile qualification, profile content portfolios, stories, highlights, followers/following, related profiles, and similar users.
- Use `instagram-content-rules.md` for post detail, comments, replies, likes, shortcode/media ID conversion, hashtag posts, music posts, Reels, and Explore content.
- Use `instagram-discovery-rules.md` for general search, hashtag/music/place search, city lookup, coordinate location search, and discovery seed resolution.
- If a request spans multiple modules, load the smallest set of module files needed and confirm report scope before broad multi-endpoint execution.

## Documentation Hints

- Filter `https://docs.keyapi.ai/llms.txt` for links under `https://docs.keyapi.ai/en/instagram/`.
- Treat endpoint titles as search hints, not stable tool names.
- Extract the current REST method and `/v1/...` path from the endpoint docs page before calling the API.
- Use examples from the docs page only after replacing sample identifiers with user-provided or resolved identifiers.

## Output Guidance

- For creator/profile work, preserve username and user ID for downstream calls.
- For post analysis, separate post metadata, comments/replies, likes, and inferred engagement observations.
- For discovery work, show which seed surface produced each candidate.
- For reports, organize findings by entity, evidence, limitations, and recommended follow-up calls.
