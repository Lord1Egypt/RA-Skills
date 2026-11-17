## Description:

Workpath (workpath.com). Use this skill for ANY Workpath request — searching and reading data. Whenever a task involves Workpath, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to retrieve goals, key results, teams, and users from their connected Workpath account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to run remote installation code whose full effects are outside the reviewed package.

Mitigation: Verify the CLI version and installation source separately, and require user approval before setup.

Risk: OOMOL mediates access to the connected Workpath account, and the CLI may install or update agent skills.

Mitigation: Review the account connection and any proposed skill changes before authorizing them.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Workpath Connect API documentation](https://developer.workpath.com/docs/connect-api-doc/ZG9jOjM2MjI2-welcome-to-connect-api)
- [Workpath homepage](https://www.workpath.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's connected Workpath account to retrieve requested data.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
