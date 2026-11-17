## Description:

Transcribes audio to text through SkillBoss API Hub using Whisper-powered speech recognition, with optional audio translation to English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit selected audio files to SkillBoss API Hub for speech-to-text transcription or English translation without downloading local models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio files and filenames selected for transcription are sent to SkillBoss API Hub for processing.

Mitigation: Avoid confidential, regulated, or consent-sensitive recordings unless vendor approval and data-handling requirements are in place.

Risk: The skill requires a SkillBoss API key for API access.

Mitigation: Store SKILLBOSS_API_KEY in a secure environment variable and do not hardcode it in source files or prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/godfery-transcribe)
- [SkillBoss API Hub](https://api.skillbossai.com)
- [SkillBoss setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with Python examples and API response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends selected audio data and filenames to SkillBoss API Hub.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
