---
name: karakeep-mcp-first
description: Unofficial MCP-first skill for using Karakeep with AI agents. Use it to save, search, organize, tag, list, summarize, and highlight Karakeep bookmarks through MCP first, with CLI/API fallback only when needed.
metadata:
  tags: bookmarks, bookmark manager, mcp, ai agents, productivity
  openclaw:
    envVars:
      - name: KARAKEEP_API_KEY
        required: true
        description: The API key for your Karakeep instance.
      - name: KARAKEEP_SERVER_ADDR
        required: false
        description: The server address for your Karakeep instance.
    requires:
      env:
        - KARAKEEP_API_KEY
        - KARAKEEP_SERVER_ADDR
      bins:
        - karakeep
    primaryEnv: KARAKEEP_API_KEY
    homepage: https://github.com/thethomasjfellows/karakeep-mcp-first-skill
    links:
      github: https://github.com/thethomasjfellows/karakeep-mcp-first-skill
      video: https://youtu.be/WQNhRyYyl64
      karakeep: https://karakeep.app
      docs: https://docs.karakeep.app
    cliHelp: karakeep --help
    install:
      - kind: node
        package: "@karakeep/cli"
        bins: [karakeep]
---

# Karakeep MCP-First

An unofficial Karakeep skill for AI agents that prefers MCP for normal work and keeps CLI/API fallback available for the edge cases MCP does not handle yet.

Use this skill when the user wants an agent to work with their Karakeep bookmarks: save links, search saved content, organize lists, apply tags, clean up duplicates, summarize research, or create meaningful highlights.

Video walkthrough: https://youtu.be/WQNhRyYyl64

## What It Does

- Uses Karakeep MCP first for normal bookmark, list, tag, and content workflows.
- Falls back to the Karakeep CLI only for unavailable MCP features, bulk work, debugging, migrations, dumps, or raw JSON verification.
- Uses the Karakeep API directly only when MCP and CLI do not expose the needed operation.
- Keeps highlights intentional instead of spraying annotations everywhere.
- Helps turn Karakeep from a passive bookmark manager into an AI-usable research and workflow system.

## Quick Setup

1. Run Karakeep and create an API key.
2. Configure the official Karakeep MCP server in your agent.
3. Install the optional CLI fallback if you want it:

```bash
npm install -g @karakeep/cli
```

4. Set your Karakeep environment variables:

```bash
export KARAKEEP_API_KEY="your-api-key"
export KARAKEEP_SERVER_ADDR="https://your-karakeep.example.com"
```

5. Restart your agent session and ask it to use `karakeep-mcp-first`.

## Tool Priority

Use tools in this order:

1. Karakeep MCP for normal work.
2. Karakeep CLI for fallback, debugging, bulk import/export, migrations, dumps, or raw JSON verification.
3. Karakeep API for unsupported operations, especially highlight creation.
4. Browser/manual workaround only when the other options are insufficient.

If you do not use MCP, briefly explain why.

## MCP Tools

Prefer MCP for:

- `search-bookmarks`
- `get-bookmark`
- `create-bookmark`
- `update-bookmark`
- `get-bookmark-content`
- `get-lists`
- `create-list`
- `add-bookmark-to-list`
- `remove-bookmark-from-list`
- `attach-tag-to-bookmark`
- `detach-tag-from-bookmark`

Do not verify with CLI unless there is a clear reason.

## Agent Behavior

- Search before creating when duplicate bookmarks might matter.
- Use lists for durable collections, projects, source libraries, and workflows.
- Use tags for reusable labels across lists.
- Reuse existing tags when possible and avoid near-duplicates such as `ai-tools`, `aitools`, and `ai tool`.
- Prefer lowercase tags such as `ai`, `research`, `reference`, `todo`, `read-later`, `dev`, `business`, `video`, or project-specific tags.
- Confirm before destructive deletes, broad archive operations, or large cleanup sweeps.
- Avoid printing API keys or local secrets.

## Meaningful Highlights

Do not create highlights by default. Create highlights only when they preserve the exact part of the content the user cares about.

Good reasons to highlight:

- Ingredients, steps, commands, requirements, definitions, warnings, compatibility notes, pricing, conclusions, or key evidence.
- One obvious passage that is basically the reason to save the bookmark.

Highlighting rules:

- Highlight the smallest useful passage.
- Prefer 1-3 highlights unless the user asks for more.
- Add a concrete note such as `Ingredients requested by the user` or `Core compatibility requirement`.
- Do not highlight text that is not present in the saved content.

MCP does not currently expose highlight creation. When highlighting is warranted, use MCP to retrieve the bookmark/content, then use the Karakeep API to create the highlight and explain that API fallback was used.

## CLI Fallback

Use the CLI only when MCP is unavailable, incomplete, or the task needs bulk/debug/raw JSON behavior.

Useful fallback commands:

```bash
karakeep whoami --json
karakeep bookmarks search "is:fav #work" --json
karakeep bookmarks get <bookmark-id> --include-content --json
karakeep dump --help
karakeep migrate --help
karakeep wipe --help
```

## More Detail

For search syntax, bookmark/list/tag concepts, and expanded workflow examples, read `references/karakeep-details.md` when needed. Do not load it unless the task needs those details.
