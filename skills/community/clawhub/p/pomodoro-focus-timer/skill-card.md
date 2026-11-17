## Description:

Pomodoro Focus Timer helps users break tasks into Pomodoro work sessions with focus intervals, short breaks, and productivity tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn a task or work/study goal into a Pomodoro session plan with focus rounds, breaks, timer settings, and a concise status message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill primarily handles Chinese-language Pomodoro prompts and may provide limited handling for non-Chinese input.

Mitigation: Use clear Chinese task and duration phrasing, and review generated plans when prompts use other languages.

Risk: Generic timer or work-planning requests may activate the skill more broadly than intended.

Mitigation: Review activation triggers during deployment and route only Pomodoro or focused work-planning requests to this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/pomodoro-focus-timer)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object containing the task, Pomodoro plan, timer settings, and message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local planning output; no evidence of unsafe access, persistence, or data exfiltration.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
