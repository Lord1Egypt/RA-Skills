---
name: machine-purchase-roi-gate
description: "Machine Purchase ROI Gate: Decide whether an agent should buy one machine service call before any payment. Validate explicit price, fee, failure probability, retry cost, output value, and budget assumptions; calculate expected net value, finite financial ROI, capital at risk, and the maximum rational price; then return buy, defer, or reject with the binding reason. Never access a wallet, sign, pay, or broadcast. Use when an agent needs to run this published AgentPMT workflow with 2 linked tool."
version: 1.0.0
homepage: https://www.agentpmt.com/agent-workflow-skills/machine-purchase-roi-gate
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/agent-workflow-skills/machine-purchase-roi-gate"}}
---
# Machine Purchase ROI Gate

## Freshness
Last updated: `2026-08-11`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Workflow Does
Decide whether an agent should buy one machine service call before any payment. Validate explicit price, fee, failure probability, retry cost, output value, and budget assumptions; calculate expected net value, finite financial ROI, capital at risk, and the maximum rational price; then return buy, defer, or reject with the binding reason. Never access a wallet, sign, pay, or broadcast.

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
{"action":"start_workflow","skill_id":"machine-purchase-roi-gate"}
```

```json
{"action":"end_workflow","skill_id":"machine-purchase-roi-gate","rating":5,"comment":"completed"}
```

## Workflow Process
1. Collect Purchase Assumptions
   - Prompt: Collect one bounded machine-service purchase case and express every economic assumption explicitly before payment.
2. Validate Purchase JSON
   - Tool product: Data Format Validation.
   - Tool skill: `../data-format-validation`.
   - ClawHub page: https://clawhub.ai/agentpmt/data-format-validation.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill data-format-validation`.
   - Marketplace: https://www.agentpmt.com/marketplace/data-format-validation.
   - Tool instructions: Validate the canonical JSON from the prior step. Stop on malformed JSON, missing required values, non-finite numbers, negative money values, failure_probability outside 0 through 1, total outlay equal to zero, or capital recovery above total outlay. Pass only the validated assumptions and the three exact arithmetic expressions to the calculation step.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
3. Calculate Expected Return
   - Tool product: Complex Mathematics Engine.
   - Tool skill: `../complex-mathematics-engine`.
   - ClawHub page: https://clawhub.ai/agentpmt/complex-mathematics-engine.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill complex-mathematics-engine`.
   - Marketplace: https://www.agentpmt.com/marketplace/complex-mathematics-engine.
   - Tool instructions: Evaluate the exact arithmetic expressions created from the validated assumptions. Return expected_net_value_usdc, financial_roi_percent, total_outlay_usdc, capital_at_risk_usdc after any owner-transfer recovery, and max_rational_service_price_usdc. Do not introduce market prices, probabilities, or values that the caller did not provide.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
4. Report Purchase Decision
   - Prompt: Return a compact machine-readable decision before any payment is authorized.

## Tool Skill Links
- Data Format Validation: `../data-format-validation`; ClawHub https://clawhub.ai/agentpmt/data-format-validation; skills.sh `npx skills add AgentPMT/agent-skills --skill data-format-validation`; marketplace https://www.agentpmt.com/marketplace/data-format-validation
- Complex Mathematics Engine: `../complex-mathematics-engine`; ClawHub https://clawhub.ai/agentpmt/complex-mathematics-engine; skills.sh `npx skills add AgentPMT/agent-skills --skill complex-mathematics-engine`; marketplace https://www.agentpmt.com/marketplace/complex-mathematics-engine

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Workflow page: https://www.agentpmt.com/agent-workflow-skills/machine-purchase-roi-gate
- AgentPMT workflows: https://www.agentpmt.com/agent-workflow-skills
