## Description:

Clockify (clockify.me). Use this skill for ANY Clockify request — reading, creating, updating, and deleting data. Whenever a task involves Clockify, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Clockify through an OOMOL-connected account can ask the agent to read Clockify data or create, update, and delete supported projects, tasks, and time entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI installation can execute changing remote code without clearly requiring approval.

Mitigation: Review and approve CLI installation separately, preferably using a pinned, verified release; check its effects on other installed agent skills before first use.

Risk: Creating, updating, or deleting Clockify data changes the connected account.

Mitigation: Retain the skill's explicit confirmations for changes and deletions.

## Reference(s):

- [Clockify](https://clockify.me)
- [Clockify API documentation](https://docs.clockify.me/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Clockify skill on ClawHub](https://clawhub.ai/oomol/skills/oo-clockify)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON payloads and Clockify data, with shell command examples and setup guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change or delete Clockify data are identified and require user confirmation.]

## Skill Version(s):

1.0.5 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
