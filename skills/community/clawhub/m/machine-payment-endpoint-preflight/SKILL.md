---
name: machine-payment-endpoint-preflight
description: "Machine Payment Endpoint Preflight: Inspect one public HTTPS endpoint without credentials or payment. Validate the URL, make one bounded GET request, and report whether its HTTP 402 x402 or MPP payment offers are parseable and internally consistent. Return protocols, prices, currencies, networks, recipients, expiries, conflicts, and a safe next action. Never sign, pay, or broadcast a transaction. Use when an agent needs to run this published AgentPMT workflow with 2 linked tool skills, workflow."
version: 1.0.0
homepage: https://www.agentpmt.com/agent-workflow-skills/machine-payment-endpoint-preflight
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/agent-workflow-skills/machine-payment-endpoint-preflight"}}
---
# Machine Payment Endpoint Preflight

## Freshness
Last updated: `2026-08-11`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Workflow Does
Inspect one public HTTPS endpoint without credentials or payment. Validate the URL, make one bounded GET request, and report whether its HTTP 402 x402 or MPP payment offers are parseable and internally consistent. Return protocols, prices, currencies, networks, recipients, expiries, conflicts, and a safe next action. Never sign, pay, or broadcast a transaction.

## Required Setup
- AgentPMT overview: `../what-is-agentpmt`.
- Account MCP/REST setup: `../agentpmt-account-mcp-rest-api-setup`.

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

## Workflow Session Management
Call `AgentPMT-Workflow-Skills` with `start_workflow` before the first step and `end_workflow` after the final step.

```json
{"action":"start_workflow","skill_id":"machine-payment-endpoint-preflight"}
```

```json
{"action":"end_workflow","skill_id":"machine-payment-endpoint-preflight","rating":5,"comment":"completed"}
```

## Workflow Process
1. Collect Payment Endpoint
   - Prompt: Collect and normalize exactly one public HTTPS endpoint to inspect without credentials or payment.
2. Validate Public URL
   - Tool product: Data Format Validation.
   - Tool skill: `../data-format-validation`.
   - ClawHub page: https://clawhub.ai/agentpmt/data-format-validation.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill data-format-validation`.
   - Marketplace: https://www.agentpmt.com/marketplace/data-format-validation.
   - Tool instructions: Validate the normalized URL from the prior step. Stop if it is invalid, not HTTPS, includes credentials, or cannot be inspected safely. Pass the validated URL to the next step.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
3. Fetch Unpaid Payment Contract
   - Tool product: Webhook - HTTP Request.
   - Tool skill: `../webhook-http-request`.
   - ClawHub page: https://clawhub.ai/agentpmt/webhook-http-request.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill webhook-http-request`.
   - Marketplace: https://www.agentpmt.com/marketplace/webhook-http-request.
   - Tool instructions: Fetch the validated public URL exactly once with GET, no credentials, no cookies, no signing, and no payment. Keep the 128 KiB and 15-second caps. Preserve status, final URL, response headers, and bounded body for the report. Treat redirects or a non-402 response as evidence, not success.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
4. Report Payment Offer Safety
   - Prompt: Produce a compact, machine-readable preflight of the unpaid endpoint response and its x402 or MPP payment offers.

## Tool Skill Links
- Data Format Validation: `../data-format-validation`; ClawHub https://clawhub.ai/agentpmt/data-format-validation; skills.sh `npx skills add AgentPMT/agent-skills --skill data-format-validation`; marketplace https://www.agentpmt.com/marketplace/data-format-validation
- Webhook - HTTP Request: `../webhook-http-request`; ClawHub https://clawhub.ai/agentpmt/webhook-http-request; skills.sh `npx skills add AgentPMT/agent-skills --skill webhook-http-request`; marketplace https://www.agentpmt.com/marketplace/webhook-http-request

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Workflow page: https://www.agentpmt.com/agent-workflow-skills/machine-payment-endpoint-preflight
- AgentPMT workflows: https://www.agentpmt.com/agent-workflow-skills
