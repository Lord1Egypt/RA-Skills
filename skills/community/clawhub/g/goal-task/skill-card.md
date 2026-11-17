## Description:

Goal Task helps an agent create a delayed, goal-oriented cron task, act on the task when triggered, and delete the cron job after completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to schedule delayed follow-up tasks or reminders for an OpenClaw agent, then remove the cron job once the goal is complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper reads the local OpenClaw gateway token and can create, update, and delete persistent remote cron jobs.

Mitigation: Install and run it only in environments where that token access and remote scheduling behavior are acceptable, and check for stale goal-task cron jobs after use.

Risk: Crafted task text can cause unintended local code execution during the script's JSON/Python construction.

Mitigation: Do not pass untrusted task text to goal_task until the JSON/Python construction is fixed.

## Reference(s):

- [Goal Task on ClawHub](https://clawhub.ai/axelhu/skills/goal-task)
- [axelhu ClawHub publisher profile](https://clawhub.ai/user/axelhu)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command output strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The sourced shell helper returns a cron job ID for created goal tasks and an ok/error-style result for deletion.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
