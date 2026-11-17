## Description:

Create and preview leases, property notices, rent rolls, purchase agreements, and other real estate documents with Pressmark. Built by Moosh Works (https://mooshworks.com).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mooshee](https://clawhub.ai/user/mooshee)

### License/Terms of Use:

MIT-0

## Use Case:

Real estate agents, landlords, and property managers use the skill to preview and generate leases, notices, management statements, rent rolls, purchase agreements, deeds, and related property documents through Pressmark.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured customer sync may record party contact details and a document summary and start automated follow-up.

Mitigation: Review Pressmark privacy and sync settings before entering real party or property details; use a guest session and synthetic contact details for testing.

Risk: A generated document may not include every requirement for its jurisdiction.

Mitigation: Review the applicable state and local profile and check the generated document against local requirements, preserving any missing or uncertain jurisdiction details.

## Reference(s):

- [Real estate calculations and disclosure fields](references/statutory-clauses.md)
- [Pressmark Studio](https://pressmark.dev)
- [Supported state profiles](https://pressmark.dev/api/v1/states)
- [Residential lease template](https://pressmark.dev/templates/residential-lease)
- [California residential lease template](https://pressmark.dev/templates/california-residential-lease)
- [Commercial NNN lease template](https://pressmark.dev/templates/commercial-nnn-lease)
- [Closing settlement statement template](https://pressmark.dev/templates/closing-settlement-statement)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [PDF real estate documents and text previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents use user-supplied terms and applicable template profiles.]

## Skill Version(s):

1.2.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
