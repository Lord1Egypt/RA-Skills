## Description:

WorkOS (workos.com). Use this skill for ANY WorkOS request — reading, creating, updating, and deleting data. Whenever a task involves WorkOS, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the oo CLI to inspect and manage WorkOS organizations, users, and memberships through a connected OOMOL account. The workflow covers reads and state-changing actions, with user confirmation required before write or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified installers and make broader agent changes without clear approval.

Mitigation: Review setup before enabling, install a verified CLI release separately, approve local changes, and check or disable automatic skill synchronization using the CLI controls.

Risk: Connecting WorkOS gives OOMOL access to the selected account, and write or destructive actions can change account data or memberships.

Mitigation: Keep explicit approval requirements for account and membership changes, and inspect the live action schema before constructing a payload.

## Reference(s):

- [WorkOS](https://workos.com)
- [WorkOS API authentication documentation](https://workos.com/docs/reference/api-authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [WorkOS skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-workos)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with oo CLI commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action commands use the live connector schema; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
