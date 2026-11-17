# Features

Everything the PosteAhora CLI can do — a command-line interface to the
[PosteAhora](https://posteahora.com) social media scheduling and publishing API.

## Publishing

- **Publish now** to one or many channels with a single command.
- **Schedule** posts for any future date/time (ISO 8601).
- **Drafts** — stage a post without publishing.
- **Multi-platform fan-out** — one post, every connected network.
- **Per-platform captions** and options (e.g. shorter text for X, TikTok drafts).
- **Post types** — feed post, reel, or story where the platform supports it.
- **Hashtags** and titles.

## Media

- **Upload images and video** via presigned URLs (`posteahora upload`).
- **Attach media** to any post with `--media` (repeatable for carousels).
- Works for large video files, not just images.

## Content management

- **Ideas backlog** — capture, tag, and list content ideas before they become posts.
- **List and filter posts** by status (draft, scheduled, queued, published, failed).

## Analytics

- **Cross-platform metrics** — views, likes, comments, shares, reach, saves,
  impressions, and more.
- **Time windows** — 7d, 30d, 90d, or all time.
- **Per-platform breakdown**.

## Built for automation & AI agents

- **`--json` output** on most commands for scripting and agents.
- **Env-var auth** (`POSTEAHORA_API_KEY`) for CI pipelines.
- **Clear, actionable errors** and exit codes.
- **Zero runtime dependencies** — native `fetch`, fast install.

## Same power, three surfaces

The CLI is one of three ways to automate PosteAhora over the same REST API:

- **CLI** — this tool (`@posteahora/cli`).
- **MCP server** — [`@posteahora/mcp`](https://github.com/posteahora/mcp) for AI
  agents (Claude, Cursor, ChatGPT, Windsurf).
- **REST API** — [posteahora.com/docs/api](https://posteahora.com/docs/api).
