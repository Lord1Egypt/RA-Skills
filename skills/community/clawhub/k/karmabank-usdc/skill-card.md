## Description:

AI agents borrow USDC based on their Moltbook karma score. Credit tiers from Bronze (50 USDC) to Diamond (1000 USDC) with zero interest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdhilabs](https://clawhub.ai/user/abdhilabs)

### License/Terms of Use:

ISC

## Use Case:

External developers and agent builders use KarmaBank to register agents, check Moltbook-based credit tiers, and run testnet USDC borrow, repay, transaction history, and wallet creation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial wallet and loan commands may create wallets or initiate borrow and repay actions.

Mitigation: Use only sandbox/testnet credentials and require review before allowing an agent to run borrow, repay, or wallet creation commands.

Risk: The install path needs dependency review before deployment.

Mitigation: Audit or remove the local file dependency, require a lockfile or pinned dependency versions, and review the skill before installation.

## Reference(s):

- [KarmaBank ClawHub page](https://clawhub.ai/abdhilabs/skills/karmabank-usdc)
- [Moltbook](https://moltbook.com)
- [Circle Console](https://console.circle.com)
- [USDC Agentic Hackathon](https://moltbook.com/m/usdc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI command examples and configuration variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions for KarmaBank CLI workflows.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
