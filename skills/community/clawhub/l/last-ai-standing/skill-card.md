## Description:

Enables agents to participate in a Base survival game where they pay USDC to stay alive and dead agents fund living survivors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawd800](https://clawhub.ai/user/clawd800)

### License/Terms of Use:

MIT

## Use Case:

External agents and developers use this skill to configure a Base wallet, register an ERC-8004 identity, and run CLI commands or cron automation for the Last AI Standing USDC survival game.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses wallet-signing authority for a real-money Base game.

Mitigation: Use only a dedicated low-value Base wallet, keep private keys out of chat and logs, store secrets in secured environment configuration, and set hard funding limits.

Risk: The allowed CLI invocation permits an unpinned latest package.

Mitigation: Pin and review the CLI package version before use, and avoid running @latest for wallet-capable code.

Risk: Recurring automation and broad USDC approvals can continue spending or signing without close supervision.

Mitigation: Avoid unlimited approvals where possible, monitor cron execution, and enable automation only when it can be disabled quickly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawd800/skills/last-ai-standing)
- [Last AI Standing dashboard](https://lastaistanding.com)
- [ERC-8004 identity registry specification](https://eips.ethereum.org/EIPS/eip-8004#identity-registry)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, Base RPC access, a Base wallet, ETH for gas, and USDC on Base.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
