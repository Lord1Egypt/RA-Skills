## Description:

Advanced JSON editing for OpenClaw configuration files, tools, and data structures, including JSON5 configs, schema validation, merge patching, environment variable substitution, and type-safe modifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avirweb](https://clawhub.ai/user/avirweb)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to edit, validate, patch, and troubleshoot OpenClaw JSON5 configuration, provider, model, agent, channel, and tool settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands that search or dump OpenClaw configuration may expose plaintext API keys, tokens, or passwords to the agent session.

Mitigation: Review configuration files for secrets first, prefer environment-variable references, and redact sensitive values before sharing command output.

Risk: Provider discovery examples can make authenticated requests to external model APIs.

Mitigation: Run provider API calls only with explicit user intent and appropriate credentials, and avoid embedding API keys directly in commands or configuration.

Risk: Configuration patch examples can change agent, model, channel, or tool behavior.

Mitigation: Back up configuration files, validate changes with OpenClaw validation commands, and review generated patches before applying them.

## Reference(s):

- [OpenClaw JSON Editing Masterclass on ClawHub](https://clawhub.ai/avirweb/skills/openclaw-json-editing)
- [xAI Models API endpoint](https://api.x.ai/v1/models)
- [OpenAI Models API endpoint](https://api.openai.com/v1/models)
- [Together AI Models API endpoint](https://api.together.xyz/v1/models)
- [Anthropic API base endpoint](https://api.anthropic.com)
- [Google Generative Language API endpoint](https://generativelanguage.googleapis.com/v1beta)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON5, TypeScript, JavaScript, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that read local configuration files or call provider APIs when the user explicitly intends to do so.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
