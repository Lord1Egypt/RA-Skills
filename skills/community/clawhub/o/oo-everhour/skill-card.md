## Description:

Everhour (everhour.com). Use this skill for ANY Everhour request — reading, creating, updating, and deleting data. Whenever a task involves Everhour, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with an OOMOL-connected Everhour account use this skill to read projects, tasks, users, time records, and timer status, and to create time records or manage timers. It guides the agent to check the live action schema before sending connector requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup and its remote installer payload and hosted service were not verified; CLI setup may also install or update other agent skills.

Mitigation: Review and install a verified CLI release separately. Check for skill synchronization and use OO_SKILLS_SYNC_DISABLED to disable it if needed.

## Reference(s):

- [Everhour](https://everhour.com)
- [Everhour API Documentation](https://everhour.docs.apiary.io/)
- [oo CLI Command Reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Everhour ClawHub Skill](https://clawhub.ai/oomol/skills/oo-everhour)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON connector requests and responses with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads follow the live connector schema; writes and destructive actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
