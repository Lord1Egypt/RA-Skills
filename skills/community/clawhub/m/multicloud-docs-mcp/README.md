<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ricardodpalmeida/multicloud-docs/main/.github/assets/banner-dark.jpg">
  <img alt="Multi-cloud Docs: cloud and AI platform answers grounded in each vendor's own docs, with sources. A search box asks for the Lambda maximum function timeout, grey answer lines end in a blue citation, and six source chips name docs.aws.amazon.com, learn.microsoft.com, docs.cloud.google.com, developers.cloudflare.com, developers.openai.com and platform.claude.com." src="https://raw.githubusercontent.com/Ricardodpalmeida/multicloud-docs/main/.github/assets/banner-light.jpg">
</picture>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT-0" src="https://img.shields.io/badge/license-MIT--0-1F5AA6?style=flat-square"></a>
  <img alt="Agent Skill" src="https://img.shields.io/badge/Agent%20Skill-SKILL.md-18191B?style=flat-square">
  <a href="https://clawhub.ai/ricardodpalmeida/skills/multicloud-docs-mcp"><img alt="On ClawHub" src="https://img.shields.io/badge/ClawHub-Multi--cloud%20Docs-6B7280?style=flat-square"></a>
  <img alt="API key only for Google" src="https://img.shields.io/badge/API%20key-only%20for%20Google-6B7280?style=flat-square">
</p>

Models answer cloud questions from training data, and service limits, SDK versions and API shapes change faster than that data. **Multi-cloud Docs** is an agent skill for official cloud and AI documentation via MCP. It grounds your agent's answers in each vendor's current documentation, through the public MCP server the vendor itself hosts, and cites the pages it used. It covers Microsoft, AWS, Google, Cloudflare, OpenAI and Anthropic with one HTTP call per lookup, no saved configuration and no API key, except for Google.

This answer comes from a real run, where the agent was asked for the maximum timeout of an AWS Lambda function and picked the skill up by itself:

```
Answer:   The standard AWS Lambda function timeout limit is 900 seconds (15 minutes).
          Exception: Lambda Managed Instances supports 5,400 seconds (90 minutes) for
          asynchronous invocations and event source mapping invocations, except
          Amazon MQ and Amazon DocumentDB.
Sources:  AWS documentation: Configure Lambda function timeout
          https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html
Status:   The cited page does not label these limits as preview.
Gaps:     None for the documented timeout limits.
```

## Quick navigation

[How it works](#how-it-works) · [Install](#install) · [Server access](#connect-the-servers) · [Package contents](#what-is-inside) · [Release notes](CHANGELOG.md)

## How it works

1. The agent picks the vendor the question is about and searches that vendor's documentation, putting the product, feature and version or tier in the query.
2. It reads a full page only when the search excerpts miss the evidence it needs, three pages per vendor at most, and pulls the passage it needs out of long pages.
3. It prefers product documentation over Q&A, blog and forum items, and never answers one vendor's question from another vendor's documentation.
4. It answers in four parts: the answer, the pages used, preview status and what the documentation does not cover.

General programming questions need no lookup, so the skill stays out of them. Queries stay generic, without secrets, account or customer identifiers or proprietary code. Retrieved text counts as evidence, never as instructions, and a rate limit or repeated timeouts stop the lookup.

| Vendor | Server | Search | Read |
| --- | --- | --- | --- |
| Microsoft (Azure, .NET, Microsoft 365, Entra) | `learn.microsoft.com/api/mcp` | `microsoft_docs_search`, `microsoft_code_sample_search` | `microsoft_docs_fetch` |
| AWS | `knowledge-mcp.global.api.aws` | `aws___search_documentation` | `aws___read_documentation` |
| Google (Cloud, Firebase, Android, Gemini API) | `developerknowledge.googleapis.com/mcp` | `search_documents` | `get_documents` |
| Cloudflare | `docs.mcp.cloudflare.com/mcp` | `search_cloudflare_documentation` | results carry the text |
| OpenAI | `developers.openai.com/mcp` | `search_openai_docs` | `fetch_openai_doc` |
| Anthropic (Claude API) | `platform.claude.com/docs/mcp` | `search_docs` | `get_doc` |

Google's server needs an API key from a Google Cloud project with the Developer Knowledge API enabled. Without a key the skill reads `docs.cloud.google.com` with the agent's ordinary web tools and says so. It does the same for vendors that publish no documentation server, such as Oracle and IBM.

## Install

The folder follows the Agent Skills format and works with compatible agents.

For OpenClaw:

```bash
openclaw skills install @ricardodpalmeida/multicloud-docs-mcp            # this workspace
openclaw skills install @ricardodpalmeida/multicloud-docs-mcp --global   # all agents
```

For agents that read `SKILL.md` directly, clone it into the agent's skills folder under the skill's name. For example, with Claude Code:

```bash
git clone https://github.com/Ricardodpalmeida/multicloud-docs ~/.claude/skills/multicloud-docs-mcp
```

Use `~/.codex/skills/multicloud-docs-mcp` for Codex or `~/.copilot/skills/multicloud-docs-mcp` for GitHub Copilot.

## Connect the servers

Nothing has to be connected. Each lookup is one stateless request with `curl`, so the skill works as soon as it is installed:

```bash
curl -sS -m 30 -X POST "https://knowledge-mcp.global.api.aws" \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"aws___search_documentation","arguments":{"search_phrase":"Lambda maximum function timeout","limit":3}}}' | head -c 12000
```

When your agent already has one of these servers connected, the skill uses the connected tools first. [references/setup.md](references/setup.md) covers optional native registration in OpenClaw, the Google key, vendor notes and recovery.

Queries and the documentation URLs you request are sent to the vendor whose server you call, so leave sensitive information out.

## What is inside

```
SKILL.md              vendors, tools, the single-request access path, how to search, read and cite
references/setup.md   vendor notes, Google key, optional OpenClaw registration, recovery
CHANGELOG.md          release notes
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
| [Microsoft Learn MCP](https://github.com/Ricardodpalmeida/openclaw-mslearn-mcp) | Ground Microsoft answers in current Learn docs and code samples |
| [LadybugDB openCypher](https://clawhub.ai/ricardodpalmeida/skills/ladybug-opencypher-updated) | Work with LadybugDB property graphs using openCypher and Python |
