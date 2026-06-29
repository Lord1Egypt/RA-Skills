---
name: post-on-discord-channel
description: "Post On Discord Channel: Send messages to Discord channels via webhooks with markdown, embeds, file attachments, and mention controls. Use when an agent needs post on discord channel, update community when new products features drop, notify channel followers of upcoming events, notify users of support ticket requests, integrate with content publishing pipeline, send, webhook url, content through AgentPMT-hosted remote tool calls. Discovery terms: post on discord channel."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/post-on-discord-channel
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/post-on-discord-channel"}}
---
# Post On Discord Channel

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
The Discord Webhook Tool enables AI agents to send rich, formatted messages directly to Discord channels through webhook URLs. It supports text messages with full Discord markdown formatting, custom username and avatar overrides, and rich embeds with titles, descriptions, fields, colors, images, and timestamps. The tool can upload up to 10 files per message with base64 encoding and reference them within embeds using the attachment:// syntax for seamless image display. Advanced features include mention controls to manage user/role pings, text-to-speech capabilities, and support for multiple embeds (up to 10) in a single message for complex notifications. Perfect for automation workflows, monitoring systems, chatbot integrations, and notification pipelines requiring formatted Discord output.

## Product Instructions
### Post On Discord Channel - Instructions

#### Overview

Send messages, rich embeds, and file attachments to Discord channels via webhooks. Supports text messages with Discord markdown, up to 10 rich embeds per message, up to 10 file attachments, custom bot identity (username/avatar), text-to-speech, and mention controls.

#### Actions

##### send

Post a message to a Discord channel using a webhook URL. At least one of `content`, `embeds`, or `files` must be provided.

**Required Fields:**
- `action` — Set to `"send"`
- `webhook_url` — Discord webhook URL in the format `https://discord.com/api/webhooks/{webhook_id}/{webhook_token}`

**Optional Fields:**
- `content` (string, max 2000 chars) — Message text. Supports Discord markdown formatting.
- `username` (string, max 80 chars) — Override the default webhook display name.
- `avatar_url` (string) — Override the default webhook avatar with a custom image URL.
- `tts` (boolean, default false) — Enable text-to-speech for the message.
- `embeds` (array, max 10) — Array of rich embed objects (see Embed Structure below).
- `files` (array, max 10) — Array of file attachment objects (see File Structure below).
- `allowed_mentions` (object) — Controls which mentions can ping users/roles (see Mention Controls below).

###### Embed Structure

Each embed object supports:
- `title` (string, max 256 chars) — Embed title.
- `description` (string, max 4096 chars) — Embed body text. Supports Discord markdown.
- `url` (string) — URL the title links to.
- `color` (integer) — Color as decimal integer. Example: Blue = 39423, Red = 16711680, Green = 65280.
- `author` (object) — Author block with required `name`, optional `url` and `icon_url`.
- `fields` (array, max 25) — Field objects with required `name` and `value` (max 256/1024 chars), optional `inline` (boolean).
- `thumbnail` (object) — Thumbnail image (top-right corner) with required `url`.
- `image` (object) — Large image below content with required `url`.
- `footer` (object) — Footer with required `text` (max 2048 chars, no markdown), optional `icon_url`.
- `timestamp` (string) — ISO 8601 timestamp displayed in the footer, e.g. `"2026-03-09T12:00:00Z"`.

###### File Structure

Each file object requires:
- `filename` (string) — File name with extension, e.g. `"report.pdf"`.
- `content` (string) — Base64-encoded file content.
- `description` (string, optional) — Description of the attachment.

###### Mention Controls

The `allowed_mentions` object controls pings:
- `parse` (array) — Allowed mention types: `"roles"`, `"users"`, `"everyone"`.
- `roles` (array) — Specific role IDs allowed to be mentioned.
- `users` (array) — Specific user IDs allowed to be mentioned.

---

#### Examples

##### Simple Text Message

```json
{
  "action": "send",
  "webhook_url": "https://discord.com/api/webhooks/123456789/abcdef",
  "content": "Hello from the bot!"
}
```

##### Custom Bot Identity

```json
{
  "action": "send",
  "webhook_url": "https://discord.com/api/webhooks/123456789/abcdef",
  "content": "Status update: all systems operational.",
  "username": "Status Bot",
  "avatar_url": "https://example.com/bot-avatar.png"
}
```

##### Rich Embed with Fields

```json
{
  "action": "send",
  "webhook_url": "https://discord.com/api/webhooks/123456789/abcdef",
  "embeds": [
    {
      "title": "Daily Sales Report",
      "description": "Summary for March 9, 2026",
      "color": 39423,
      "fields": [
        { "name": "Total Revenue", "value": "$12,450", "inline": true },
        { "name": "Orders", "value": "87", "inline": true },
        { "name": "Top Product", "value": "Widget Pro", "inline": false }
      ],
      "footer": { "text": "Generated automatically" },
      "timestamp": "2026-03-09T17:00:00Z"
    }
  ]
}
```

##### Embed with Image and Author

```json
{
  "action": "send",
  "webhook_url": "https://discord.com/api/webhooks/123456789/abcdef",
  "embeds": [
    {
      "title": "New Blog Post Published",
      "url": "https://example.com/blog/new-post",
      "description": "Check out our latest article on automation best practices.",
      "color": 65280,
      "author": {
        "name": "Content Team",
        "icon_url": "https://example.com/team-icon.png"
      },
      "image": { "url": "https://example.com/blog-banner.png" },
      "thumbnail": { "url": "https://example.com/logo-small.png" }
    }
  ]
}
```

