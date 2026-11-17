## Description:

Proactive daily planning assistant that helps organize your day, track tasks, and provide motivation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akshaymemane](https://clawhub.ai/user/akshaymemane)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate daily planning prompts, check progress during the day, receive motivational text, and produce evening review guidance for an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily planning files can contain sensitive personal or work details.

Mitigation: Protect the OpenClaw memory directory and periodically delete saved plans that should not persist.

Risk: Optional cron or HEARTBEAT automation can run the planner on a recurring schedule.

Mitigation: Enable recurring automation only when scheduled daily planner runs are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akshaymemane/skills/proactive-daily-planner)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown planning templates and terminal text with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local daily plan Markdown files under the user's OpenClaw memory directory.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
