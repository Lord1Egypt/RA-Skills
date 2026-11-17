# Pinterest Profile Module Rules

## 1. Module Scope

Use this module for Pinterest user search and profile information.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. User search and profile baseline

## 2. User search and profile baseline

- Documentation: `https://docs.keyapi.ai/en/pinterest/search.md`
- Documentation: `https://docs.keyapi.ai/en/pinterest/information.md`
- Purpose: Find Pinterest accounts and retrieve profile information.

### Best Suited For

- creator or brand discovery
- profile validation
- account shortlist enrichment

### Routing Rules

- Use search users when the target account is unknown.
- Use user information when username or user identifier is known.
- Preserve user identifiers for boards, pins, followers, and following.

## 3. Common Workflows

- Profile lookup: search users -> user information.
