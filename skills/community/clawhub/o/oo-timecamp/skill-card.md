## Description:

Connects to TimeCamp to review and manage time entries, timers, tasks, and users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

TimeCamp account holders use the skill to review time entries, timers, tasks, and users, and to create or update time records after confirming the intended changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may introduce broader agent changes that are not explained by the skill.

Mitigation: Disable startup skill synchronization if unwanted, review and install the CLI separately, and keep approval enabled for edits.

Risk: The remote CLI installer and hosted service remain unverified.

Mitigation: Review the CLI before installation and connect only the intended TimeCamp account.

## Reference(s):

- [TimeCamp](https://www.timecamp.com)
- [TimeCamp API documentation](https://developer.timecamp.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, Guidance]

**Output Format:** [JSON responses and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some actions create, update, start, or stop time tracking and require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
