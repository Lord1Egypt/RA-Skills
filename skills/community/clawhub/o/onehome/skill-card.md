## Description:

Search OneHome (CoreLogic) portal listings, get property details, photos, schools, saved searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Buyers and other OneHome users can search listings shared by their real-estate agent, review property details, photos, schools and saved searches, and compare properties. The skill also provides local mortgage and affordability estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens and OneHome magic links grant account access.

Mitigation: Use a trusted OneHome MCP server and protect tokens and magic links like passwords.

Risk: Browser capture uses access from the user's signed-in OneHome session.

Mitigation: Use browser capture only with a trusted server and a session the user intends to share.

Risk: Compact mode removes media URLs but retains personal account information.

Mitigation: Do not treat compact results as anonymized or free of personal information.

## Reference(s):

- [OneHome skill release](https://clawhub.ai/chrischall/skills/onehome)
- [OneHome portal](https://portal.onehome.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Property listing data, Numeric estimates]

**Output Format:** [Structured listing and property data, concise text summaries, and mortgage or affordability estimates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Listing results depend on the user's OneHome account access and selected view.]

## Skill Version(s):

1.2.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
