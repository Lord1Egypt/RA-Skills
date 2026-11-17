## Description:

Use when the user asks for Pionex account balance, available funds, or how much USDT they have; it is read-only, requires API credentials, and should not be used for market data or placing/cancelling orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pibrandon](https://clawhub.ai/user/pibrandon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent retrieve Pionex spot account balances, including available funds and currency-specific balances such as USDT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Pionex API credentials to retrieve account balances.

Mitigation: Use read-only credentials where available and avoid granting trading permissions for this read-only balance lookup workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON balance output references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying account balance command returns JSON for spot balances that the agent filters or summarizes for the user.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