##### File Attachment

```json
{
  "action": "send",
  "webhook_url": "https://discord.com/api/webhooks/123456789/abcdef",
  "content": "Here is the report you requested.",
  "files": [
    {
      "filename": "report.csv",
      "content": "bmFtZSxhZ2UKSm9obiwyNQpKYW5lLDMw",
      "description": "Monthly sales data"
    }
  ]
}
```

##### Message with Mention Controls

```json
{
  "action": "send",
  "webhook_url": "https://discord.com/api/webhooks/123456789/abcdef",
  "content": "Attention @everyone: server maintenance at 10 PM.",
  "allowed_mentions": {
    "parse": ["everyone"]
  }
}
```

---

#### Common Workflows

1. **Automated Notifications** — Send alerts from monitoring systems, CI/CD pipelines, or scheduled tasks to a Discord channel using a simple text message.
2. **Formatted Reports** — Use embeds with fields, colors, and timestamps to deliver structured data like daily summaries, analytics, or dashboards.
3. **File Delivery** — Attach generated reports (CSV, PDF, images) directly to Discord messages using base64-encoded file content.
4. **Multi-Channel Broadcasting** — Send the same message to multiple channels by calling the tool once per webhook URL.

#### Important Notes

- You must provide at least one of `content`, `embeds`, or `files` in every send request.
- The `webhook_url` must match the Discord webhook URL pattern. You can create webhooks in Discord under Channel Settings > Integrations > Webhooks.
- Embed colors must be decimal integers, not hex strings. Convert hex to decimal (e.g., 0x0099FF = 39423).
- File content must be valid base64-encoded data.
- Discord limits: 2000 characters for content, 10 embeds per message, 25 fields per embed, 10 files per message.
- The `tts` (text-to-speech) option will cause the message to be read aloud to users in the channel.

## When To Use
- Use this skill for `Post On Discord Channel` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: post on discord channel, update community when new products features drop, notify channel followers of upcoming events, notify users of support ticket requests, integrate with content publishing pipeline, send, webhook url, content.
- Supported action names: `send`.

## Use Cases
- Update community when new products features drop
- notify channel followers of upcoming events
- notify users of support ticket requests
- integrate with content publishing pipeline

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `send` (action slug: `send`): Send a message to a Discord channel via webhook. Supports text content with Discord markdown, rich embeds, file attachments, custom bot identity, text-to-speech, and mention controls. At least one of content, embeds, or files must be provided. Price: `3` credits. Parameters: `allowed_mentions`, `avatar_url`, `content`, `embeds`, `files`, `tts`, `username`, `webhook_url`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "post-on-discord-channel"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "post-on-discord-channel"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "post-on-discord-channel"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "post-on-discord-channel"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "post-on-discord-channel"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "post-on-discord-channel"
  }
}
```

## Call This Tool
Product slug: `post-on-discord-channel`

Marketplace page: https://www.agentpmt.com/marketplace/post-on-discord-channel

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Post-On-Discord-Channel",
    "arguments": {
      "action": "send",
      "allowed_mentions": {
        "parse": [
          "roles"
        ],
        "roles": [
          "example role"
        ],
        "users": [
          "example user"
        ]
      },
      "avatar_url": "https://example.com",
      "content": "Draft marketing copy to check for banned phrases.",
      "embeds": [
        {
          "author": {
            "icon_url": "https://example.com",
            "name": "example name",
            "url": "https://example.com"
          },
          "color": 1,
          "description": "example description",
          "fields": [
            {
              "inline": false,
              "name": "example name",
              "value": "example value"
            }
          ],
          "footer": {
            "icon_url": "https://example.com",
            "text": "example text"
          },
          "image": {
            "url": "https://example.com"
          },
          "thumbnail": {
            "url": "https://example.com"
          },
          "timestamp": "example timestamp"
        }
      ],
      "files": [
        {
          "content": "Draft marketing copy to check for banned phrases.",
          "description": "example description",
          "filename": "example filename"
        }
      ],
      "tts": false,
      "username": "example username",
      "webhook_url": "https://example.com"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "post-on-discord-channel",
  "parameters": {
    "action": "send",
    "allowed_mentions": {
      "parse": [
        "roles"
      ],
      "roles": [
        "example role"
      ],
      "users": [
        "example user"
      ]
    },
    "avatar_url": "https://example.com",
    "content": "Draft marketing copy to check for banned phrases.",
    "embeds": [
      {
        "author": {
          "icon_url": "https://example.com",
          "name": "example name",
          "url": "https://example.com"
        },
        "color": 1,
        "description": "example description",
        "fields": [
          {
            "inline": false,
            "name": "example name",
            "value": "example value"
          }
        ],
        "footer": {
          "icon_url": "https://example.com",
          "text": "example text"
        },
        "image": {
          "url": "https://example.com"
        },
        "thumbnail": {
          "url": "https://example.com"
        },
        "timestamp": "example timestamp"
      }
    ],
    "files": [
      {
        "content": "Draft marketing copy to check for banned phrases.",
        "description": "example description",
        "filename": "example filename"
      }
    ],
    "tts": false,
    "username": "example username",
    "webhook_url": "https://example.com"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `send` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/post-on-discord-channel
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
