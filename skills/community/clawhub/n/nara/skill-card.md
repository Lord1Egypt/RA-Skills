## Description:

Nara helps agents use the Nara chain CLI for PoMI quest mining, wallet operations, transfers, on-chain skills, ZK ID, agent registration, referrals, and related NARA workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naraguy](https://clawhub.ai/user/naraguy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate naracli for Nara wallet setup, PoMI quest mining, agent registration, referrals, ZK ID, transfers, and on-chain skill or agent tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to install or run mutable crypto-wallet tooling from npm.

Mitigation: Review the package before installation, pin and verify the naracli version, and obtain explicit user confirmation before installing or first running the CLI.

Risk: Wallet creation, transactions, staking, unstaking, uploads, deletes, endpoint changes, and social account binding can affect assets or accounts.

Mitigation: Require explicit user confirmation for each asset-affecting, account-binding, endpoint-changing, upload, or delete action.

Risk: The skill can install a secondary AgentX skill whose behavior may differ from the reviewed artifact.

Mitigation: Inspect any AgentX skill contents before installation or use.

## Reference(s):

- [Nara homepage](https://nara.build)
- [naracli npm package](https://www.npmjs.com/package/naracli)
- [naracli source repository](https://github.com/nara-chain/nara-cli)
- [ClawHub skill page](https://clawhub.ai/naraguy/skills/nara)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI workflow details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local npm/npx CLI execution and wallet-affecting actions that require explicit user confirmation.]

## Skill Version(s):

1.0.31 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
