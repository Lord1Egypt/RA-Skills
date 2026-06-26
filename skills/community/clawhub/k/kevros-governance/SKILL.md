# Kevros — Governance-as-a-Service for AI Agents

Every agent action verified. Every decision recorded. Every record signed.

## What This Does

Kevros adds cryptographic governance to any AI agent. Before your agent takes an action (deploy code, move money, access data), Kevros evaluates it against your policies and returns a signed decision: **ALLOW**, **CLAMP** (adjusted to safe bounds), or **DENY**.

Every decision is appended to a hash-chained, tamper-evident evidence ledger. Auditors can verify the entire chain without your source code.

## Quick Start

```python
from kevros_governance import GovernanceClient

client = GovernanceClient(agent_id="my-agent")
result = client.verify(
    action_type="trade",
    action_payload={"symbol": "AAPL", "qty": 100},
    agent_id="my-agent",
)
print(result.decision)  # ALLOW, CLAMP, or DENY
```

Or use the API directly:

```bash
# Get a free API key (instant, no credit card)
curl -X POST https://governance.taskhawktech.com/signup \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "my-agent"}'

# Verify an action
curl -X POST https://governance.taskhawktech.com/governance/verify \
  -H "X-API-Key: kvrs_..." \
  -H "Content-Type: application/json" \
  -d '{"action_type": "deploy", "action_payload": {"service": "api"}, "agent_id": "my-agent"}'
```

## Governance Primitives

| Primitive | What It Proves | Cost |
|-----------|---------------|------|
| **Verify** | Agent is authorized — signed ALLOW/CLAMP/DENY | $0.01 |
| **Attest** | Action happened — hash-chained evidence | $0.02 |
| **Bind** | Intent matched command — cryptographic binding | $0.02 |
| **Bundle** | Compliance evidence package — independently verifiable | $0.25 |
| **Media Attest** | Media file integrity — SHA-256 in provenance chain | $0.05 |

Free endpoints: verify-outcome, verify-token, verify-certificate, reputation lookup, passport, media verify.

## Payment

- **Free tier**: 1,000 calls/month, instant signup, no credit card
- **x402 (USDC on Base)**: Pay per call, no API key needed
- **Subscription**: Scout $29/mo, Sentinel $149/mo, Sovereign $499/mo

## Why Agents Need This

- **Audit trails**: When regulators ask "who authorized this agent action?", you have cryptographic proof
- **Fail-closed safety**: If governance fails, the agent stops. Not the other way around
- **Trust between agents**: Agent B can verify Agent A's release token without trusting Agent A
- **Evidence chain**: Hash-chained, append-only, independently verifiable

## Integration

- **Python SDK**: `pip install kevros`
- **TypeScript SDK**: `npm install @kevros/agentkit`
- **MCP**: `https://governance.taskhawktech.com/mcp/`
- **A2A**: `https://governance.taskhawktech.com/.well-known/agent.json`
- **x402**: `https://governance.taskhawktech.com/.well-known/x402`
- **REST API**: `https://governance.taskhawktech.com/api`

Works with LangChain, CrewAI, OpenAI Agents SDK, Microsoft Agent Framework, and any HTTP client.

## Links

- Website: https://www.taskhawktech.com
- API Docs: https://governance.taskhawktech.com/api
- Quickstart: https://www.taskhawktech.com/quickstart
- Playground: https://www.taskhawktech.com/playground
