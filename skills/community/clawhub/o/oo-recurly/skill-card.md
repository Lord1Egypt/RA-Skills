## Description:

Recurly (recurly.com). Use this skill for ANY Recurly request — reading, creating, and updating data. Whenever a task involves Recurly, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to read Recurly accounts, plans, and subscriptions, and to create or update supported account and billing records through their connected Recurly account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run remote installers without pinning a release, and the remote installer contents were unavailable for inspection.

Mitigation: Review installer contents and use a reviewed, pinned CLI release before installation.

Risk: Automatic skill syncing may make broader agent changes outside clear user control.

Mitigation: Review and control CLI installation and automatic syncing, and retain confirmation for every change.

Risk: The connected OOMOL account mediates access to business data in Recurly.

Mitigation: Connect only the Recurly permissions needed for the task.

## Reference(s):

- [Recurly API documentation](https://recurly.com/developers/api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Recurly skill release](https://clawhub.ai/oomol/skills/oo-recurly)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and shell commands, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve Recurly records; create and update actions change account data and require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
