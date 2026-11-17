## Description:

Use Microsoft Edge online TTS service to convert text to speech. Supports command line and module invocation, no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert text into speech, generate audio files, produce subtitle JSON, and configure Microsoft Edge online TTS voices and speech options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples run an unpinned npm package, so behavior can change when the package updates.

Mitigation: Use a pinned and reviewed node-edge-tts version through a lockfile or sandbox before deployment.

Risk: Text submitted for synthesis is sent to Microsoft Edge's online TTS service.

Mitigation: Use the skill only with text that is acceptable to send to that online service.

Risk: Speech generation depends on network access and may be affected by service availability or rate limiting.

Mitigation: Control call frequency and plan for network or service failures in automated workflows.

## Reference(s):

- [Microsoft Voice Support Documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/microsoft-edge-tts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands, JavaScript examples, parameter tables, and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced TTS tool can produce audio files and subtitle JSON when invoked.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
