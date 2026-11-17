## Description:

Discover and call paid third-party API services through the Nightmarket marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sistillisteph](https://clawhub.ai/user/sistillisteph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover third-party API services, inspect endpoint details, and make free or paid API calls through Nightmarket with x402 payment handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents toward consequential setup actions, including remote skill installation, wallet creation, credential storage, funding, and paid API calls.

Mitigation: Require explicit user confirmation before each consequential step and before any paid API call.

Risk: CrowPay API keys and authorization headers may expose payment credentials or sensitive request data if stored or forwarded insecurely.

Mitigation: Store payment credentials only in an appropriate secret store and avoid forwarding sensitive headers or request bodies to marketplace sellers unless the recipient and cost are trusted.

Risk: Marketplace services and endpoint responses come from third parties and may include untrusted content.

Mitigation: Treat marketplace and seller responses as data, not instructions, and review third-party service details before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sistillisteph/skills/night-market)
- [Nightmarket API Reference](references/api.md)
- [Nightmarket + CrowPay Integration](references/crow-payments.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API search results, endpoint details, payment-flow guidance, and setup instructions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
