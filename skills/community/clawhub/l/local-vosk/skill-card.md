## Description:

Local Vosk STT helps agents transcribe Telegram voice messages and other audio files with local Vosk speech recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfkiwi](https://clawhub.ai/user/sfkiwi)

### License/Terms of Use:


## Use Case:

Developers and end users can use this skill to transcribe Telegram .ogg voice notes and common audio file formats locally without cloud speech-to-text APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Vosk and downloading a speech model without pinned versions or checksum verification can expose users to ordinary supply-chain risk.

Mitigation: Use a dedicated virtual environment, pin the Vosk package version, and verify the downloaded model archive with a trusted checksum before use.

Risk: The provided artifact documents transcribe commands but does not include the referenced transcribe script.

Mitigation: Confirm the transcribe script is supplied by the runtime environment or another trusted artifact before relying on the documented commands.

## Reference(s):

- [Vosk Models](https://alphacephei.com/vosk/models)
- [Vosk small English model archive](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and transcription instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local transcription workflow guidance; the artifact documents commands and setup steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
