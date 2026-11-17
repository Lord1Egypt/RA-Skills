## Description:

Provides Gladia speech-to-text integration guidance for pre-recorded and live transcription, including SDK examples, API workflows, and feature selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gladiaio](https://clawhub.ai/user/gladiaio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this reference to choose Gladia transcription modes and features, integrate the SDK or API, and handle audio transcription results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcription can send sensitive audio or video to Gladia and retain audio and transcripts.

Mitigation: Obtain consent before uploading; configure zero data retention when privacy or compliance requires it.

Risk: Exposing the Gladia API key in client code can allow unauthorized use.

Mitigation: Keep the API key on the backend or in a protected environment variable; never hardcode it in client code.

## Reference(s):

- [Gladia skill documentation](https://docs.gladia.io/.well-known/agent-skills/gladia/skill.md)
- [Gladia documentation](https://docs.gladia.io/llms.txt)
- [Pre-recorded transcription quickstart](https://docs.gladia.io/chapters/pre-recorded-stt/quickstart)
- [Live transcription quickstart](https://docs.gladia.io/chapters/live-stt/quickstart)
- [Gladia API reference](https://docs.gladia.io/api-reference/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [SDK-first guidance for pre-recorded and live transcription.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
