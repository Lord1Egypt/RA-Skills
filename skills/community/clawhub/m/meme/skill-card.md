## Description:

Create funny voice memes with various styles, effects, and templates. Use when users want to make humorous audio content, voice memes, or entertaining sound clips for social media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate short meme-style voice clips with SenseAudio TTS presets or custom speed, pitch, and volume settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text is sent to SenseAudio for TTS generation.

Mitigation: Avoid sensitive, personal, or regulated text unless the deployment has approved SenseAudio use for that data.

Risk: Generated audio is written as a local MP3 file.

Mitigation: Write output files to an intended location and handle them according to the user's content-retention requirements.

Risk: The prerequisite uses an unpinned requests dependency.

Mitigation: Install in a dedicated virtual environment and pin dependency versions for repeatable deployments.

## Reference(s):

- [SenseAudio](https://senseaudio.cn)
- [SenseAudio TTS API](https://senseaudio.cn/docs/text_to_speech_api)
- [SenseAudio Voice List](https://senseaudio.cn/docs/voice_api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with Python and shell code blocks; generated workflows save MP3 audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and transmits user-provided text to SenseAudio.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
