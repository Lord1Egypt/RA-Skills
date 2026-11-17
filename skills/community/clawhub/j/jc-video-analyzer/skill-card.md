## Description:

Parse local video files into transcript and AI analysis. Extract audio, transcribe with faster-whisper, analyze with AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremycooper2077](https://clawhub.ai/user/jeremycooper2077)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video analysts use this skill to process local video files into timestamped transcripts and AI-generated analysis reports. It supports workflows that extract audio, run faster-whisper transcription, and summarize or correct the transcript through a configured AI endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI analysis step can send the complete transcript to a configurable remote endpoint.

Mitigation: Verify the provider URL before use and avoid processing sensitive recordings unless that data flow is acceptable.

Risk: The analysis step reads an API credential for the configured AI endpoint.

Mitigation: Use a constrained API key with limited scope and rotate it if transcript processing occurs in an untrusted environment.

Risk: Runtime dependencies and models are installed or downloaded outside the skill package.

Mitigation: Pin dependencies and review the configured model download endpoint before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeremycooper2077/skills/jc-video-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands plus generated transcript and analysis files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow can produce WAV audio, timestamped transcript text, corrected transcript Markdown, analysis Markdown, and optional extracted frame images.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
