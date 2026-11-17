# Pinterest Network Module Rules

## 1. Module Scope

Use this module for Pinterest followers and following relationships.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Followers and following

## 2. Followers and following

- Documentation: `https://docs.keyapi.ai/en/pinterest/followers.md`
- Documentation: `https://docs.keyapi.ai/en/pinterest/followings.md`
- Purpose: Inspect follower or following relationships for a Pinterest user.

### Best Suited For

- audience sampling
- network context
- creator discovery through social graph

### Routing Rules

- Use followers or following based on requested direction.
- Enrich only selected related users unless broad traversal is approved.
- State direction clearly in the final output.

## 3. Common Workflows

- Network review: user information -> followers or following -> selected profile enrichment.
