## Description:

Guides agents through configuring, testing, and debugging OpenClaw text-to-speech with OpenAI-compatible local or self-hosted TTS servers, including speech endpoint validation, mode selection, streaming, custom voices, and spoken-number normalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mozi1924](https://clawhub.ai/user/mozi1924)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and troubleshoot OpenClaw TTS integrations backed by OpenAI-compatible local or self-hosted servers. It helps validate server health, speech endpoint behavior, streaming, model and voice mode selection, consent-based cloning, and TTS-ready text normalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to send text and optional voice recordings to a configured TTS server, which may expose sensitive content if the endpoint is not trusted.

Mitigation: Confirm the configured TTS base URL before use, send data only to trusted servers, and require access controls for any deployed endpoint.

Risk: Consent-based voice clone flows can involve sensitive biometric voice recordings.

Mitigation: Collect clear consent before upload and verify that the server has an appropriate deletion or retention policy for stored recordings and metadata.

## Reference(s):

- [TTS API Calling Documentation](references/tts-api.md)
- [Local OpenAPI Schema](http://localhost:8000/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local curl tests, OpenClaw configuration checks, request-shape guidance, and troubleshooting conclusions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
