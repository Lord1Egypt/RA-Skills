## Description:

Local Speech Recognition transcribes supported audio files locally with faster-whisper and returns voice-message text without requiring API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zktufo](https://clawhub.ai/user/zktufo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert local voice messages, meeting audio, podcasts, and other supported audio files into readable text. It is suitable for privacy-sensitive workflows where audio should be processed locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First use may download or install speech model dependencies.

Mitigation: Review dependency and model installation behavior in the target environment before deployment.

Risk: Voice transcripts may contain sensitive user content and are inserted into the conversation.

Mitigation: Treat generated transcripts as sensitive data and apply the same handling controls used for confidential conversation content.

Risk: The default language is Chinese when no language argument is supplied.

Mitigation: Pass the intended language argument or use auto detection when Chinese is not the expected default.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zktufo/skills/localspeechrecognition)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text transcript with status or error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports .ogg, .m4a, .mp3, and .wav audio files up to 25MB; language can be zh, en, ja, or auto.]

## Skill Version(s):

1.0.2 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
