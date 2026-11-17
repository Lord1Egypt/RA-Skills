## Description:

Whisper v1转录免费版 helps agents guide local Whisper v1 audio transcription, subtitle generation, and basic translation workflows for individual users and automation scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent creators, and automation users can use this skill to prepare local Whisper transcription commands, generate txt/srt/vtt/json outputs, and document setup requirements for offline media transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence marks the release as suspicious because the documentation is broad and internally inconsistent.

Mitigation: Review the skill before installation and confirm that the publisher's intended behavior matches local transcription or subtitle-generation use.

Risk: The skill proposes package installation, sudo package-manager commands, and shell commands that may process private media files.

Mitigation: Review each command before execution, avoid passing sensitive media unless the local environment is trusted, and confirm package sources before installing dependencies.

Risk: The documentation contains inconsistent API key language even though the security guidance says to treat API key references as unreliable unless clarified by the publisher.

Mitigation: Do not provide API keys based only on this skill's text; clarify requirements with the publisher or rely on local-only operation when appropriate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/llm-provider-whisper-v1-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and transcription output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or point to local txt, srt, vtt, json, or tsv transcription artifacts when executed by an agent.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
