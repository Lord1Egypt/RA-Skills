# Twitter/X Rules

Use this file for platform-level routing boundaries, identifier discipline, and output expectations. Use module files for scenario-specific workflows.

## Entity Scope

tweets, threads, replies, retweets, profiles, timelines, media, followers, following, communities, lists, trends, jobs, Spaces, affiliates, and live status

## Identifier Discipline

- Keep tweet IDs, profile handles/rest IDs, community IDs, list IDs, Space IDs, and job-search inputs distinct.
- Resolve profile IDs before follower/following/media/timeline workflows when the endpoint requires rest IDs.
- Use tweet detail before thread, replies, or retweets when the tweet context is unclear.

## Scenario Module Routing

- Use `twitter-content-rules.md` for tweet detail, threads, replies, retweets, search, trends, inspiration posts, jobs, and content monitoring.
- Use `twitter-profile-social-rules.md` for profile detail, timelines, media, followers, following, affiliates, follow checks, and live status.
- Use `twitter-community-rules.md` for communities, community posts/members, lists, Spaces, and adjacent network surfaces.
- If a request spans multiple modules, load the smallest set of module files needed and confirm report scope before broad multi-endpoint execution.

## Documentation Hints

- Filter `https://docs.keyapi.ai/llms.txt` for links under `https://docs.keyapi.ai/en/twitter/`.
- Treat endpoint titles as search hints, not stable tool names.
- Extract the current REST method and `/v1/...` path from the endpoint docs page before calling the API.
- Use examples from the docs page only after replacing sample identifiers with user-provided or resolved identifiers.

## Output Guidance

- For tweet work, separate tweet detail, thread context, replies, and retweet/social proof.
- For profile work, separate profile metadata, timeline/media activity, social graph, and relationship checks.
- For community/list work, state the selected surface and sort mode.
- For reports, organize findings by entity, evidence, limitations, and recommended follow-up calls.
