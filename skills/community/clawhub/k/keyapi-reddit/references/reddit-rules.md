# Reddit Rules

Use this file for platform-level routing boundaries, identifier discipline, and output expectations. Use module files for scenario-specific workflows.

## Entity Scope

posts, comments, sub-comments, users, trophies, active communities, subreddits, rules, settings, channels, feeds, search results, typeahead suggestions, and trending searches

## Identifier Discipline

- Keep post IDs, comment IDs, usernames, and subreddit names separate.
- Use batch post detail only when the user provides or approves multiple post IDs.
- Use sub-comment endpoints only after a comment node provides the required continuation context.

## Scenario Module Routing

- Use `reddit-post-comment-rules.md` for single/batch post detail, post comments, sub-comments, and discussion-thread analysis.
- Use `reddit-community-rules.md` for subreddit info, feed, rules/style, settings, channels, highlights, mute status, and active subreddit context.
- Use `reddit-discovery-rules.md` for dynamic search, typeahead, trending searches, popular/home/news/games feeds, and user activity discovery.
- If a request spans multiple modules, load the smallest set of module files needed and confirm report scope before broad multi-endpoint execution.

## Documentation Hints

- Filter `https://docs.keyapi.ai/llms.txt` for links under `https://docs.keyapi.ai/en/reddit/`.
- Treat endpoint titles as search hints, not stable tool names.
- Extract the current REST method and `/v1/...` path from the endpoint docs page before calling the API.
- Use examples from the docs page only after replacing sample identifiers with user-provided or resolved identifiers.

## Output Guidance

- For discussion analysis, separate post detail, top-level comments, and nested replies.
- For community analysis, separate profile, governance, feed, highlights, and user-affinity evidence.
- For feed/search work, state the surface used and enrich only selected posts.
- For reports, organize findings by entity, evidence, limitations, and recommended follow-up calls.
