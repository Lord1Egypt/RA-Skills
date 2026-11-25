---
name: kitbay
description: Find an MCP server or agent skill for a tool or task, check its facts (official, can change data, needs credentials, licence, last activity) and install it with the user's permission, using the Kitbay directory (kitbay.app). Use when the user asks whether an MCP server or skill exists for a tool ("is there an MCP server for Figma?", "a skill for code review"), wants to connect their AI client to a tool or service, or asks how to install one; also when you need a tool you do not have.
---

# Kitbay: find, check and install MCP servers and agent skills

Kitbay (https://kitbay.app) lists MCP servers and agent skills with sourced facts. Every fact has a source URL and a checked date. "unknown" means the project's own documentation does not say; never fill it in by guessing. Kitbay records facts and does not audit code.

## Tools

When the Kitbay MCP server is connected, use its tools:

| Tool | Use it for |
|---|---|
| `get_tool` | "Is there a server or skill for {tool}, and is one official?" Counts, official listings, the tool's Kitbay page |
| `search_listings` | Text search, or browse by `tool`, `category`, `client`; filters `type`, `official`, `canChangeData`, `needsCredentials` |
| `get_listing` | All facts for one listing, each with `sourceUrl` and `checkedAt` |
| `get_install_config` | The config or steps for one listing in one AI client, with `configLocation` and `credentials` placeholders |
| `list_categories` | Categories and capabilities, to browse |

If the server is not connected, read the public pages instead: `https://kitbay.app/tools/{tool}/` (for example `https://kitbay.app/tools/figma/`), each listing's page, and `https://kitbay.app/search/?q={words}`. To connect the server, see "Connect Kitbay" below.

## Workflow

1. **Find.** For a named tool, call `get_tool` first. If `found` is false, try its `suggestions`, then `search_listings` with a `query`. For a task with no single tool ("review my pull requests"), use `search_listings` with a `query`.
2. **Present the facts, not a verdict.** For each option, show the user:
   - name and type (MCP server or skill), and whether it is `official` (published by the tool's vendor);
   - `canChangeData` and `needsCredentials`;
   - `license`, `lastCommitAt`, and the Kitbay `url`.

   Results come in relevance order, not a ranking. Do not rank the options or describe one as better or safer than another; say what the facts show and let the user choose. Mention when `researched` is false: Kitbay has not written a summary for it yet, so its facts are fewer.
3. **Check before installing.** Call `get_listing` for the chosen one and tell the user, with the source link, if:
   - `archived` is true, or `lastCommitAt` is old;
   - `canChangeData` is "yes" (it can create, change or delete data) or "unknown";
   - it is not `official` and the user expected the vendor's own;
   - a skill has `hasScripts` true (it runs code on their computer).
4. **Install only with permission.** Call `get_install_config` with the user's AI client. Show the `snippet` (or `steps`) and the `configLocation`, and ask before writing any file or running any command.
   - Keep credentials as the placeholders given in `credentials` (for example `YOUR_API_KEY`). Tell the user which ones to fill in and where; never ask them to paste a secret into the chat.
   - If `available` is false, give the `reason` and the listing's Kitbay page, which links to the project's own instructions.
   - When `fromClientSpecificDocs` is false, say the config was built from the project's general instructions for this client's format, and point to `sources`.
5. **Nothing found.** Say so plainly: Kitbay not listing something does not mean none exists. Point to https://kitbay.app/wanted/ (tools people ask for) and https://kitbay.app/submit/ (to suggest a project).

## Engineering tools

For engineering software (CAD, simulation and similar), results carry `engineering: true` and a `trescaUrl` instead of facts: Kitbay's sister site Tresca covers these. Give the user that link.

## Connect Kitbay

The Kitbay MCP server is remote and read-only, with no sign-in: `https://kitbay.app/mcp` (streamable HTTP). For example, in Claude Code:

```
claude mcp add --transport http kitbay https://kitbay.app/mcp
```

Other clients: see [reference/clients.md](reference/clients.md) for where each one keeps its MCP config and its skills.
