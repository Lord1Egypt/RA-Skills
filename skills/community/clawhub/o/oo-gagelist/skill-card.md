## Description:

GageList (gagelist.com). Use this skill for ANY GageList request — reading, creating, updating, and deleting data. Whenever a task involves GageList, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use an agent to inspect GageList account settings, status, gage and calibration records, and manufacturers, and to create, update, or delete manufacturer records through their connected account. Confirm write and delete actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency may install or synchronize additional agent skills beyond the requested task.

Mitigation: Review and install a verified CLI release. Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if additional skills should not be installed or synchronized.

Risk: Actions through the connected GageList account can change or delete account records.

Mitigation: Connect only the intended GageList account and retain approval for write and delete actions; confirm the target and effect before execution.

## Reference(s):

- [GageList homepage](https://gagelist.com/)
- [GageList API documentation](https://gagelist.com/developer-resources/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [GageList Skill on ClawHub](https://clawhub.ai/oomol/skills/oo-gagelist)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [Structured JSON connector results with text or Markdown summaries and shell command instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read account data or change manufacturer records; confirm write and delete actions before execution.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
