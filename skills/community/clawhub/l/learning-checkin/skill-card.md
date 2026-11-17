## Description:

Daily learning habit builder with check-ins and smart reminders

This skill is ready for commercial/non-commercial use.

## Publisher:

[daizongyu](https://clawhub.ai/user/daizongyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to record daily learning check-ins, view streak status, and receive optional reminder guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Undocumented scheduled-job output can record check-ins automatically.

Mitigation: Do not use the setup-cron output as written; configure reminders to call reminder or message flows only, and require explicit learning-checkin wording or confirmation before recording a check-in.

Risk: The skill creates local habit data files in the skill folder.

Mitigation: Tell users before initialization that records, reminder status, and reminder logs are stored locally, and treat those files as user data.

Risk: The current init path appears to reference an undefined get_welcome_message helper.

Mitigation: Review or patch initialization before relying on first-run setup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daizongyu/skills/learning-checkin)
- [Project Repository](https://github.com/daizongyu/learning-checkin)
- [Project Releases](https://github.com/daizongyu/learning-checkin/releases)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command results with human-facing text or Markdown responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local habit data files in the skill data folder for records, reminder status, and reminder logs.]

## Skill Version(s):

3.1.0 (source: release evidence, artifact README, SKILL.md, and script VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
