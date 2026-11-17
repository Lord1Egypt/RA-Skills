## Description:

Orchestrate a PM bot and one or more Dev bots in a private Telegram group, turning structured chat commands into Dev-side ClawHub skill management and OpenClaw cron actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiril-shturman](https://clawhub.ai/user/kiril-shturman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a controlled Telegram-to-OpenClaw workflow for installing or updating ClawHub skills and managing OpenClaw cron jobs from approved PM bot commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included executor can perform high-impact skill and cron changes without enforcing the Telegram authorization checks described by the skill.

Mitigation: Deploy only where Telegram chat and sender identity are enforced before commands reach the executor, and run the executor account with limited privileges.

Risk: Skill installation and update commands can change agent behavior on the Dev server.

Mitigation: Restrict installs and updates to approved, pinned packages and review changes before enabling them in a production workflow.

Risk: Cron creation can schedule repeated agent work from chat-provided messages.

Mitigation: Limit who can create cron jobs, review scheduled prompts, and monitor or disable jobs that create unsafe or unwanted actions.

Risk: The optional script uses temporary-file handling for cron job creation.

Mitigation: Harden temporary-file handling before production use, or prefer the documented Dev bot behavior contract with explicit authorization checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kiril-shturman/skills/pm-dev-orchestrator)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code]

**Output Format:** [Markdown guidance with JSON configuration, shell commands, command syntax, and a Python executor scaffold]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes short OK/ERR response conventions for Dev bot command handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
