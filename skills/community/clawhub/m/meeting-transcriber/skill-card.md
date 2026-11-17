## Description:

Meeting Transcriber provides real-time Chinese meeting transcription with microphone capture, voice activity detection, punctuation, transcript saving, and environment checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinapjs](https://clawhub.ai/user/chinapjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to capture Chinese meeting audio, run local FunASR transcription, and manage saved meeting transcript files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The core transcription path depends on an unaudited local script outside the packaged artifact.

Mitigation: Review and trust the local transcription script before installation or execution.

Risk: Environment setup can create or modify local Conda and OpenClaw configuration files.

Mitigation: Run setup only after reviewing the files and paths it creates or changes.

Risk: Meeting audio and generated transcripts can contain sensitive participant information.

Mitigation: Get participant consent before recording and store transcript files according to the user's data handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinapjs/skills/meeting-transcriber)
- [FunASR project](https://github.com/alibaba-damo-academy/FunASR)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text with command examples and saved transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs in a Windows Conda environment and saves meeting transcripts as local text files.]

## Skill Version(s):

1.0.0 (source: evidence release, artifact metadata, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
