## Description:

快樂刷牙俠，讓孩子愛上刷牙的歡樂計時器與打卡系統

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT

## Use Case:

Parents, caregivers, and agents use this skill to run a positive two-minute brushing timer for young children, provide story or music encouragement, record brushing progress, award virtual stickers, and generate optional reminder or TTS text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local brushing history for a child may be saved under ~/.bookshelf-plus/kids.

Mitigation: Use a nickname when appropriate and remove the local JSON files if brushing history should be cleared.

Risk: Automatic reminder activation could create unexpected brushing prompts.

Mitigation: Avoid broad automatic activation and add scheduled reminders only after reviewing the printed cron lines or scheduler setup.

## Reference(s):

- [README](README.md)
- [Skill Instructions](SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/xuan905/skills/happy-brushing-hero)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus plain text or TTS-ready output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON brushing history, sticker, configuration, and reminder-state files under ~/.bookshelf-plus/kids when tracking or reminders are used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
