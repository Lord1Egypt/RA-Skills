## Description:

Guides an agent through configuring OpenClaw to transcribe audio locally on Apple Silicon Macs with mano-asr, with optional fallback to a cloud transcription provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovejing0306](https://clawhub.ai/user/lovejing0306)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add local speech-to-text handling for voice and audio messages across supported chat channels. It helps configure mano-asr installation, OpenClaw audio settings, model selection, validation, service management, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional cloud fallback may send voice content or transcription data to OpenAI after local transcription fails.

Mitigation: Use the local-only mano-asr configuration unless users explicitly accept cloud processing for failed local transcriptions.

Risk: Strong offline-privacy claims may be misunderstood when a cloud fallback provider is also configured.

Mitigation: Document fallback behavior clearly in deployment guidance and separate local-only examples from hybrid local-plus-cloud examples.

Risk: Installation depends on an external Homebrew tap and mano-asr release artifacts.

Mitigation: Review the tap and release provenance before deployment, and prefer pinned, verified releases where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovejing0306/skills/mano-asr)
- [Publisher profile](https://clawhub.ai/user/lovejing0306)
- [mano-asr project](https://github.com/Mininglamp-AI/mano-asr)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, configuration, validation, service-management, model-management, and troubleshooting guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
