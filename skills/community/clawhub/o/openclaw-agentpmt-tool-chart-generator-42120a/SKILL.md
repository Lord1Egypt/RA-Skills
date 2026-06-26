---
name: agentpmt-current-clawhub-skills
description: "Find and install the current canonical AgentPMT skills published under the AgentPMT ClawHub org account. Use when an agent needs the latest AgentPMT setup, x402/no-account, overview, or current tool skills and should route to AgentPMT's current ClawHub locations."
version: 1.0.0
homepage: https://clawhub.ai/user/agentpmt
compatibility: "No credentials required. This is an index and routing skill for canonical AgentPMT ClawHub listings."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://clawhub.ai/user/agentpmt"}}
---

# AgentPMT Current ClawHub Skills

## Freshness

Last updated: `2026-06-09`.

If the current date is more than 7 days after the last updated date, check the AgentPMT ClawHub publisher page before relying on this index:

https://clawhub.ai/user/agentpmt

Use this skill to choose current AgentPMT skills from the AgentPMT org account. Every skill link below points directly to the canonical AgentPMT ClawHub location.

## Canonical Publisher

Current AgentPMT ClawHub org:

https://clawhub.ai/user/agentpmt

Use only the full AgentPMT ClawHub URLs in this document when linking, installing, or handing users to a current AgentPMT skill.

## Current AgentPMT Org Skills

| Skill | Slug | Current Version | Use When | Current ClawHub Page |
|---|---|---|---|---|
| AgentPMT no-account AgentAddress/x402 setup | `agentpmt-no-account-agentaddress-x402` | `v1.0.1` | The caller does not have an AgentPMT account Bearer Token and must use AgentAddress credits or direct x402 payment. | https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402 |
| What Is AgentPMT | `what-is-agentpmt` | `v1.0.0` | The caller needs the AgentPMT concept map before choosing account, no-account, MCP, REST, workflow, skill, or payment paths. | https://clawhub.ai/agentpmt/what-is-agentpmt |
| AgentPMT account MCP/REST API setup | `agentpmt-account-mcp-rest-api-setup` | `v1.0.0` | The caller has an AgentPMT Agent Group Bearer Token and should connect the hosted MCP server, local MCP router, or REST API. | https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup |
| Image Generation Agent | `image-generation-agent` | `v1.0.0` | The caller needs the AgentPMT image generation tool powered by Google Gemini/Nano Banana, including text-to-image and reference-image edits. | https://clawhub.ai/agentpmt/image-generation-agent |

## Install Commands

Install the current AgentPMT setup skills:

| Skill | AgentPMT ClawHub Page | Install Command |
|---|---|---|
| AgentPMT no-account AgentAddress/x402 setup | https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402 | `openclaw skills install agentpmt-no-account-agentaddress-x402` |
| What Is AgentPMT | https://clawhub.ai/agentpmt/what-is-agentpmt | `openclaw skills install what-is-agentpmt` |
| AgentPMT account MCP/REST API setup | https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup | `openclaw skills install agentpmt-account-mcp-rest-api-setup` |

```bash
openclaw skills install agentpmt-no-account-agentaddress-x402
openclaw skills install what-is-agentpmt
openclaw skills install agentpmt-account-mcp-rest-api-setup
```

Install the current AgentPMT product skill published on the org account:

| Skill | AgentPMT ClawHub Page | Install Command |
|---|---|---|
| Image Generation Agent | https://clawhub.ai/agentpmt/image-generation-agent | `openclaw skills install image-generation-agent` |

```bash
openclaw skills install image-generation-agent
```

If the installer or search results show multiple AgentPMT-related entries, choose the listing whose full page URL starts with `https://clawhub.ai/agentpmt/`.

## Choosing The Right Skill

Use `what-is-agentpmt` first when the caller is deciding what AgentPMT path to use.

Canonical page: https://clawhub.ai/agentpmt/what-is-agentpmt

Use `agentpmt-account-mcp-rest-api-setup` when the caller has an AgentPMT account and an Agent Group Bearer Token.

Canonical page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup

Use `agentpmt-no-account-agentaddress-x402` when the caller does not have an AgentPMT account Bearer Token and should pay with AgentAddress credits or x402.

Canonical page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402

Use `image-generation-agent` when the caller specifically needs AgentPMT image generation actions, schemas, prices, sample parameters, and call shapes.

Canonical page: https://clawhub.ai/agentpmt/image-generation-agent

## Static Skill Notes

The current AgentPMT org setup/static skills in this index are:

- `agentpmt-no-account-agentaddress-x402`: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402
- `what-is-agentpmt`: https://clawhub.ai/agentpmt/what-is-agentpmt
- `agentpmt-account-mcp-rest-api-setup`: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup

`image-generation-agent` is a current generated product skill on the AgentPMT org account: https://clawhub.ai/agentpmt/image-generation-agent

`vercel-creating-using-skills` is not an AgentPMT current setup, payment, or product skill and is intentionally excluded from this index.

## Routing Rule

When this skill is installed, use it only as an index. Route users to the current AgentPMT org page or one of the current AgentPMT skill pages listed above.

Do not copy partial paths or relative paths. Use the full AgentPMT ClawHub URL for every handoff:

- https://clawhub.ai/user/agentpmt
- https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402
- https://clawhub.ai/agentpmt/what-is-agentpmt
- https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
- https://clawhub.ai/agentpmt/image-generation-agent

## AgentPMT Reference

- AgentPMT website: https://www.agentpmt.com
- AgentPMT marketplace: https://www.agentpmt.com/marketplace
- AgentPMT ClawHub org: https://clawhub.ai/user/agentpmt
- Current AgentPMT skills repository: https://github.com/AgentPMT/agent-skills
