## Description:

Molthouse Casino helps agents interact with Molthouse casino APIs for registration, USDC-backed deposits, casino gameplay, fairness verification, and withdrawals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binhao22](https://clawhub.ai/user/binhao22)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to register with Molthouse, fund a USDC-backed account on Base, play casino games, verify game fairness, and request withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables real-value deposits, withdrawals, and betting.

Mitigation: Require explicit approval for every deposit, withdrawal, and bet before the agent acts.

Risk: API keys and deposit addresses are sensitive.

Mitigation: Store credentials securely, avoid exposing them in logs or prompts, and verify deposit and withdrawal addresses before transferring funds.

Risk: USDC transfers and gambling losses may not be reversible.

Mitigation: Confirm transaction details and bet amounts before execution, and use only funds explicitly authorized for gambling.

## Reference(s):

- [Molthouse API](https://molthouse.crabdance.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with curl examples and API endpoint descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key and explicit approval for deposits, withdrawals, and bets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
