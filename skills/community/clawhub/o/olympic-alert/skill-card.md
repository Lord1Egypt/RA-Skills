## Description:

Olympic Alert sends Korean-language reminders up to 15 minutes before configured Olympic events, supports schedule add and remove commands, and includes streaming links for 2026 Milano Cortina Winter Olympics Korean team defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garibong-labs](https://clawhub.ai/user/garibong-labs)

### License/Terms of Use:


## Use Case:

External users or agents use this skill to monitor configured Olympic schedules, notify users near event start time, list upcoming events, and maintain event entries for Korean-language Olympic coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script on heartbeat and writes a small notification history under ~/.config/olympic-alert.

Mitigation: Install it only when local heartbeat execution and this notification state file are acceptable for the environment.

Risk: Broad Olympic or Milan trigger phrases may activate the skill during ordinary sports-related conversations.

Mitigation: Review or narrow the trigger list before deployment if those terms are too broad for the agent's normal use.

Risk: Bundled event schedules and streaming links can become stale as Olympic schedules change.

Mitigation: Review scripts/events.json before use and update events with the documented add, remove, or direct edit workflow.

## Reference(s):

- [Olympic Alert on ClawHub](https://clawhub.ai/garibong-labs/skills/olympic-alert)
- [Naver Sports Milano Cortina 2026](https://m.sports.naver.com/milanocortina2026)
- [Chzzk Olympic Search](https://chzzk.naver.com/search?query=올림픽)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Korean text alerts and event lists, with Markdown links and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emits no-alert text when no event is due and includes configured streaming links when an alert is produced.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
