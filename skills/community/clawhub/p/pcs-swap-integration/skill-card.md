## Description:

Integrate PancakeSwap swaps into applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcs-bot](https://clawhub.ai/user/pcs-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add PancakeSwap quote, routing, transaction encoding, and swap execution guidance to frontends, backends, scripts, and smart contracts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated swap examples can submit real mainnet transactions from funded wallets.

Mitigation: Review generated code before execution and prefer testnet or simulation before using funded wallets.

Risk: Example flows can grant persistent unlimited token approvals.

Mitigation: Use exact-amount or short-lived approvals where possible and verify router and Permit2 addresses before approving tokens.

Risk: Project tooling or agent-readable environments may expose production private keys.

Mitigation: Avoid placing production private keys where the agent or project tooling can read them unnecessarily.

Risk: Unpinned dependencies can change swap behavior or integration compatibility over time.

Mitigation: Pin dependencies with a lockfile and review dependency changes before execution.

## Reference(s):

- [PancakeSwap AI repository](https://github.com/pancakeswap/pancakeswap-ai)
- [ClawHub skill page](https://clawhub.ai/pcs-bot/skills/pcs-swap-integration)
- [ClawHub publisher profile](https://clawhub.ai/user/pcs-bot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, SDK setup instructions, smart contract call patterns, and transaction safety checks.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
