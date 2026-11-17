## Description:

MiMo ASR transcribes audio to text through Xiaomi's public Gradio API, with automatic, Chinese, and English language modes and no local model or API key requirement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xcchenx345](https://clawhub.ai/user/xcchenx345)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to transcribe audio recordings, extract spoken dialogue, and save transcripts from common audio formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio is uploaded to an external Gradio/Hugging Face service for transcription.

Mitigation: Use only with audio that may be shared with that service; avoid confidential, regulated, or private recordings unless data handling is reviewed.

Risk: The API script disables HTTPS certificate verification.

Mitigation: Enable TLS certificate verification before deployment and review outbound network traffic.

Risk: Runtime dependencies are not pinned in a reviewed requirements file.

Mitigation: Pin and review dependencies such as requests before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xcchenx345/skills/mimo-asr)
- [MiMo-V2.5-ASR Hugging Face Space](https://xiaomimimo-mimo-v2-5-asr.hf.space)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Plain text transcript, optionally written to a text file, with shell command examples in guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports auto, Chinese, and English language modes; requires an audio file and network access for the API workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
