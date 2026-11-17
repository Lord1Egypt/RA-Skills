## Description:

Use this skill to read, create, update, or delete New Relic data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to query New Relic data and manage alerts, dashboards, deployment markers, synthetic monitors, credentials, and entity searches through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded CLI code that has not been verified.

Mitigation: Review and verify the CLI installation source before allowing setup.

Risk: The CLI may install additional persistent agent skills during startup synchronization.

Mitigation: Review proposed skills and use OO_SKILLS_SYNC_DISABLED=1 to suppress startup synchronization when appropriate.

Risk: Actions can modify or delete New Relic resources and credentials.

Mitigation: Use narrowly scoped credentials and require the documented approvals for changes and deletions.

## Reference(s):

- [New Relic API documentation](https://docs.newrelic.com/docs/apis/intro-apis/introduction-new-relic-apis/)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and shell commands with usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected New Relic action; writes and deletions require user approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
