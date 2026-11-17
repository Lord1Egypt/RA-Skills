## Description:

Dida365 (dida365.com). Use this skill for ANY Dida365 request — reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Dida365 through an OOMOL-connected account use this skill to read and manage projects, tasks, habits, and check-ins, including creating, updating, completing, moving, and deleting records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded CLI code whose installer contents and remote connector behavior were not verified.

Mitigation: Review and approve CLI installation separately, preferably using a verified, pinned release.

Risk: Automatic skill synchronization can write skill files, and account actions can change or delete connected Dida365 data.

Mitigation: Review automatic synchronization and disable it with OO_SKILLS_SYNC_DISABLED if needed. Require approval for exact account changes and deletion targets.

## Reference(s):

- [Dida365 homepage](https://dida365.com)
- [Dida365 API documentation](https://developer.dida365.com/docs/index.html)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Dida365 ClawHub skill page](https://clawhub.ai/oomol/skills/oo-dida365)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, JSON]

**Output Format:** [Markdown guidance with oo CLI commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses may contain task, project, or habit data.]

## Skill Version(s):

1.0.9 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
