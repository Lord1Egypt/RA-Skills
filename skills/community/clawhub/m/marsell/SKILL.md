---
name: marsell
description: Work with Marsell, an AI for marketing, sales and content creation, through its MCP server. Use when someone wants to run their Marsell projects from their own AI (see what Marsell planned, made and found, answer the decisions waiting for them, update their brand, plan work, make pictures and films, or check results), or asks what Marsell does and how to connect it.
license: MIT
metadata:
  author: marsell
  version: "1.0.0"
  homepage: https://getmarsell.com
---

# Marsell

Marsell is an AI for marketing, sales and content creation. For each business, called a project, it plans the month, makes the posts, pictures and films, publishes to the accounts the owner connects, finds customers and talks to them, and measures what worked. Anyone can sign up at https://getmarsell.com.

## Connect

Add Marsell's remote MCP server: `https://getmarsell.com/mcp` (Streamable HTTP).

- **OAuth:** choose OAuth, sign in to Marsell, and review the permissions before pressing **Allow**.
- **Agent key:** the owner makes one in Marsell under a project's **Agents → Your own AI**, choosing **Reads only** or **Can act**. Keep it in the client's secure credential settings, never in a file or a chat.

Full guide: https://docs.getmarsell.com/developers/mcp

## How to work with it

- Start with `list_projects` when there are several, then `get_app` for the project's map: every place, every agent, and what waits for the owner. `get_overview` says where the project stands today.
- Before saying what a card, a message or a page says, read it whole: `card_read`, `inbox_read`, `site_draft_read`.
- Write in the brand's own voice. Read it first with `get_brand`.
- A tool that spends tokens says so. Tell the user what it costs and go ahead only on their yes.
- Use `answer_decision` only for what the user asked you to answer: it answers in the owner's name.

## Constraints

- Use only the tools the server lists. Don't invent others. There is no public REST API.
- Without the owner's sign-in or agent key, an agent can't act in anyone's projects.
- Every project needs a Marsell plan before Marsell reads pages or makes anything.
- Marsell learns each kind of work from the owner's first answers, then runs it on its own within limits, each item with an undo window. Money, deals, replies in strangers' threads and changes to live pages always ask the owner.
- "Tokens" are Marsell's unit of AI and media work, granted monthly by the plan. They are not model tokens.
- Prices come only from https://docs.getmarsell.com/account/plans-and-tokens. Don't quote them from anywhere else.

## Help

- Docs: https://docs.getmarsell.com. Add `.md` to any page's address to read it as Markdown.
- Support: hello@getmarsell.com
- Security: security@getmarsell.com
