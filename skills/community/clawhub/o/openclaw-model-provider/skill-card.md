## Description:

Help users add custom model providers to OpenClaw by configuring provider definitions, default model selection, environment variables, and validation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksbbs](https://clawhub.ai/user/ksbbs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure built-in or custom AI model providers, generate configuration snippets, apply them to OpenClaw settings, and validate connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider setup guidance may lead users to expose API keys in chat, shell output, OpenClaw JSON, or shell profile files.

Mitigation: Use placeholders while discussing configuration, prefer environment variables or a safer secret mechanism, avoid commands that print full keys, and rotate any exposed key.

Risk: Manual provider configuration can break model routing when provider names, model IDs, merge mode, endpoints, or API types are incorrect.

Mitigation: Back up the OpenClaw configuration before editing, validate JSON syntax, run OpenClaw configuration validation, list available models, and test the target model before relying on it.

## Reference(s):

- [OpenClaw Official Documentation - Model Providers](https://docs.openclaw.ai/zh-CN/concepts/model-providers)
- [OpenClaw Model Provider Configuration Reference](references/openclaw-config-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-key placeholders and provider-specific model settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
