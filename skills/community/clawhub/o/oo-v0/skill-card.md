## Description:

Operate v0 through an OOMOL-connected account to manage chats, projects, deployments, environment variables, hooks, and related data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect and manage v0 chats, projects, deployments, and settings through their connected v0 account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs unverified remote code and may change agent skills without clearly disclosing the scope.

Mitigation: Review setup first, install a verified CLI release yourself, and disable startup skill synchronization.

Risk: Actions can change or delete v0 workspace data.

Mitigation: Connect only the needed v0 permissions and retain confirmation for writes and deletions.

## Reference(s):

- [v0 API documentation](https://v0.dev/docs/api)
- [v0](https://v0.dev)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with oo CLI commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live action schemas; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
