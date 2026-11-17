---
name: markdown-convert
description: Convert Markdown to Slack mrkdwn, Teams HTML, Jira ADF, or plain text via the markdown-convert MCP server. Use when the agent will post or paste into Slack, Microsoft Teams, Jira Cloud, or needs stripped text for another channel.
version: 1.2.0
---

# Markdown Convert MCP

This skill points agents at the **markdown-convert** MCP server (`@ysskrishna/markdown-convert-mcp`). The server is convert-only: it does not post messages or create issues.

## When to use which tool

| Tool | Output | Choose when |
|------|--------|-------------|
| `markdown_to_slack` | Slack mrkdwn | The next hop is Slack API, Slack MCP `text`, or another mrkdwn field |
| `markdown_to_teams` | HTML with inline CSS | Teams paste, Graph `contentType: html`, or rich HTML paste targets |
| `markdown_to_jira` | ADF JSON string | Jira Cloud REST v3 / Atlassian MCP rich-text fields |
| `markdown_to_plaintext` | Plain text | Any destination that should not receive Markdown syntax |

Each tool accepts `{ "markdown": "<source>" }`. Input over 200,000 characters returns a tool error (`isError: true`).

## Do not use

- `markdown_to_slack` for Composer clipboard paste or fields that expect raw Markdown.
- `markdown_to_teams` for Adaptive Cards or when you need this server to send Teams messages.
- `markdown_to_jira` for wiki markup or Jira Server v2 APIs.

Full tool matrix: [README — Tools and next hops](https://github.com/ysskrishna/markdown-convert-mcp#tools-and-next-hops).