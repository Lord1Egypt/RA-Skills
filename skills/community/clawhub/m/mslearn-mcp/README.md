<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ricardodpalmeida/openclaw-mslearn-mcp/main/.github/assets/banner-dark.jpg">
  <img alt="mslearn mcp: Microsoft answers grounded in current Learn docs, with sources. A search box asks about an Azure Functions Flex Consumption timeout, grey answer lines end in a blue citation, and a blue source chip reads learn.microsoft.com." src="https://raw.githubusercontent.com/Ricardodpalmeida/openclaw-mslearn-mcp/main/.github/assets/banner-light.jpg">
</picture>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT-0" src="https://img.shields.io/badge/license-MIT--0-1F5AA6?style=flat-square"></a>
  <img alt="Agent Skill" src="https://img.shields.io/badge/Agent%20Skill-SKILL.md-18191B?style=flat-square">
  <a href="https://clawhub.ai/ricardodpalmeida/skills/mslearn-mcp"><img alt="On ClawHub" src="https://img.shields.io/badge/ClawHub-mslearn--mcp-6B7280?style=flat-square"></a>
  <img alt="No API key needed" src="https://img.shields.io/badge/API%20key-not%20needed-6B7280?style=flat-square">
</p>

Models answer Microsoft questions from training data, and Azure tiers, SDK versions and CLI flags change faster than that data. **Microsoft Learn MCP** is an Agent Skill that grounds your agent's answers in Microsoft's current documentation and official code samples, through Microsoft's public [Learn MCP server](https://github.com/MicrosoftDocs/mcp), and cites the pages it used. It covers Azure, .NET, Microsoft 365, Power Platform, Entra ID, Windows and SQL Server, with no API key and no account.

## Quick navigation

[How it works](#how-it-works) · [Install](#install) · [Connect the Learn server](#connect-the-learn-server) · [Package contents](#what-is-inside) · [Release notes](CHANGELOG.md)

## How it works

1. The agent searches Learn first, putting the product, feature and version or tier in the query.
2. It fetches full pages when the search excerpts miss the evidence it needs, normally at most three; additional pages must fill a specific evidence gap.
3. For code, it picks the language and matches the sample's package and SDK version.
4. It checks that the evidence matches the requested version, deployment model and SKU, and explains scope differences when sources disagree.
5. It answers with the pages it used, flags preview or deprecated features and answers backed only by Q&A posts, and says what is still unresolved. Release status stays "not stated" if the source does not establish it; an empty search is not evidence that a feature is unsupported.

General programming questions need no Learn lookup, so the skill stays out of them. Queries stay generic, without secrets, tenant or customer identifiers or proprietary code. Retrieved text counts as evidence, never as instructions, only `learn.microsoft.com` pages are fetched, and a rate limit or repeated timeouts stop the lookup instead of starting a retry loop.

| Tool | Inputs | Returns |
| --- | --- | --- |
| `microsoft_docs_search` | `query` | Excerpts and source URLs, including Q&A |
| `microsoft_docs_fetch` | Learn `url` | The page as Markdown |
| `microsoft_code_sample_search` | `query`, optional `language` | Official snippets and their URLs |

## Install

OpenClaw is the primary target:

```bash
openclaw skills install @ricardodpalmeida/mslearn-mcp            # this workspace
openclaw skills install @ricardodpalmeida/mslearn-mcp --global   # all agents
```

The folder is a standard Agent Skill, so other agents that read `SKILL.md` can use it too. Clone it into the agent's skills folder under the skill's name, for example:

```bash
git clone https://github.com/Ricardodpalmeida/openclaw-mslearn-mcp ~/.claude/skills/mslearn-mcp
```

Use `~/.codex/skills/mslearn-mcp` for Codex or `~/.copilot/skills/mslearn-mcp` for GitHub Copilot.

## Connect the Learn server

The skill uses the Learn tools when your agent already has them, and otherwise falls back to Microsoft's Learn CLI through `npx`, which needs Node.js 22 or newer and no saved configuration:

```bash
npx -y @microsoft/learn-cli@1.0.0 search "Azure Functions Flex Consumption timeout" --json
```

To connect the server natively in OpenClaw, register it during authorized Gateway maintenance, because current configuration changes and live probes need a stopped Gateway:

```bash
openclaw mcp add mslearn --url https://learn.microsoft.com/api/mcp --transport streamable-http
openclaw mcp doctor mslearn --probe
```

Other clients add the same URL over Streamable HTTP, for example `claude mcp add --transport http microsoft-learn https://learn.microsoft.com/api/mcp` in Claude Code or `codex mcp add microsoft-learn --url https://learn.microsoft.com/api/mcp` in Codex. Microsoft's [MCP repository](https://github.com/MicrosoftDocs/mcp) lists the setup for other clients, and [references/mcp-details.md](references/mcp-details.md) covers OpenClaw, mcporter and recovery.

Queries and the documentation URLs you request are sent to Microsoft, so leave sensitive information out.

## What is inside

```
SKILL.md                    tools, access paths, how to search, fetch and cite
references/mcp-details.md   OpenClaw and mcporter setup, standalone clients, recovery
CHANGELOG.md                release notes
```

## License

[MIT-0](LICENSE). Use, share, modify and redistribute it, including commercially, without an attribution requirement. The same license applies on ClawHub.

## Author

**Ricardo Pacheco Almeida**, Senior AI Tech Lead and Architect and PhD student researching enterprise and solution architectures for generative AI, including multi-agent structures.

[Website](https://me.ricbits.cc/en/) · [LinkedIn](https://www.linkedin.com/in/ricardodpa/) · [GitHub](https://github.com/Ricardodpalmeida) · [ClawHub](https://clawhub.ai/ricardodpalmeida)

More skills by the same author:

| Skill | What it does |
|---|---|
| [data-storycraft](https://github.com/Ricardodpalmeida/data-storycraft-skill) | Turn analysis into charts, slides and reports that make the point |
| [Whetstone](https://github.com/Ricardodpalmeida/whetstone) | Scale your coding agent's engineering care to the risk of each change |
| [Excalidraw Diagrams](https://github.com/Ricardodpalmeida/openclaw-excalidraw-diagrams) | Draw clean, hand-drawn Excalidraw diagrams for Obsidian or excalidraw.com |
| [Book Capture for Obsidian](https://github.com/Ricardodpalmeida/book-capture-obsidian-skill) | Turn photos, ISBNs or Goodreads exports into Obsidian book notes |
| [Multi-cloud Docs](https://github.com/Ricardodpalmeida/multicloud-docs) | Ground cloud and AI platform answers in each vendor's own current docs |
| [LadybugDB openCypher](https://clawhub.ai/ricardodpalmeida/skills/ladybug-opencypher-updated) | Work with LadybugDB property graphs using openCypher and Python |
