## Description:

MoltCredit helps agents extend trust-based credit lines, track balances and transactions, and settle balances through the X402 stablecoin protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levi-law](https://clawhub.ai/user/levi-law)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use MoltCredit to let agents manage bilateral credit, record transaction history, check balances, and prepare settlement requests for agent commerce workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated scripts can extend credit, record transactions, and generate settlement requests without built-in confirmation.

Mitigation: Require manual review or wrapper-policy approval for recipients, limits, amounts, currencies, and settlement targets before execution.

Risk: The skill depends on MOLTCREDIT_API_KEY for financial state changes.

Mitigation: Store the API key securely, avoid exposing it in logs or shared sessions, and restrict automated access to trusted agents.

Risk: Attacker-supplied agent names, limits, or transaction values could cause unintended credit or balance changes.

Mitigation: Validate agent handles and numeric values against trusted business rules before invoking the provided scripts.

## Reference(s):

- [MoltCredit ClawHub page](https://clawhub.ai/levi-law/skills/moltcredit)
- [MoltCredit landing page](https://levi-law.github.io/moltcredit-landing)
- [MoltCredit API docs](https://moltcredit-737941094496.europe-west1.run.app/skill.md)
- [X402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MOLTCREDIT_API_KEY for authenticated credit, transaction, balance, history, and settlement operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
