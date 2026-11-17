## Description:

Transcribe audio via OpenAI Audio Transcriptions API (Whisper).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to transcribe a selected local audio file through OpenAI's transcription API and save the transcript for downstream work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio files are sent to OpenAI for transcription and may contain confidential, regulated, or non-consented speech.

Mitigation: Use only with recordings that are appropriate to send to OpenAI under the user's account settings, permissions, and applicable policy.

Risk: The script writes transcript files locally and may overwrite an explicitly provided output path.

Mitigation: Choose an output location deliberately and review the saved transcript before sharing or using it in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/skills/mh-openai-whisper-api)
- [OpenAI speech-to-text guide](https://platform.openai.com/docs/guides/speech-to-text)
- [OpenAI audio transcriptions endpoint](https://api.openai.com/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration]

**Output Format:** [Plain text or JSON transcript files, with shell output containing the saved file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and OPENAI_API_KEY; the selected audio file is sent to OpenAI for transcription.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
