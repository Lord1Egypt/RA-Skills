## Description:

Proactive Trigger helps an agent decide when to initiate proactive engagement by evaluating user silence, topic heat, signal priority, and trigger timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoguoqiang-hub](https://clawhub.ai/user/zhaoguoqiang-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add proactive timing decisions to OpenClaw-style agents, including checks for silence duration, topic interest decay, cooldowns, daily limits, and pending signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports behavioral profiling of interaction timing, topics, responses, and possibly mood-related signals.

Mitigation: Require explicit user opt-in for proactive messaging and define retention, review, and deletion controls for OpenClaw .soul state and signal files.

Risk: The security evidence reports unsafe command execution wrappers around the OpenClaw CLI.

Mitigation: Review and harden the CLI wrapper before deployment, especially parameter handling and the trust boundary for any OpenClaw command invocation.

Risk: The skill can generate proactive messages based on inferred timing and topic signals, which may interrupt users or create unwanted engagement.

Mitigation: Keep daily limits, cooldowns, focus-mode checks, quiet hours, and user rejection learning enabled, and require a clear path to disable proactive contact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoguoqiang-hub/skills/proactive-trigger)
- [Interest graph calculation](references/interest-graph-calculation.md)
- [Silence index formula](references/silence-index-formula.md)
- [Trigger state management](references/trigger-state-management.md)
- [Chinese skill reference](references/SKILL.zh.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI text output and JSON-backed state or signal files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write trigger state, signal, context, and message log files under the configured OpenClaw workspace.]

## Skill Version(s):

0.4.0 (source: server release metadata; package.json reports 0.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
