## Description:

Create or update a pawr.link profile. $9 USDC self-service (instant) or $10 curated (AI-built, ~1 min). Free profile discovery API. All payments via x402 on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baseddesigner](https://clawhub.ai/user/baseddesigner)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to create, update, or discover public pawr.link profiles with links, social embeds, token widgets, and machine-readable agent data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Create, curated-create, and update examples can trigger paid x402 actions when run through a compatible wallet client.

Mitigation: Review endpoint paths, prices, and wallet behavior before executing requests, and treat those examples as payment-authorized actions.

Risk: Profile details, links, email addresses, descriptions, and curated-profile inputs may be processed by pawr.link and published on a public profile.

Mitigation: Only submit information that is appropriate for public display and acceptable to process through pawr.link.

## Reference(s):

- [pawr.link](https://pawr.link)
- [pawr.link ClawHub listing](https://clawhub.ai/baseddesigner/skills/pawr-link)
- [x402](https://www.x402.org/)
- [Bankr SDK documentation](https://docs.bankr.bot/)
- [pawr.link Agent Card](https://pawr.link/.well-known/agent.json)
- [pawr.link LLM context](https://pawr.link/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON, Markdown]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces curl examples and field guidance for paid x402 profile create/update requests and free profile discovery.]

## Skill Version(s):

4.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
