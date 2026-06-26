---
name: pipintama-boards
description: Create, fetch, share, or change visibility for hosted Pipintama Boards through the MCP server. Use when a user needs a mindmap, flowchart, kanban board, or architecture map, and the right output is a hosted visual board link instead of only prose.
---

# Pipintama Boards

Use this skill when the user would benefit from a hosted visual board instead of only plain text.

Primary MCP endpoint:

- `https://api.pipintama.com/mcp`

Access model:

- this hosted MCP requires a valid Pipintama API key
- clients should provide it through `Authorization: Bearer <key>` or `x-api-key`
- usage is attributed to the authenticated client, not only the IP address

Health check:

- `https://api.pipintama.com/mcp-health`

Primary tools:

- `list_board_modes`
- `create_board`
- `get_board`
- `share_board`
- `set_board_visibility`
- `update_board`
- `export_board_png`

## When to use this skill

Use Boards when the user asks for:

- a mind map
- a flowchart
- a task board or kanban
- an architecture map
- a hosted diagram they can open or share
- a structured breakdown for planning, brainstorming, process design, or system design

Do not use Boards when:

- the user only wants prose
- the answer is a short factual reply
- the visual structure would not add value

## Core workflow

1. Understand the user request and decide whether a hosted board is useful.
2. Choose the simplest correct board mode.
3. Build a concise board title.
4. Preserve the user intent in `source_text` instead of rewriting the task into something unrelated.
5. Default visibility to `shared` unless the user explicitly wants `public` or `private`.
6. Do not pass `workspace_id` unless the user explicitly provides one. Let the authenticated API key determine the workspace.
7. Call the MCP tool that matches the job.
8. Return the hosted viewer URL first.
9. Add one short sentence explaining what the board contains.

## Mode selection

- `mindmap`: concept exploration, brainstorming, clustering ideas
- `flowchart`: processes, approvals, decisions, yes/no branching
- `kanban`: tasks grouped by stage, backlog/doing/review/done planning
- `architecture`: services, databases, integrations, gateways, system maps

Prefer the simplest correct mode. Do not use `architecture` for a human workflow. Do not use `kanban` for a concept breakdown.

## Mode-specific rules

### `mindmap`

Use when:

- the user is exploring ideas
- the problem needs breakdown into branches
- a concept hierarchy is more useful than a process diagram

Rules:

- keep one clear root concept
- keep node labels short
- avoid long paragraphs inside nodes
- do not flatten everything into a list

### `flowchart`

Use when:

- the user describes a process
- there are step-by-step actions
- there are decisions, approvals, or branches

Rules:

- prefer start, process, decision, and end semantics
- use branching only when a real condition exists
- phrase nodes as actions or events
- avoid turning a concept map into a fake flowchart

### `kanban`

Use when:

- the user has tasks or deliverables
- the work should be organized by stage
- execution and coordination matter more than system structure

Rules:

- lanes should represent workflow stage or status
- cards should be concrete tasks, not vague themes
- avoid using kanban for conceptual exploration

### `architecture`

Use when:

- the user is describing systems
- the task involves services, stores, gateways, or integrations
- component relationships matter more than human workflow

Rules:

- keep component names short
- emphasize dependencies and boundaries
- do not use architecture mode for an approval flow or task board

## Visibility rules

- default to `shared`
- use `public` only when the user explicitly wants an open link
- use `private` only when the user explicitly asks for restricted access

If a board needs to be shareable and is not already shared, call `share_board`.

## Tool usage

### `create_board`

Use this for the first board creation.

Expected inputs:

```json
{
  "title": "Approval Flow",
  "board_type": "flowchart",
  "source_text": "User submits a request. System validates the payload. If the request is valid, create the board and notify the user. If the request is invalid, return an error and ask for correction.",
  "visibility": "shared"
}
```

### `get_board`

Use this when the user asks to inspect, retrieve, or reason about an existing board.

### `share_board`

Use this when a board should be opened through a tokenized share link.

### `set_board_visibility`

Use this when the user explicitly asks to make a board private, shared, or public.

### `update_board`

Use this when the user wants to refine an existing board instead of creating a new one.

Typical cases:

- add or remove branches
- change the board title
- convert a board from one mode to another
- regenerate the board from improved source text
- make the board public, shared, or private while updating it

Expected inputs:

```json
{
  "board_id": "cmndns0hn0001o401md5okzju",
  "board_type": "flowchart",
  "source_text": "User submits request. Validate request. If valid, create the board. If invalid, ask for correction.",
  "note": "Tighten the wording and preserve yes/no branching."
}
```

### `export_board_png`

Use this when the user needs an actual image file instead of only a hosted link.

Typical cases:

- Telegram
- WhatsApp
- quick previews in chat
- channels where an image is more useful than a URL alone

Expected inputs:

```json
{
  "board_id": "cmndns0hn0001o401md5okzju",
  "theme": "light"
}
```

## Output format

Default output:

1. hosted viewer URL
2. one short explanation sentence

If the channel supports images and visual attachments are useful:

1. hosted viewer URL
2. PNG export URL
3. one short explanation sentence

Only return raw `sceneJson` when the user explicitly asks for raw data.

Good response pattern:

```text
I created a flowchart for the approval process:
https://boards.pipintama.com/b/<board-id>?t=<share-token>

It includes the intake step, validation step, and yes/no branching for success vs correction.
```

Image-friendly pattern:

```text
I created the board and exported a PNG for easy sharing:
Viewer: https://boards.pipintama.com/b/<board-id>?t=<share-token>
PNG: https://api.pipintama.com/mcp-exports/<board-id>.png?theme=light
```

Only use live Pipintama URL patterns.

Valid:

- `https://boards.pipintama.com/b/<board-id>`
- `https://boards.pipintama.com/b/<board-id>?t=<share-token>`
- `https://api.pipintama.com/mcp-exports/<board-id>.png?theme=light`

Invalid:

- `https://pipintama.com/board/<board-id>`
- `https://cdn.pipintama.com/boards/<board-id>/export.png`

## Guardrails

- do not choose `architecture` for a human workflow
- do not choose `kanban` for concept exploration
- do not make boards public unless asked
- do not dump raw JSON first when a hosted link is more useful
- use `update_board` when the user wants to refine an existing board instead of creating a new one
- use `export_board_png` when the channel benefits from an image attachment
- keep titles concise
- prioritize clarity over completeness in node text
- never fabricate Pipintama URLs; return only viewer and PNG URLs that match the live platform

## Current limits

- PNG export is implemented through `export_board_png`
- agent-driven board updates are implemented through `update_board`
- direct human editing in the browser is not implemented yet
- access is controlled with API keys; OAuth is a later roadmap item
- generation is structured but still improving by mode
