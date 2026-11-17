## Description:

Auto-detects local hardware, recommends Ollama-compatible models, configures Ollama, and sets up hybrid cloud/local routing in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate local AI hardware capacity, select a suitable local model, and configure OpenClaw routing between local Ollama models and cloud providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may install Ollama, download models, and edit OpenClaw configuration.

Mitigation: Run detect or recommend mode first, review proposed changes, and back up `~/.openclaw/openclaw.json` before allowing configuration commands.

Risk: The automatic Linux installer path can execute a remote installer.

Mitigation: Prefer installing Ollama manually from a verified source before running setup that depends on Ollama.

## Reference(s):

- [Model Matrix](references/model-matrix.md)
- [Ollama Model Library](https://ollama.com/library)
- [ClawHub Skill Page](https://clawhub.ai/stevojarvisai-star/skills/local-model-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend model downloads, Ollama setup steps, and OpenClaw configuration changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
