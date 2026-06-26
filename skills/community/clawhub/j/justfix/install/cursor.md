# Installing JustFix Skill on Cursor

[Cursor](https://cursor.com) is an AI-powered code editor with MCP support.

## Step 1: Register the MCP server

Open Cursor → Settings → Features → Model Context Protocol → Add new MCP server.

| Field | Value |
|---|---|
| Name | `justfix-estimator` |
| Type | `Streamable HTTP` |
| URL | `https://estimator-mcp.justfix.app/mcp` |

Click Save. Cursor will validate the connection and list the three available tools.

## Step 2: Drop the skill into your Cursor rules

Cursor's "Rules" feature is the closest equivalent to AgentSkills. Add the SKILL.md content as a project or user rule:

1. Cursor → Settings → Rules → Add new rule
2. Paste the content of [SKILL.md](../SKILL.md) into the rule body
3. Mark it as **always active** (or set the trigger to "quote, estimate, price, trades, plumbing, electrical")

Alternatively, save SKILL.md to your project as `.cursor/rules/justfix.md` and Cursor will load it automatically.

## Step 3: Verify

In a Cursor chat session, ask:

> How much for a locksmith to come and change my front door lock?

Cursor should invoke the `service-estimate-card` tool with `service_code=locksmith` and return a quote.

## Why use this in Cursor?

You probably won't book a plumber from your IDE. But:

- **Demo/test the JustFix MCP** while developing integrations
- **Build customer-facing experiences** that wrap JustFix pricing into your own product – test the MCP responses in Cursor before shipping
- **API documentation by example** – the skill teaches your AI assistant the right service codes and defaults

## Notes

- Cursor supports MCP over HTTP and stdio. The JustFix MCP is HTTP-only.
- No auth required.
- The booking URL is rendered as a clickable link in the Cursor chat panel.
