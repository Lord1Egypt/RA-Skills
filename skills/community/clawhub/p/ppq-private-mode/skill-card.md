## Description:

Install PPQ.AI Private Mode for end-to-end encrypted AI inference in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattius459](https://clawhub.ai/user/mattius459)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install PPQ.AI Private Mode, configure a local OpenAI-compatible provider, and switch to encrypted private models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to handle a live PPQ API key.

Mitigation: Treat the key as sensitive, use a limited or revocable key when available, avoid exposing it in logs or chat history, and rotate it if it may have been disclosed.

Risk: The skill installs third-party plugin code from a mutable repository URL without pinning or verification.

Mitigation: Review the plugin source before installation and prefer a pinned release or commit with provenance.

Risk: The PPQ API key is written into ~/.openclaw/openclaw.json.

Mitigation: Check file permissions on ~/.openclaw/openclaw.json and know how to remove the plugin configuration or rotate the key before proceeding.

## Reference(s):

- [PPQ.AI API documentation](https://ppq.ai/api-docs)
- [PPQ.AI](https://ppq.ai)
- [PPQ Private Mode proxy repository](https://github.com/PayPerQ/ppq-private-mode-proxy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw provider configuration, plugin configuration, gateway restart guidance, and available private model identifiers.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
