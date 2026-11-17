## Description:

Use when a new user messages the bot for the first time or sends /start. Guides them through conversational onboarding - organization setup, industry, language, priorities - entirely via Telegram chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rithythul](https://clawhub.ai/user/rithythul)

### License/Terms of Use:

MIT-0

## Use Case:

External users and organization operators use this skill to complete first-run Nimmit setup through Telegram chat. It gathers organization details, language preference, team size, and priorities, then configures the workspace and onboarding checklist for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to make persistent workspace changes during onboarding without clearly exposing the full scope to the user.

Mitigation: Require an explicit confirmation step that lists the files to be changed before setup actions are executed.

Risk: The skill may install additional skill packs as part of setup.

Mitigation: Restrict installation to an approved allowlist and disclose the selected skill packs before installation.

Risk: The skill may create a recurring daily briefing schedule.

Mitigation: Disclose the schedule, timezone, and removal steps, and allow the user to opt out before creating the job.

Risk: The security verdict is suspicious because consent, scope, audit trail, and rollback behavior are not clear.

Mitigation: Review the skill before installing and ask the publisher for exact changed files, cron details, confirmation prompts, audit logging, and rollback instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rithythul/skills/nimmit-onboarding)

## Skill Output:

**Output Type(s):** [guidance, text, configuration, shell commands]

**Output Format:** [Conversational text with agent actions for workspace file updates, skill-pack installation, and scheduled briefing setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat-based onboarding flow with Khmer and English language handling]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
