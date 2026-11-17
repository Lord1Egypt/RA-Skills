## Description:

AI agents borrow USDC based on their Moltbook karma score. Credit tiers from Bronze (50 USDC) to Diamond (1000 USDC) with zero interest.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[abdhilabs](https://clawhub.ai/user/abdhilabs)

### License/Terms of Use:

ISC

## Use Case:

External developers and agent builders use KarmaBank to try a command-line USDC credit workflow that registers Moltbook-named agents, calculates karma-based credit tiers, and records borrow and repay activity in a demo ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet or API secrets could be exposed when installing mutable wallet-related dependencies.

Mitigation: Use only testnet or throwaway credentials, avoid running npm install where wallet/API secrets are present, and inspect or vendor the missing ../skills/circle-wallet dependency before use.

Risk: Borrow, repay, and wallet creation commands can trigger financial or wallet-related actions without enough scoping.

Mitigation: Require explicit human confirmation of amount, account, network, and environment before allowing an agent to run those commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abdhilabs/skills/karmabank-minimal)
- [Moltbook](https://moltbook.com)
- [Circle Console](https://console.circle.com)
- [Moltbook USDC Hackathon](https://moltbook.com/m/usdc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Moltbook and Circle environment variables; mock profiles are used when MOLTBOOK_API_KEY is unset.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
