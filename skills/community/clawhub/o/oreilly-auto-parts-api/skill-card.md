## Description:

Retrieves O'Reilly Auto Parts cross-references, retail prices, product details, vehicle fitment, store availability, rebates, and promotions through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use an agent to cross-reference auto part numbers, review O'Reilly retail prices and product details, check vehicle fitment and nearby pickup availability, and find rebates or promotions.

### Deployment Geography for Use:

United States (Mexican store directory only)

## Known Risks and Mitigations:

Risk: VIN or ZIP lookups may send vehicle or location information to Scavio.

Mitigation: Before using VIN or ZIP lookups, confirm the user is comfortable sharing that information; omit those inputs when they are not needed.

## Reference(s):

- [Scavio O'Reilly API](https://scavio.dev/oreilly-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=oreilly-auto-parts-api)
- [O'Reilly Auto Parts](https://www.oreillyauto.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include part matches, store-specific prices, fitment, availability states, and current offer details.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
