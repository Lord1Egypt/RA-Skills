## Description:

Automates Blue World Marketing morning standups by preparing Slack transcript processing, task assignment, immediate agent delegation, memory updates, and summary reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and marketing teams use this skill to turn weekday morning standup discussion into task assignments, agent-routed follow-up work, meeting notes, and Slack-ready status summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slack meeting text may be converted into actions across business systems without enough approval or scope control.

Mitigation: Require human approval before external, destructive, financial, infrastructure, publishing, customer-facing, or credential-related actions.

Risk: Untrusted channel content could influence task routing or meeting memory.

Mitigation: Use the skill only with trusted Slack channels and run the hosting agent with strict permissions.

Risk: Transcript-derived notes may be mistaken for approved task state.

Mitigation: Keep raw transcript-derived memory separate from reviewed and approved task records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blueworldmarketing/skills/morning-meeting-bwm)
- [Publisher profile](https://clawhub.ai/user/blueworldmarketing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown meeting summaries and task lists, Slack-ready text reports, and shell command output for local setup paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated meeting notes and active task state to local memory paths when used by a hosting agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
