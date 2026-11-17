## Description:

One-shot reminders via natural language that auto-detect channel and timezone, then ping the user when the reminder is due.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethan-shen-individual-lab](https://clawhub.ai/user/ethan-shen-individual-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to create, list, cancel, and configure one-shot reminders for users across OpenClaw-supported chat channels. It is intended for users who want natural-language reminder scheduling with automatic channel and timezone handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cancellation command can remove unrelated OpenClaw scheduled jobs if supplied an ID for another job.

Mitigation: List reminders first, verify the target job is a ping-me reminder, and avoid cancelling arbitrary or ambiguous job IDs until cancellation scoping is fixed.

Risk: The README includes an unpinned npx install command.

Mitigation: Prefer the ClawHub install path or a pinned installer/version for controlled installs.

Risk: Some announce channels require an explicit delivery target, and reminders may fail if that target is missing.

Mitigation: Configure the default channel and delivery target during first-time setup for target-required channels such as QQ Bot.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ethan-shen-individual-lab/skills/ping-me)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise text confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates, lists, cancels, and configures OpenClaw cron reminders; reminder jobs are intended to delete after firing.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
