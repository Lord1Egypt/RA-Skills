## Description:

Transform any text into emotionally expressive audio with ambient soundscapes using ElevenLabs v3 audio tags and Sound Effects API

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashutosh887](https://clawhub.ai/user/ashutosh887)

### License/Terms of Use:

MIT License

## Use Case:

Developers, creators, writers, and agent users use MoodCast to convert supplied text into emotionally expressive spoken audio, optionally with matching ambient soundscapes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install an unpinned Python package at runtime.

Mitigation: Install dependencies from a pinned, trusted environment before use and review the resolved package version.

Risk: The skill sends submitted text to ElevenLabs for text-to-speech or sound-effect generation.

Mitigation: Do not submit confidential, regulated, or secret text unless ElevenLabs processing is acceptable for that data.

Risk: The release uses mutable install paths.

Mitigation: Install from a controlled path and avoid running the skill with elevated privileges.

## Reference(s):

- [MoodCast ClawHub page](https://clawhub.ai/ashutosh887/skills/moodcast)
- [MoodCast homepage](https://github.com/ashutosh887/moodcast)
- [ElevenLabs](https://elevenlabs.io)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; generated outputs are enhanced text and MP3 audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ELEVENLABS_API_KEY; optional ambient sound generation is capped at 30 seconds.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
