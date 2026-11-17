## Description:

Regularly audits Hermes Agent self-improvement behavior, including skill changes, curator status, and memory-provider health, so users can spot unexpected agent evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freepengyang](https://clawhub.ai/user/freepengyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and teams operating Hermes Agent use this skill to schedule or trigger read-only audits of skill changes, curator behavior, usage patterns, memory-provider health, and configuration drift. The reports help users review agent self-modification and decide whether manual investigation or rollback is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled audit reports may run weekly and send operational details to a chat destination.

Mitigation: Confirm the cron schedule and use only trusted delivery targets before installing or enabling the skill.

Risk: Audit output may reveal skill names, curator status, and memory-provider configuration.

Mitigation: Limit report recipients to people authorized to view Hermes operational details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freepengyang/skills/hermes-self-audit)
- [ClawHub homepage metadata](https://clawhub.ai/freepengyang/hermes-self-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or chat-platform formatted audit report with inline shell commands and configuration checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also save a local audit log at ~/.hermes/logs/audit.log when used in a Hermes environment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
