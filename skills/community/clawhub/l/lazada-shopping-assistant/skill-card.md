## Description:

Lazada cross-site shopping assistant that guides users from intent to purchase by detecting the regional Lazada site, clarifying shopping scenarios, searching live listings, and presenting ranked recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gezhi-io](https://clawhub.ai/user/gezhi-io)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to compare Lazada products across supported regional sites and receive concise, ranked buying recommendations with prices, social proof, caveats, and product links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install unpinned browser automation components or an extra skill when no browser tool is available.

Mitigation: Use an already available trusted browser automation tool when possible; independently trust and pin any global npm package or extra skill before installing it.

Risk: Automated Lazada searches expose shopping intent and the workflow favors LazMall or Official Store results.

Mitigation: Tell users when LazMall or Official Store filtering is used, and broaden or change the search if the user wants non-official listings or a less promotional comparison.

Risk: Live scraped prices, sold counts, and availability can be incomplete or stale on dynamic Lazada pages.

Mitigation: Treat the recommendation as shopping guidance and ask the user to verify final price, seller, shipping, warranty, and return terms before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gezhi-io/skills/lazada-shopping-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, ranked recommendation sections, clickable product links, and occasional inline shell commands for browser automation setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on live Lazada page content and available browser automation.]

## Skill Version(s):

1.0.1 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
