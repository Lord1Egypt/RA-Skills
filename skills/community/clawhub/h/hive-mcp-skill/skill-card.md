## Description:

Use Hive Intelligence MCP through UXC for broad crypto market, onchain, portfolio, and risk workflows with help-first discovery and convenience-layer guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and invoke Hive Intelligence MCP endpoints for crypto market, onchain, portfolio, wallet, and security-risk workflows through UXC. It is intended as a convenience layer that inspects endpoint schemas before narrow, explicit invocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, token symbols, and other query inputs may be sent to Hive's remote MCP service.

Mitigation: Keep requests narrow and avoid submitting sensitive wallet or portfolio details unless sharing them with Hive is acceptable.

Risk: The skill can guide endpoint invocation against a broad crypto MCP surface, including risk and portfolio workflows.

Mitigation: Inspect endpoint schemas before invocation and require explicit review before any write-like or transaction-related operation.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Hive MCP docs](https://hiveintelligence.xyz/crypto-market-data-mcp)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/hive-mcp-skill)
- [Publisher profile](https://clawhub.ai/user/jolestar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON argument examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send wallet addresses, token symbols, and other query inputs to Hive's remote MCP service.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
