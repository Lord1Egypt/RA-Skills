## Description:

Helps agents manage Gumroad storefront products, sales, subscribers, licenses, and webhooks through an authorized connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Storefront operators and developers use this skill to inspect Gumroad products and sales, verify licenses, and manage approved storefront changes and webhook automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Storefront writes, product deletion, and license changes can alter business data.

Mitigation: Confirm the account, exact resource, proposed change, and persistence with the user before acting.

Risk: Webhooks, hosted functions, and triggers can persist or send customer and payment data to unintended destinations.

Mitigation: Obtain approval for each automation and verify its payload, destination URL, and ongoing behavior before enabling it.

Risk: Long-lived API keys can expose account access if mishandled.

Mitigation: Prefer the Maton CLI OAuth flow over raw API keys.

## Reference(s):

- [Gumroad skill on ClawHub](https://clawhub.ai/byungkyu/skills/gumroad)
- [Publisher profile](https://clawhub.ai/user/byungkyu)
- [Maton](https://maton.ai)
- [Related API gateway skill](https://clawhub.ai/byungkyu/api-gateway)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Gumroad account and customer data returned by authorized requests.]

## Skill Version(s):

1.2.5 (source: server-resolved ClawHub release; skill frontmatter says 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
