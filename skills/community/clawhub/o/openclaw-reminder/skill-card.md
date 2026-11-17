## Description:

Create one-time reminder tasks using OpenClaw cron. User specifies reminder time and task content in natural language via Discord, and the task result will be sent back through Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyan](https://clawhub.ai/user/skyan)

### License/Terms of Use:


## Use Case:

External users and OpenClaw agents use this skill to schedule one-time Discord reminders from natural-language time and task requests. The skill creates an OpenClaw cron job that posts the eventual result back to the originating Discord context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder text is scheduled as a privileged main-session system event and the resulting output is sent back to Discord.

Mitigation: Review before installing, ask for confirmation before scheduling, treat reminder text as quoted data, and prefer an isolated low-privilege execution context where available.

Risk: Unsanitized user task content could alter shell command behavior when creating reminder jobs.

Mitigation: Validate task content with the included sanitizer before passing it to cron, and reject command substitution, shell metacharacters, double quotes, newlines, and dangerous command prefixes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skyan/skills/openclaw-reminder)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and concise confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw, the session_status tool, a Discord delivery context, future reminder times, and sanitized task content.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
