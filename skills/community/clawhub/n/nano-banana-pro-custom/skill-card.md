## Description:

Generate or edit images using an OpenAI-compatible image API, with support for multi-image input, fine-tuned models, and configuration through CLI options, environment variables, OpenClaw config, or a skill config file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxchen](https://clawhub.ai/user/chenxchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate new images, edit existing images, or compose multiple images through a configured OpenAI-compatible image API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images may be sent to the configured API provider.

Mitigation: Install and use the skill only with an approved provider and avoid submitting sensitive prompts or images unless that provider is authorized for the data.

Risk: The skill can target any configured OpenAI-compatible API endpoint.

Mitigation: Review the configured NANO_BASE_URL or OpenClaw configuration before use and restrict it to trusted endpoints.

Risk: Credential diagnostics can reveal whether API keys are set and plaintext config files may contain secrets.

Mitigation: Prefer environment variables or managed OpenClaw configuration, keep extra secrets out of skill config files, and avoid logging --show-config output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenxchen/skills/nano-banana-pro-custom)
- [Publisher Profile](https://clawhub.ai/user/chenxchen)
- [OpenAI-Compatible API Base URL Example](https://api.openai.com/v1)
- [OpenRouter API Base URL Example](https://openrouter.ai/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples; runtime script output includes saved PNG file paths and MEDIA markers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved as PNG files; multiple outputs are numbered when more than one image is requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
