## Description:

Search Indeed job postings by keyword and location via RolesAPI.com, returning job listings as JSON with filters for postings from today, this week, or remote-only across 60+ country editions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Indeed listings by keyword, location, country edition, recency, and remote status. It is intended for explicit job-search requests and returns structured job-listing data that can be reviewed or passed to related Indeed detail skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job-search keywords and optional locations are sent to RolesAPI.

Mitigation: Use the skill only for searches where sending those terms to RolesAPI is acceptable.

Risk: Search requests consume RolesAPI credits, especially when fetching multiple pages.

Mitigation: Set conservative page limits for exploratory scans and monitor account usage.

Risk: The skill requires a RolesAPI key for authenticated API access.

Mitigation: Keep ROLESAPI_KEY scoped to this service and revoke it when it is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nikhonit/skills/indeed-search)
- [RolesAPI](https://rolesapi.com)
- [RolesAPI Pricing](https://rolesapi.com/pricing/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON responses from Python scripts, with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search calls consume RolesAPI credits; preset scripts can fetch up to 3 pages per call.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
