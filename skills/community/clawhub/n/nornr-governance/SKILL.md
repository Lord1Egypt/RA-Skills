---
name: nornr-governance
description: The control layer before consequential MCP and OpenClaw execution: approve, queue or block before local tool use turns into spend or vendor action.
homepage: https://github.com/NORNR/nornr-mcp-control
metadata: {"openclaw":{"homepage":"https://github.com/NORNR/nornr-mcp-control","primaryEnv":"NORNR_API_KEY","requires":{"env":["NORNR_API_KEY"],"anyBins":["python","python3"]}}}
---

# NORNR MCP Control for OpenClaw

## What this skill is for

Use NORNR as the control layer before an OpenClaw skill or local MCP-connected action triggers spend, vendor action or another consequential downstream step.

The shortest correct reading is:

- one local tool request becomes one NORNR intent
- NORNR decides whether it is approved, queued or blocked
- queued work enters named review with context attached
- the same action still survives into proof, finance packet and audit export later

## When to use it

- Before a skill triggers a purchase, subscription, or vendor-side paid action
- When an autonomous flow should pause for operator approval before execution
- When finance or operations need one defensible decision record after the action completes
- When suspicious prompt instructions or unusual spend should surface as review posture instead of silent execution

## Installation

- `python -m pip install -r requirements.txt`

## Hello world

1. Set `NORNR_API_KEY`.
2. Run:
   `python nornr_governance.py preflight --action purchase --amount-usd 25 --counterparty openai --purpose "Run the paid research action"`
3. If NORNR returns `approved`, the autonomous action may proceed.
4. If NORNR returns `approval_required` or `blocked`, stop the autonomous flow and route to review.

## Copy-paste MCP / desktop config

Use NORNR as the default control layer before consequential local tool execution clears:

- Claude Desktop:
  `nornr mcp claude-config --server-name nornr --agent-id openclaw-agent`
- Cursor:
  `nornr mcp cursor-config --server-name nornr --agent-id openclaw-agent`

## Cursor rule

Add this to `.cursorrules` if Cursor is allowed to use local tools through NORNR:

```text
Use NORNR as the control layer before consequential tool execution.
Do not proceed with a paid, vendor-side or policy-sensitive action until NORNR returns approved or a named operator explicitly approves the queued intent.
Treat queued, blocked, anomalous or review-required posture as a stop state for autonomous execution.
```

## First run

1. Set `NORNR_API_KEY` and, if needed, `NORNR_AGENT_ID`.
2. Run:
   `python nornr_governance.py preflight --action purchase --amount-usd 25 --counterparty openai --purpose "Run the paid research action"`
3. If NORNR returns `approved`, the action may proceed.
4. If NORNR returns `approval_required` or `blocked`, stop the autonomous flow and route to review.

## Environment

Only this variable is required:

- `NORNR_API_KEY`

These are optional:

- `NORNR_BASE_URL` (optional, defaults to `https://nornr.com`)
- `NORNR_AGENT_ID` or a stored NORNR login profile

## Default policy pack for OpenClaw

Start from `mcp-local-tools-guarded` when OpenClaw actions can trigger spend, vendor action or policy-sensitive tool execution. The point is not to invent a new OpenClaw policy language. It is to make NORNR the default control layer before autonomous execution.

## Recommended API key scope

Minimum action scope for the full skill surface:

- `payments:write`
- `workspace:read`
- `approvals:write`
- `events:read`
- `audit:read`

Add these if you want the finance-close paths too:

- `reports:read`
- `webhooks:read`

## Dependency provenance

This skill delegates governance decisions to the official NORNR Python SDK, `agentpay`.

- Public MCP package repo: `https://github.com/NORNR/nornr-mcp-control`
- Install source: `requirements.txt`
- Pinned PyPI package: `nornr-agentpay==0.1.0`
- Local bridge: `nornr_governance.py`

Review the pinned SDK revision before use if your environment requires dependency review.

## Commands

- `python nornr_governance.py preflight --action purchase --amount-usd 25 --counterparty openai --purpose "Run the paid research action"`
- `python nornr_governance.py approvals`
- `python nornr_governance.py approve --payment-intent-id pi_123 --comment "Approved after review"`
- `python nornr_governance.py reject --payment-intent-id pi_123 --comment "Rejected pending review"`
- `python nornr_governance.py anomalies --counterparty openai`
- `python nornr_governance.py timeline`
- `python nornr_governance.py finance-packet`
- `python nornr_governance.py audit-export`
- `python nornr_governance.py weekly-review`
- `python nornr_governance.py monthly-close --provider quickbooks`
- `python nornr_governance.py review-bundle --counterparty openai`

## Why raw tool execution is not enough

Raw OpenClaw or MCP tool execution exposes capability. NORNR adds the missing layer above capability:

- should this action clear under the active mandate
- who reviews it when it should queue
- what finance or audit can inspect afterward

## What happens after queued

Queued does not mean "probably yes later". It means:

1. stop the autonomous action
2. inspect `review-bundle`, `anomalies` or `timeline`
3. let a named operator `approve` or `reject`
4. carry the same action into `finance-packet`, `audit-export` or `monthly-close` later

## Suggested demo GIF

The clearest first demo is:

1. the local agent proposes a consequential action
2. NORNR returns `approval_required`
3. the client pauses instead of continuing
4. an operator approves
5. the action resumes with one defended record afterward

## Operating rule

Do not let OpenClaw proceed with the autonomous action until NORNR returns `approved` or an operator explicitly approves the queued intent. Treat queued, blocked, anomalous, or prompt-risk posture as operator review states, not autonomous green lights.
