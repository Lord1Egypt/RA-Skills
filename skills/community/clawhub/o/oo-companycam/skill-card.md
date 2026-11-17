## Description:

Lets an agent read and manage CompanyCam projects, tags, users, and company details through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

CompanyCam users can use the skill to retrieve company, project, tag, and user information, and to create or manage projects and tags from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses downloads and may automatically install or synchronize skills into other agents; these behaviors were not verified.

Mitigation: Review and install a verified CLI release before use, and check its automatic skill installation and synchronization settings.

Risk: CompanyCam data passes through OOMOL, and write or destructive actions can change connected account data.

Mitigation: Use the connected account with awareness of this data path; confirm the exact effect of write actions and get explicit approval for destructive actions.

## Reference(s):

- [CompanyCam release on ClawHub](https://clawhub.ai/oomol/skills/oo-companycam)
- [CompanyCam](https://companycam.com)
- [CompanyCam API documentation](https://companycam.readme.io/docs/getting-started)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [Structured JSON results with concise natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can retrieve account data or request changes to projects and tags.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
