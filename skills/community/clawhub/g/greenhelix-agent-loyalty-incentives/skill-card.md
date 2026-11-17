## Description:

Guides developers through designing machine-readable loyalty programs, rewards APIs, and incentive protocols that AI shopping agents can discover, evaluate, and redeem autonomously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce engineers use this guide to design agent-readable loyalty, rewards, identity-linking, incentive-negotiation, redemption, and settlement flows for AI shopping agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample API flows may create or mutate loyalty, identity, payment, and ledger records if adapted against a production GreenHelix account.

Mitigation: Test in the GreenHelix sandbox first and use an API key with only the minimum permissions needed for the exercise.

Risk: The guide references credentials for API access and a wallet address.

Mitigation: Provide only the intended GreenHelix API key and a public wallet address; never include private keys or unrelated secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-loyalty-incentives)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)
- [Schema.org](https://schema.org)

## Skill Output:

**Output Type(s):** [markdown, code, configuration, guidance]

**Output Format:** [Markdown guide with Python and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable educational content; examples reference GREENHELIX_API_KEY and WALLET_ADDRESS environment values.]

## Skill Version(s):

1.3.1 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
