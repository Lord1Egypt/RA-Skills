## Description:

Open-source market making for AI agents. Multi-exchange trading, grid strategies, and real-time market data. CLI + MCP + Skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agents use OpenMM to retrieve exchange market and account data, configure exchange credentials, and support multi-exchange market-making and grid-trading workflows through CLI commands, MCP tools, and portable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access exchange account data and, when enabled, place or cancel real trades.

Mitigation: Use dedicated exchange API keys with withdrawals disabled, narrow read and trade permissions, IP allowlisting, pinned package versions, small limits, and human confirmation before non-dry-run actions.

Risk: Automated grid strategies and bulk cancellation authority can affect live orders without strong built-in confirmation controls.

Mitigation: Keep destructive tools disabled unless needed, dry-run strategies first, require confirmation outside the model, and apply max-position and safety-reserve limits.

## Reference(s):

- [OpenMM GitHub Repository](https://github.com/3rd-Eye-Labs/OpenMM)
- [OpenMM Documentation](https://deepwiki.com/3rd-Eye-Labs/OpenMM)
- [OpenMM MCP Server](https://github.com/QBT-Labs/OpenMM-MCP)
- [OpenMM npm Package](https://www.npmjs.com/package/@3rd-eye-labs/openmm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with CLI commands, JSON examples, TypeScript snippets, and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON command output when users request machine-readable CLI or MCP results.]

## Skill Version(s):

0.1.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
