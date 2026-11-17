## Description:

Use when you need the price of a product or service, or have observed a price worth recording; PriceClaw searches crowdsourced price data, submits new price observations, and votes on existing entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roundtoo](https://clawhub.ai/user/roundtoo)

### License/Terms of Use:

MIT-0

## Use Case:

External agents use PriceClaw to search crowdsourced prices for products and services, submit newly observed prices, and corroborate or report existing entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The direct-token authentication path can expose a GitHub, Google, or Discord access token to the agent.

Mitigation: Prefer the browser OAuth setup and do not paste provider access tokens into the agent unless the user explicitly chooses that path.

Risk: Persisting the PriceClaw API key stores a reusable credential in OpenClaw configuration.

Mitigation: Ask for user confirmation before writing the key, store only PRICECLAW_API_KEY in the documented config locations, and avoid logging or sharing the key.

Risk: Price submissions, votes, edits, and reports affect shared crowdsourced data.

Mitigation: Search for existing places and prices first, vote when an entry matches, and only create or force-create entries after reviewing duplicate and outlier warnings.

## Reference(s):

- [PriceClaw homepage](https://priceclaw.io)
- [PriceClaw API docs](https://priceclaw.io/docs)
- [PriceClaw ClawHub listing](https://clawhub.ai/roundtoo/skills/priceclaw)
- [RoundToo publisher profile](https://clawhub.ai/user/roundtoo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP examples, JSON request bodies, shell commands, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read public PriceClaw price data without authentication; writes, votes, and persisted agent history require PRICECLAW_API_KEY.]

## Skill Version(s):

1.2.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
