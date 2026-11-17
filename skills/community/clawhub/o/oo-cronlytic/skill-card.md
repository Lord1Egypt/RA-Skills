## Description:

Cronlytic (cronlytic.com). Use this skill for ANY Cronlytic request — reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage recurring HTTP jobs and review job schedules and execution logs in Cronlytic through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency setup may execute unverified downloaded code and add agent skills without clearly explaining those changes.

Mitigation: Review dependency setup, use a reviewed oo CLI release, and approve its local changes separately. Set OO_SKILLS_SYNC_DISABLED=1 if additional agent skills are unwanted.

Risk: Cronlytic write and destructive actions can change or remove jobs and logs.

Mitigation: Keep confirmation enabled for changes and deletions, and confirm the exact action and target before execution.

Risk: Cronlytic account access is brokered through the connected OOMOL account.

Mitigation: Proceed only when you trust OOMOL to broker access to the connected account.

## Reference(s):

- [Cronlytic homepage](https://www.cronlytic.com)
- [Cronlytic API documentation](https://www.cronlytic.com/api-documentation)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Cronlytic skill listing](https://clawhub.ai/oomol/skills/oo-cronlytic)
- [oo CLI command controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [Structured JSON action results with concise natural-language summaries; shell commands for setup and operation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Cronlytic account and the selected action.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
