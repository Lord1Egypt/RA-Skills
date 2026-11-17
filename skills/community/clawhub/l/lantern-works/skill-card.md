## Description:

Look up tracked GPU rental prices and work-stack deals through the Lantern Works hosted MCP server or public JSON API, with vendor links, check dates, price changes, and referral links flagged.

This skill is ready for commercial/non-commercial use.

## Publisher:

[connormatthewdouglas](https://clawhub.ai/user/connormatthewdouglas)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and teams can compare tracked GPU rental prices, estimate job or monthly stack costs, and find work-stack tool deals. They can use the listed vendor source links and check dates to evaluate current options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local package command is not pinned to a reviewed version, so a later release may change what runs.

Mitigation: Prefer the hosted MCP server or public JSON API; if using the local command, review the package release and pin an appropriate version.

## Reference(s):

- [Lantern Works installation and overview](https://thelanternworks.com/install/?ref=clawhub)
- [Hosted Lantern Works MCP server](https://lantern-works-mcp.lantern-works.workers.dev/mcp?ref=clawhub)
- [GPU rental prices JSON API](https://thelanternworks.com/api/v1/gpu-prices.json?ref=clawhub)
- [GPU price changes JSON API](https://thelanternworks.com/api/v1/gpu-price-changes.json?ref=clawhub)
- [Work-stack deals JSON API](https://thelanternworks.com/api/v1/deals.json?ref=clawhub)
- [ClawHub skill page](https://clawhub.ai/connormatthewdouglas/skills/lantern-works)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured tool results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results cover tracked providers and may include vendor source links, verification dates, and affiliate flags.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
