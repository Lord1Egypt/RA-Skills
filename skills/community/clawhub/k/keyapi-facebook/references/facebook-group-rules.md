# Facebook Group Module Rules

## 1. Module Scope

Use this module for public Facebook group ID resolution, group details, group posts, and future events.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Group identity and detail
3. Group posts and events

## 2. Group identity and detail

- Documentation: `https://docs.keyapi.ai/en/facebook/group_id.md`
- Documentation: `https://docs.keyapi.ai/en/facebook/group_details.md`
- Purpose: Resolve public group identity and retrieve group baseline detail.

### Best Suited For

- public group validation
- community overview
- group URL-to-ID conversion

### Routing Rules

- Use get group ID when the group ID is unknown.
- Use group details after ID resolution or when an ID is provided.
- Keep group identifiers separate from profile/page IDs.

## 3. Group posts and events

- Documentation: `https://docs.keyapi.ai/en/facebook/group_posts.md`
- Documentation: `https://docs.keyapi.ai/en/facebook/group_future_events.md`
- Purpose: Retrieve public group posts and upcoming events.

### Best Suited For

- community activity reports
- post monitoring
- upcoming event checks

### Routing Rules

- Use group posts for content/activity analysis.
- Use future events only when the user asks about upcoming activity.
- Do not infer membership/private group data beyond returned fields.

## 4. Common Workflows

- Group report: group ID -> group details -> group posts -> future events when requested.
