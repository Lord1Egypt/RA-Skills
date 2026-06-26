# NORNR MCP Control for OpenClaw

This is the official NORNR skill bundle for OpenClaw / ClawHub.

It positions NORNR exactly where it belongs:

- before consequential MCP and OpenClaw execution
- before local tool use turns into spend or vendor action
- before review and export are lost to side channels

Use this bundle when an OpenClaw flow can trigger real-world spend or any downstream action that should pause for review before execution.

The shortest correct reading is:

- one local tool request becomes one NORNR intent
- NORNR decides whether it is approved, queued or blocked
- queued work enters named review with context attached
- the same action still survives into proof, finance packet and audit export later

## What NORNR does here

NORNR is not the runtime and not the rail.
It is the control layer above autonomous execution.

That means:

- OpenClaw can keep moving fast
- NORNR decides whether the action should proceed
- operators can approve queued actions
- operators can reject risky or suspicious actions before execution
- anomalies and intent timeline stay reviewable from the same lane
- finance gets a defensible record afterward

## Installation

```bash
python -m pip install -r requirements.txt
```

## Hello world

```bash
python nornr_governance.py preflight \
  --action purchase \
  --amount-usd 25 \
  --counterparty openai \
  --purpose "Run the paid research action"
```

Interpret the result like this:

- `approved`: the action can proceed
- `approval_required`: stop the autonomous flow and route to operator review
- `blocked`: do not proceed until the intent or policy changes

## Copy this config

If OpenClaw is part of a wider local-agent setup, use NORNR as the default control layer before consequential MCP tool execution clears:

```bash
nornr mcp claude-config --server-name nornr --agent-id openclaw-agent
nornr mcp cursor-config --server-name nornr --agent-id openclaw-agent
```

That should be treated as the standard install path when the same team also uses Claude Desktop or Cursor around OpenClaw.

The dependency is pinned to the official public NORNR Python SDK repo for provenance review:

- Public MCP package repo: `https://github.com/NORNR/nornr-mcp-control`
- PyPI package: `nornr-agentpay==0.1.0`
- Package spec: `requirements.txt`

## Cursor rule

Add this to `.cursorrules` if Cursor is allowed to use local tools through NORNR:

```text
Use NORNR as the control layer before consequential tool execution.
Do not proceed with a paid, vendor-side or policy-sensitive action until NORNR returns approved or a named operator explicitly approves the queued intent.
Treat queued, blocked, anomalous or review-required posture as a stop state for autonomous execution.
```

## Install and first preflight

1. Install the skill into your OpenClaw workspace:

```bash
clawhub install nornr-governance --workdir /path/to/openclaw-workspace
```

2. Install the pinned NORNR SDK dependency:

```bash
cd /path/to/openclaw-workspace/skills/nornr-governance
python -m pip install -r requirements.txt
```

3. Set the minimum NORNR environment:

```bash
export NORNR_API_KEY="replace-with-your-key"
export NORNR_BASE_URL="https://nornr.com"
export NORNR_AGENT_ID="replace-with-your-agent-id"
```

4. Run a first preflight before any paid or risky action:

```bash
python nornr_governance.py preflight \
  --action purchase \
  --amount-usd 25 \
  --counterparty openai \
  --purpose "Run the paid research action"
```

## Environment

Only this variable is required:

- `NORNR_API_KEY`

These are optional:

- `NORNR_BASE_URL` (optional, defaults to `https://nornr.com`)
- `NORNR_AGENT_ID` or a stored NORNR login profile

## Default policy pack for OpenClaw

Start from `mcp-local-tools-guarded` when OpenClaw actions can trigger spend, vendor action or policy-sensitive tool execution. This is how NORNR becomes the default control layer before autonomous execution, not just a useful plugin after the fact.

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

## Files

- `SKILL.md` - minimal skill definition for OpenClaw / ClawHub
- `SECURITY.md` - dependency provenance, key scope, and review checklist
- `requirements.txt` - pinned install spec for the official NORNR SDK dependency
- `nornr_governance.py` - tiny CLI bridge into `agentpay.openclaw`

## Dependency provenance

This bundle is intentionally thin. The actual governance logic lives in the official NORNR Python SDK, not in a second copy hidden inside the skill.

- Public MCP package repo: `https://github.com/NORNR/nornr-mcp-control`
- Delegated package: `nornr-agentpay` (import path: `agentpay`)
- Public source repo: `https://github.com/NORNR/sdk-py`
- Pinned package release for this skill: `0.1.0`

If your environment requires security review, inspect the pinned SDK revision before enabling the skill in autonomous workflows.

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

OpenClaw can expose useful autonomous capability. That is not the same thing as a control plane.

Raw tool execution still leaves three missing questions:

- should this action clear under the active mandate
- who reviews it when it should queue
- what finance or audit can inspect after it runs

NORNR sits above execution and answers those questions before the action continues.

## What happens after queued

Queued means the action stops and enters review with context attached.

1. Stop the autonomous action path.
2. Inspect `review-bundle`, `anomalies` or `timeline`.
3. Let a named operator `approve` or `reject`.
4. Use `finance-packet`, `audit-export` or `monthly-close` once the action has to survive outside engineering too.

## Suggested demo GIF

The clearest first demo is:

1. the local agent proposes a consequential action
2. NORNR returns `approval_required`
3. the client pauses instead of continuing
4. an operator approves
5. the action resumes with one defended record afterward

## Recommended autonomous pattern

1. Run `preflight` before the OpenClaw skill triggers a paid or risky action.
2. If NORNR returns `approval_required`, stop the autonomous flow.
3. Inspect `review-bundle` or `anomalies` to understand why the lane is hot.
4. `approve` or `reject` explicitly.
5. Use `finance-packet`, `audit-export`, or `monthly-close` when finance needs the record afterward.

See [SECURITY.md](./SECURITY.md) for provenance review and recommended key scope.
