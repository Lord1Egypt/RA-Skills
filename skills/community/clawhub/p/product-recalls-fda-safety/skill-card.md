## Description:

Product Recalls & FDA Safety Alerts helps agents look up FDA drug recalls, medical device recalls, 510(k) clearances, drug approvals, and labels by company or keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external compliance, safety, and supplier-risk teams use this skill to monitor FDA recall and product safety signals for companies, products, or topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes paid x402 API calls, so an agent or wallet runtime could spend funds while performing lookups.

Mitigation: Configure spending visibility and caps before use.

Risk: The skill depends on a third-party GoCreative API provider for FDA data lookup responses.

Mitigation: Confirm the provider is acceptable for the intended workflow before installing or enabling the skill.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/colinhughes2121/skills/product-recalls-fda-safety)
- [GoCreative API Base URL](https://api.gocreativeai.com)
- [Publisher Profile](https://clawhub.ai/user/colinhughes2121)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance describing HTTPS GET endpoints that return JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses disclosed x402 USDC pay-per-call requests; no API key or signup is described.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
