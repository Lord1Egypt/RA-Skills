## Description:

Bitwarden (bitwarden.com). Use this skill for ANY Bitwarden request — searching and reading data. Whenever a task involves Bitwarden, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and organization administrators use this skill to read Bitwarden organization data, including collections, groups, members, policies, audit events, and subscription capacity, through an OOMOL-connected account. It guides the agent to check each action's schema before making a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions may execute unverified remote code without a clear approval step; the remote installers and connector implementation were not verified.

Mitigation: Verify the CLI release independently before use, require approval before installation or changes to other agent skills, connect only the Bitwarden permissions needed, and consider OOMOL's handling of credentials and organization data.

## Reference(s):

- [Bitwarden API documentation](https://bitwarden.com/help/bitwarden-apis/)
- [Bitwarden](https://bitwarden.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only organization data such as collections, groups, members, policies, audit events, and subscription details.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
