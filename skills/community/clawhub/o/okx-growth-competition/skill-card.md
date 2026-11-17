## Description:

Helps agents guide users through Agentic Wallet trading competitions, including discovery, rule review, registration, leaderboard checks, and reward claiming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find OKX Agentic Wallet trading competitions, understand rules and prize pools, join eligible competitions, check rankings, and claim rewards through wallet-mediated flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reward claiming can sign backend-provided blockchain transactions without documented validation.

Mitigation: Before claiming rewards, verify the wallet, chain, recipient, amount, and transaction details through a trusted wallet or OKX interface.

Risk: The skill may inspect other wallet accounts while checking competition participation or reward status.

Mitigation: Install and use it only when account inspection is expected, and avoid exposing unrelated wallet accounts unless needed for the competition workflow.

Risk: Competition reward claims require wallet-mediated authority and can broadcast transactions.

Mitigation: Use the claim flow only after confirming eligibility and transaction details, and ensure the wallet has sufficient gas before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ok-james-01/skills/okx-growth-competition)
- [Publisher profile](https://clawhub.ai/user/ok-james-01)
- [OKX Web3](https://web3.okx.com)
- [Competition CLI Reference](references/cli-reference.md)
- [Trading competition page pattern](https://web3.okx.com/boost/trading-competition/{shortName})

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API calls]

**Output Format:** [Markdown responses with command references and structured competition tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fixed response templates for competition listing, details, registration, status, ranking, wallet export guard, and reward claiming.]

## Skill Version(s):

3.1.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
