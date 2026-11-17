## Description:

Guides agents through terminal transcription of prerecorded audio files and URLs using the Gladia CLI, then helps answer questions grounded in the transcript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gladiaio](https://clawhub.ai/user/gladiaio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other CLI users use this skill to transcribe prerecorded audio from local files or URLs and answer questions using the resulting text, timestamps, or speaker labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested installation command pipes a changing remote script directly into a shell.

Mitigation: Download and inspect the installer before running it; prefer a pinned or package-manager installation if available.

Risk: Transcribing local files or URLs sends audio to Gladia.

Mitigation: Upload only audio or URLs that the user is authorized to send to Gladia.

Risk: The local authentication command stores an API key in ~/.gladia.

Mitigation: Use an environment variable when local persistence is inappropriate and protect any stored credentials.

## Reference(s):

- [CLI vs SDK routing guide](references/cli-vs-sdk.md)
- [Gladia CLI documentation and installation](https://github.com/gladiaio/gladia-cli/)
- [Gladia prerecorded transcription quickstart](https://docs.gladia.io/chapters/pre-recorded-stt/quickstart)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Natural-language answers and CLI instructions; transcripts may be text, JSON, SRT, or VTT]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should be grounded in captured transcripts, with timestamps and speakers when available.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
