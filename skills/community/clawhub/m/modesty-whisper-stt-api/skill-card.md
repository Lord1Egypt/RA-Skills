## Description:

Provides agent instructions for using OpenAI Whisper speech-to-text through SkillBoss with an OpenAI-compatible API and a SkillBoss API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and call Whisper speech-to-text through SkillBoss, including setup guidance, curl examples, and Python examples. It is intended for users who want a SkillBoss API key as an intermediary for Whisper access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path may enable a broad SkillBoss API gateway beyond the stated Whisper transcription purpose.

Mitigation: Install only when broad SkillBoss platform access is intended; prefer a narrowly scoped Whisper-only configuration or key when available.

Risk: Requests and bearer tokens are sent to SkillBoss as an intermediary.

Mitigation: Use a dedicated SkillBoss API key, avoid sharing unrelated credentials, and review SkillBoss handling requirements before sending sensitive audio.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/skills/modesty-whisper-stt-api)
- [SkillBoss Setup](https://skillboss.co/skill.md)
- [SkillBoss Console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=whisper-stt-api)
- [SkillBoss Products](https://skillboss.co/products)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, curl, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and routes transcription requests through SkillBoss.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
