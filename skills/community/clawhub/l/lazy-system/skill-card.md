## Description:

Lazy System is a bilingual productivity skill that uses an agent as an external anchor for proactive daily habit check-ins and minimum viable actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcii](https://clawhub.ai/user/0xcii)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to set up an agent-driven habit execution system that asks for daily check-ins, tracks streaks in memory, and supports recovery after missed days.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may start the skill when the user did not intend to begin a habit check-in flow.

Mitigation: Use specific triggers such as "lazy system" or "懒人系统" when invoking or configuring the skill.

Risk: Recurring reminders may continue after the user no longer wants the habit system.

Mitigation: Review and remove the Hermes cron job when the user pauses or stops using the system.

Risk: Habit state and progress are stored in Hermes memory.

Mitigation: Install only when persistent progress tracking is desired, and remove the related memory entry when it is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xcii/skills/lazy-system)
- [0xcii Publisher Profile](https://clawhub.ai/user/0xcii)
- [Hermes Agent](https://hermes-agent.nousresearch.com)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown conversation responses with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses scheduled check-ins and persistent memory entries when installed in Hermes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
