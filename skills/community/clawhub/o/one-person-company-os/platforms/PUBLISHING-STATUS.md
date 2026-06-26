# Publishing Status

Updated: 2026-05-06

This is the canonical push list for One Person Company OS `1.0.3`.

Status vocabulary:

- `published`: the platform page, version API, downloadable package, or review record proves the release is live.
- `ready-to-submit`: the local submission package exists, but platform account, browser flow, API key, or review is still required.
- `backend-needed`: the platform requires a hosted API, extension runtime, webhook, or MCP bridge before marketplace submission.
- `tenant-needed`: the platform requires an organization tenant, admin approval, or enterprise marketplace account.

| Mainstream channel | Status | Version | Local package | Evidence now | Blocker | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| OpenClaw / ClawHub | published | 1.0.3 | repository root | ClawHub API latest is `1.0.3`; download package verified | none | keep page, download package, and scan verdict evidence with each release |
| Claude Skills | ready-to-submit | 1.0.3 | `platforms/claude-skill/` | Claude skill instructions and install notes generated | requires Claude account upload/install flow | upload the skill package or install `platforms/claude-skill/SKILL.md` as the Claude-facing prompt skill |
| OpenAI GPT Store | ready-to-submit | 1.0.3 | `platforms/openai-gpt/` | Custom GPT instructions, Actions OpenAPI schema, and knowledge file list generated | requires ChatGPT builder account; public Actions also require hosted HTTPS API and a privacy policy URL | publish a prompt-only GPT first, then attach Actions after the backend and privacy policy are live |
| MCP Registry | ready-to-submit | 1.0.3 | `platforms/mcp-server/`, `platforms/mcp-registries/` | stdio MCP server, `server.json`, and registry submission notes generated | requires publisher namespace/auth and final package identity | submit the MCP package after publisher namespace is confirmed |
| Smithery | ready-to-submit | 1.0.3 | `platforms/mcp-server/`, `platforms/mcp-registries/smithery.md` | Smithery submission note generated | requires Smithery account/API key or compatible hosted endpoint | connect repo or hosted endpoint, then record listing URL |
| Glama | ready-to-submit | 1.0.3 | `platforms/mcp-server/`, `platforms/mcp-registries/glama.md` | Glama submission note generated | requires GitHub indexing or submission flow | request indexing after public repo metadata is current |
| PulseMCP | ready-to-submit | 1.0.3 | `platforms/mcp-server/`, `platforms/mcp-registries/pulsemcp.md` | PulseMCP submission note generated | requires manual/API submission | submit registry metadata and record listing URL |
| Hermes Agent / agentskills.io | ready-to-submit | 1.0.3 | `platforms/hermes-agent/`, `platforms/agentskills-io/` | Hermes skill, SOUL, MCP config, install notes, and agentskills.io listing generated | requires Hermes instance or agentskills.io submission flow | install in Hermes and submit listing package when account access is available |
| Dify Marketplace | ready-to-submit | 1.0.3 | `platforms/dify-plugin/` | Dify manifest, provider, and tool schemas generated | requires Dify marketplace publisher account and packaging review | package with Dify's marketplace tooling and record review result |
| GitHub Copilot Extensions | backend-needed | 1.0.3 | `platforms/github-copilot-extension/` | current package records the VS Code Copilot Extension path and retired GitHub App path caveat | GitHub App-based Copilot Extensions are closed; a VS Code extension or other currently supported Copilot surface must be built before marketplace submission | rebuild this as a VS Code Copilot Extension or supported GitHub Copilot integration, then record listing evidence |
| Microsoft Copilot Studio / Commercial Marketplace | tenant-needed | 1.0.3 | `platforms/microsoft-copilot-studio/` | agent instructions, Teams manifest draft, and Commercial Marketplace notes generated | requires Microsoft tenant, Copilot Studio license/admin approval; Commercial Marketplace requires a Partner Center package built through the supported Microsoft 365 Agents Toolkit path | create tenant-backed agent first, then package with the supported Agents Toolkit / Partner Center route |
| Poe Bots | ready-to-submit | 1.0.3 | `platforms/poe-bot/` | bot profile and prompt generated | requires Poe creator account | create bot, paste profile/prompt, and record public bot URL |
| Gemini Gems | ready-to-submit | 1.0.3 | `platforms/gemini-gem/` | Gem instructions generated | requires Gemini account with Gems creation/sharing | create Gem, paste instructions, and record share/public URL |

## Evidence Required Before Marking Published

- public listing URL or platform review record
- visible version number or package date
- package hash, download URL, or key file check
- security scan result when the platform provides one
- rejection reason and remediation note if submission is not accepted

## Current Release Boundary

- The MCP adapter is the highest-leverage execution layer because Hermes, Claude Desktop, Cursor, VS Code, Codex-style clients, and registry sites can consume it.
- OpenAI GPT Store, Poe, and Gemini Gems are guided assistant versions unless connected to the hosted MCP/API bridge.
- GitHub Copilot Extensions and Microsoft marketplaces require hosted or tenant-owned infrastructure; do not mark them `published` until the platform listing is visible.
