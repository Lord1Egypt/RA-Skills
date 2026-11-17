## Description:

OpenAI Audio Transcriptions API via curl; gpt-4o-transcribe, mini, diarize, or whisper-1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to transcribe audio recordings through the OpenAI Audio Transcriptions API, with options for model, language, output format, and speaker diarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio recordings are sent to the configured transcription service, and model or account choice can affect privacy, billing, or quota.

Mitigation: Before sending audio, check the configured service, model, and account and confirm you are comfortable with the recording being processed there.

## Reference(s):

- [OpenAI speech-to-text guide](https://platform.openai.com/docs/guides/speech-to-text)
- [ClawHub skill release](https://clawhub.ai/hillstreet-ph/skills/oc-openai-whisper-api)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions]

**Output Format:** [Plain-text or JSON transcription results, with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription output may include speaker labels when diarization is selected. Hosted API uploads are limited to 25 MB.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
