## Description:

Pivotal Tracker (pivotaltracker.com). Use this skill for ANY Pivotal Tracker request — reading, creating, and updating data. Whenever a task involves Pivotal Tracker, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to read Pivotal Tracker projects and stories, create stories or comments, and update story state through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote installer code without a clear approval step.

Mitigation: Review the installer and verify the CLI version before installation; check whether installation also installs agent skills, and confirm Pivotal Tracker changes before running write actions.

## Reference(s):

- [Pivotal Tracker skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-pivotal-tracker)
- [Pivotal Tracker](https://www.pivotaltracker.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON connector responses and Markdown usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON responses include action data and an execution ID.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
