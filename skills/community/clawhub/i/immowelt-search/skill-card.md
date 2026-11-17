## Description:

Search immowelt.at and immowelt.de real estate listings via HTML parsing, including optional expose details such as heating type, energy source, building condition, year built, energy class, parking, and features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mihaimacarie98](https://clawhub.ai/user/mihaimacarie98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Austrian and German Immowelt property listings, apply price and room filters, and retrieve listing details for property search or reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes public web requests to Immowelt listing pages and can issue multiple requests when detail fetching is enabled.

Mitigation: Confirm the user intends an Immowelt search before running it, and use reasonable page limits and request pacing.

Risk: Listing data is parsed from public HTML and may be incomplete or stale if page structure or listing availability changes.

Mitigation: Treat returned property details as search assistance and verify important listing facts directly on Immowelt before making decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mihaimacarie98/skills/immowelt-search)
- [Immowelt Austria](https://www.immowelt.at)
- [Immowelt Germany](https://www.immowelt.de)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON emitted by a local Python command, with agent guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the requests library; outputs are based on public Immowelt HTML pages and may vary if page markup changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
