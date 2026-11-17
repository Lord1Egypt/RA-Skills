# Threads Rules

Use this file for Threads platform-level routing boundaries. Use module files for scenario-specific workflows.

## Entity Scope

users, user IDs, profiles, posts, replies, reposts, comments, top content, recent content, and profile search results

## Scenario Module Routing

- Use `threads-profile-rules.md` for profile search and user info.
- Use `threads-content-rules.md` for user posts, replies, reposts, post detail, and comments.
- Use `threads-search-rules.md` for top and recent content search.

## Identifier Discipline

- Resolve profile username/user ID before user posts, replies, or reposts.
- Use post shortcode or full URL for post detail before comment analysis.
- Keep top content and recent content as different search modes.

## Output Guidance

- For profile work, separate profile metadata, authored posts, replies, and reposts.
- For post work, separate post detail from comment evidence.
- For content search, state whether top or recent mode was used.
