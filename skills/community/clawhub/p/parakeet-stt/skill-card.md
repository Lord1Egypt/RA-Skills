## Description:

Local speech-to-text skill for using NVIDIA Parakeet TDT 0.6B v3 with ONNX on CPU, OpenAI-compatible transcription APIs, auto-detected languages, and local audio transcription workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carlulsoe](https://clawhub.ai/user/carlulsoe)

### License/Terms of Use:


## Use Case:

Developers and users with local audio files use this skill to configure or call a local Parakeet transcription service for plain text, JSON, timestamped segments, SRT, or WebVTT output without cloud transcription APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup directs users to run unverified third-party code.

Mitigation: Review the upstream repository before installing and prefer a pinned reviewed commit or verified release.

Risk: The local speech-to-text service may be exposed without authentication if bound broadly.

Mitigation: Run the service only on localhost unless authentication, TLS or network restrictions, and resource limits are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/carlulsoe/skills/parakeet-stt)
- [Parakeet TDT FastAPI OpenAI Repository](https://github.com/groxaxo/parakeet-tdt-0.6b-v3-fastapi-openai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, curl, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples and environment variable configuration for PARAKEET_URL.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
