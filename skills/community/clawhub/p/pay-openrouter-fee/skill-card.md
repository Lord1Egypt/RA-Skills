## Description:

Top up or pay OpenRouter or similar LLM billing from a CAI custodial wallet after an agent finds the payee details and the user confirms the transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent prepare OpenRouter or similar LLM billing payments from a CAI custodial wallet. The user remains responsible for confirming the recipient, amount, chain, and token before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment recipient, amount, chain, or token details may be incorrect or malicious, and transfers may be irreversible.

Mitigation: Before approving any transfer, manually verify the billing source, recipient, amount, chain, and token.

Risk: The skill requires CAI_API_KEY configuration for wallet access.

Mitigation: Store the API key through the agent secret mechanism and avoid exposing it in chat or logs.

## Reference(s):

- [CAI Skill Reference](https://cai.com/skill.md)
- [Agent Payment Workflow](https://cai.com/skill-references/agent-payment-workflow.md)
- [CAI Agent Payment](https://cai.com/agent-payment.html)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash commands and payment workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before any transfer.]

## Skill Version(s):

1.0.15 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
