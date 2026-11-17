## Description:

AI agents borrow USDC based on their Moltbook karma score. Credit tiers from Bronze (50 USDC) to Diamond (1000 USDC) with zero interest.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[abdhilabs](https://clawhub.ai/user/abdhilabs)

### License/Terms of Use:

ISC

## Use Case:

External developers and agent operators use KarmaBank to register Moltbook-backed agents, check karma-based credit tiers, and run testnet USDC borrow/repay workflows from a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live financial paths can record successful transfers without independently confirmed Circle transaction success.

Mitigation: Use only sandbox or testnet Circle credentials and isolated wallets unless transfer handling fails closed and transaction status is independently confirmed.

Risk: Weak Moltbook identity verification can allow credit activity to be associated with an agent name without sufficient ownership proof.

Mitigation: Require enforced Moltbook identity ownership checks before registration, borrowing, repayment, or credit decisions.

Risk: The local ledger should not be treated as authoritative financial accounting for real funds.

Mitigation: Do not use the ledger for real accounting until Circle transfers are reconciled, failures are handled conservatively, and transaction status is verified.

Risk: Dependencies are not fully pinned and reproducible.

Mitigation: Pin dependency versions and use a reproducible install process before review or deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abdhilabs/skills/karmabank)
- [ClawDIS Homepage](https://github.com/openclaw/agent-credit-system)
- [Project Repository Listed in README](https://github.com/abdhilabs/karmabank)
- [Moltbook](https://moltbook.com)
- [Circle Console](https://console.circle.com)
- [USDC Hackathon](https://moltbook.com/m/usdc)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI workflows may read or write a local credit ledger and use Moltbook and Circle credentials when configured.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
