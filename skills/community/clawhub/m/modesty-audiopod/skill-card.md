## Description:

Audiopod helps agents use SkillBoss API Hub for AI music generation, text-to-speech, speech-to-text transcription, stem separation, noise reduction, and speaker separation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to have an agent prepare SkillBoss API calls for generating or processing audio, including music, speech, transcription, stem separation, noise reduction, and speaker diarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio, media URLs, generated lyrics, text, and transcripts are sent to SkillBoss for processing.

Mitigation: Avoid confidential meetings, private voice recordings, regulated data, or third-party audio unless you have permission and understand SkillBoss handling and retention terms.

Risk: The skill requires a SkillBoss API key to authorize requests.

Mitigation: Store SKILLBOSS_API_KEY as an environment variable or managed secret and do not place it in prompts, logs, or shared files.

## Reference(s):

- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [Stem Separation Reference](references/stems.md)
- [Text to Speech Reference](references/tts.md)
- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-audiopod)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python and cURL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SKILLBOSS_API_KEY environment variable and sends selected audio, media URLs, generated lyrics, text, and transcripts to SkillBoss for processing.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
