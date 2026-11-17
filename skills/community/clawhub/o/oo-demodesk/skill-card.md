## Description:

Demodesk (demodesk.com). Use this skill for ANY Demodesk request — searching and reading data. Whenever a task involves Demodesk, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents handling user requests to find and read Demodesk data can list recordings and users, retrieve recordings and transcripts, and read recording scorecards and summaries through the user's connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can persistently change skills used by other agents without the skill clearly explaining that impact.

Mitigation: Review and deliberately install a trusted CLI release. Disable or explicitly approve cross-agent skill synchronization, and connect only the intended Demodesk account. Requests pass through OOMOL, and the external installers and exact installed CLI behavior remain unverified.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Demodesk API documentation](https://demodesk.com/api/docs/index.html)
- [Demodesk](https://demodesk.com)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Demodesk records and related data returned as JSON, with text summaries when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results depend on the connected Demodesk account and requested action.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
