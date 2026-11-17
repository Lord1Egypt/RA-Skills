# Threads Profile Module Rules

## 1. Module Scope

Use this module for Threads profile search and user information.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Profile search and user info

## 2. Profile search and user info

- Documentation: `https://docs.keyapi.ai/en/threads/search_profiles.md`
- Documentation: `https://docs.keyapi.ai/en/threads/fetch_user_info.md`
- Documentation: `https://docs.keyapi.ai/en/threads/fetch_user_info_by_id.md`
- Purpose: Find Threads profiles and retrieve user information.

### Best Suited For

- profile discovery
- username/user-ID normalization
- profile validation

### Routing Rules

- Use search profiles when the target account is unknown.
- Use get user info when username/profile input is available.
- Use get user info by ID when the workflow starts from a user ID.
- Preserve user ID and username for posts, replies, and reposts.

## 3. Common Workflows

- Profile lookup: search profiles -> user info or user info by ID.
