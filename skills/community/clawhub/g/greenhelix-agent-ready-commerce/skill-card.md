## Description:

A guide for retrofitting commerce APIs and storefront data so AI buying agents can discover products, evaluate structured feeds, and complete checkout through UCP, ACP, x402, and GreenHelix payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, API teams, and commerce operators use this skill to plan agent-discoverable storefronts, structured product feeds, marketplace listings, and payment workflows for AI buyers. It is a non-executable Markdown guide with illustrative production-style examples that should be adapted with credential and payment safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide asks users to configure high-value commerce credentials, including GreenHelix, wallet, signing, and Stripe-related values.

Mitigation: Use sandbox or test credentials by default, avoid supplying Stripe keys or agent signing private keys unless required, and scope any credentials to the minimum needed workflow.

Risk: Production-style payment examples could become live, state-changing payment flows when adapted directly.

Mitigation: Add endpoint allowlisting, dry-run modes, spending caps, and human confirmation before using adapted examples in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-ready-commerce)
- [GreenHelix sandbox endpoint](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)
- [Schema.org structured data reference](https://schema.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guide with inline Python, JSON, YAML, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable educational guide; examples reference GreenHelix, wallet, signing, and Stripe credentials supplied by the user.]

## Skill Version(s):

1.3.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
