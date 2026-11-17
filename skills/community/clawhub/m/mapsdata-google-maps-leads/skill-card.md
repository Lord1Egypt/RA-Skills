## Description:

Search Google Maps businesses through Mapsdata or enrich supplied companies with business details, contact information, and CSV-ready leads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vagif12](https://clawhub.ai/user/vagif12)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and prospecting teams use this skill to find local businesses or enrich existing company lists with Mapsdata business and contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Mapsdata API key is required and could be exposed if copied into output or files.

Mitigation: Provide the key through the MAPSDATA_API_KEY environment variable; do not print or persist it.

Risk: Creating search or enrichment jobs may consume lead credits.

Mitigation: Check account balance and limits first, and confirm scope before creating jobs unless the user has already authorized it.

Risk: Enriched contact data may be subject to privacy, marketing, and platform rules.

Mitigation: Handle leads according to applicable rules and require explicit permission before outreach or sharing beyond the requested destination.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/vagif12/skills/mapsdata-google-maps-leads)
- [Mapsdata homepage](https://www.mapsdata.io)
- [Mapsdata API documentation](https://www.mapsdata.io/docs)
- [Mapsdata data fields](https://www.mapsdata.io/docs/reference/data-fields)
- [Mapsdata plans and credits](https://www.mapsdata.io/docs/reference/plans-and-credits)
- [Mapsdata API access](https://www.mapsdata.io/api-access)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV-ready data, Shell commands]

**Output Format:** [Markdown summaries and tables, CSV-ready rows, or shell examples as requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes job status, lead counts, credit usage, and email verification status when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
