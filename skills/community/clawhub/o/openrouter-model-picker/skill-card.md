## Description:

OpenRouter Model Picker fetches OpenRouter models, presents a Canvas UI for filtering and selecting enabled models, and applies OpenClaw model configuration updates without a Gateway restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ys727469926](https://clawhub.ai/user/ys727469926)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to choose OpenRouter models, set primary and fallback models, and hot-update local OpenClaw configuration through a Canvas picker or CLI fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local configuration server can change enabled, primary, and fallback OpenClaw model settings without authentication.

Mitigation: Run the picker only in a trusted local environment, avoid browsing untrusted sites while it is running, and prefer a version with a per-session token, strict origin checks, and server-side model validation.

Risk: Applying a selection can permanently change which OpenClaw models are enabled.

Mitigation: Review selected models before applying and use the picker or CLI fallback to restore intended settings if needed.

## Reference(s):

- [config_server.py Reference](artifact/references/config-server.md)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)
- [ClawHub Skill Page](https://clawhub.ai/ys727469926/skills/openrouter-model-picker)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown embed instructions with bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates local OpenClaw model settings and can render an interactive Canvas picker.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
