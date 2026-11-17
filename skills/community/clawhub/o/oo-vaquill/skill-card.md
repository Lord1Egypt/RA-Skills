## Description:

Vaquill (vaquill.ai). Use this skill for ANY Vaquill request — reading, creating, updating, and deleting data. Whenever a task involves Vaquill, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Vaquill through an OOMOL-connected account can search and read statutory materials, resolve citations, inspect changes, and manage board watches through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI can install and refresh other agent skills without this skill explaining those changes.

Mitigation: Review the CLI's additional skill-management behavior before installing; consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking oo, and keep the required approvals for Vaquill changes.

## Reference(s):

- [Vaquill API documentation](https://www.vaquill.ai/docs/api-guide/authentication)
- [Vaquill](https://www.vaquill.ai)
- [oo CLI commands and settings](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Vaquill connector responses as JSON with explanatory text and oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected Vaquill action and connected account.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
