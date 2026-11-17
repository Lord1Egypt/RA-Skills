## Description:

Oanda Forex Trading lets agents retrieve OANDA forex market data, inspect account state, and place or manage practice or live forex orders through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to integrate OANDA forex market data and trading workflows into AgentPMT-enabled automations, including price checks, historical candles, account review, order placement, order modification, cancellation, and trade or position closure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected credentials can be used to place, modify, cancel, or close live-money forex trades.

Mitigation: Use practice credentials by default, require explicit human confirmation for every order-affecting action, and apply separate live-trading controls before enabling real accounts.

Risk: Prompts or logs could expose account credentials, wallet secrets, signatures, or payment headers.

Mitigation: Keep credentials in the setup flow, avoid placing secrets in prompts or logs, and scope tool inputs to the minimum content needed.

Risk: Outdated schemas, examples, or setup routes may cause incorrect calls against a remote trading integration.

Mitigation: Refresh the skill before use when stale, fetch live schema or instructions when parameters are unclear, and resolve validation or warning responses before retrying.

## Reference(s):

- [Oanda Forex Trading schema](artifact/schema.md)
- [AgentPMT marketplace product page](https://www.agentpmt.com/marketplace/oanda-forex-trading-2)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/oanda-forex-trading)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON action payloads, MCP/REST call examples, and shell setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote tool responses are JSON and should be treated as the source of truth for each call.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
