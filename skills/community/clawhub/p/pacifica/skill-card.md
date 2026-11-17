## Description:

Trade perpetuals on Pacifica through MCP tools for market data, account monitoring, order execution, subaccounts, and real-time WebSocket streaming on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockchain-oracle](https://clawhub.ai/user/blockchain-oracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to inspect Pacifica market data, monitor accounts and positions, and prepare or execute order, funding, subaccount, and withdrawal workflows on Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent high-impact authority over crypto trading, including order execution, leverage, transfers, and withdrawals.

Mitigation: Use it only with wallet funds acceptable for agent-operated trading risk, keep separate hard limits and monitoring for autonomous use, and confirm order details during interactive use.

Risk: The Pacifica wallet private key is generated locally and gives full control over exposed funds.

Mitigation: Protect the local wallet configuration and treat the generated private key as sensitive credentials with full fund-control authority.

Risk: Installation depends on npm packages whose versions and provenance affect trust.

Mitigation: Verify npm package versions and provenance before installation or deployment.

## Reference(s):

- [Pacifica Skill Page](https://clawhub.ai/blockchain-oracle/skills/pacifica)
- [Pacifica Mainnet App](https://pacifica.fi)
- [Pacifica Testnet App](https://test-app.pacifica.fi)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes tool-selection mappings, wallet-required action notes, and JSON-oriented CLI/MCP usage guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
