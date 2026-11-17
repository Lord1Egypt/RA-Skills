# Pinterest Content Module Rules

## 1. Module Scope

Use this module for Pinterest boards and pins.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Boards and pins

## 2. Boards and pins

- Documentation: `https://docs.keyapi.ai/en/pinterest/boards.md`
- Documentation: `https://docs.keyapi.ai/en/pinterest/pins.md`
- Purpose: Inspect what a user curates or publishes through boards and pins.

### Best Suited For

- brand/creator content audit
- moodboard/topic research
- pin inventory review
- board-level analysis

### Routing Rules

- Fetch user information first if identity is uncertain.
- Use boards for collection structure and pins for content inventory.
- Avoid fetching every board/pin unless the user approves a broad audit.

## 3. Common Workflows

- Content audit: user information -> boards -> pins for selected boards.
