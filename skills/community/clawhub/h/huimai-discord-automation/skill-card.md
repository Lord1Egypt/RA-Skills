## Description:

Automates routine Discord community administration tasks including auto-replies, role and channel management, cleanup, logging, moderation workflows, activity summaries, and multilingual welcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External Discord community administrators, project community operators, and game guild managers use this skill to reduce repetitive moderation, onboarding, channel maintenance, role assignment, and reporting work. Treat action results as unconfirmed unless the skill is connected to real Discord API calls with permission checks and audit records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may simulate successful Discord moderation actions, creating false confidence that messages, roles, users, or channels were actually changed.

Mitigation: Use it for operational moderation only after real Discord API integration confirms each action, validates bot permissions, and records auditable outcomes.

Risk: Automated destructive actions such as deletion, kicks, mutes, or channel cleanup can affect community access and records if enabled without controls.

Mitigation: Require explicit confirmation, scoped permissions, backups or logs, and reviewable moderation rules before enabling destructive actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/huimai-discord-automation)
- [Publisher profile](https://clawhub.ai/user/yezhaowang888-stack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands and JSON-like operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report simulated success for Discord actions; operational users should require API-confirmed results and audit logging.]

## Skill Version(s):

2.0.0 (source: server release evidence, created 2026-05-03; artifact changelog also lists v2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
