## Description:

Search koopje.ai for Belgian second-hand deals and auctions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antarcticaice](https://clawhub.ai/user/antarcticaice)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask an agent to find Belgian second-hand listings or auction lots. The agent summarizes matching items with prices, locations, sources, and links.

### Deployment Geography for Use:

Belgium

## Known Risks and Mitigations:

Risk: Search queries, follow-up context, and location details are sent to koopje.ai.

Mitigation: Share only information needed for the search; prefer a postcode over precise coordinates unless the user asks for distance filtering.

Risk: Account features can save listings, publish public ads, and send recurring reminder emails.

Mitigation: Use these actions only when explicitly requested and confirm before every creation, publication, update, or deletion route, including direct ad creation.

## Reference(s):

- [koopje.ai /v1 API reference](references/api.md)
- [koopje.ai API documentation](https://koopje.ai/api#mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with linked listings, prices, locations, and sources]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Auction listings may not have fixed prices.]

## Skill Version(s):

1.0.23 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
