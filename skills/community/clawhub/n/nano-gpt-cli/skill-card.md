## Description:

Use when tasks need the NanoGPT API for text, image, or video generation through the local `nano-gpt` CLI and bundled wrapper scripts for OpenClaw or ClawHub workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icework](https://clawhub.ai/user/icework)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call NanoGPT from a local terminal for text prompts, chat, model discovery, image generation, and video generation. It is useful when OpenClaw or ClawHub workflows need a thin CLI wrapper around NanoGPT API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can store and reveal a NanoGPT API token in local configuration.

Mitigation: Prefer NANO_GPT_API_KEY for authentication and avoid running commands that print the API key in logged or shared environments.

Risk: Prompts, API tokens, and explicitly provided media are sent to the configured NanoGPT endpoint.

Mitigation: Keep NANO_GPT_BASE_URL set only to trusted HTTPS endpoints and provide only prompts or media intended for that service.

## Reference(s):

- [NanoGPT Documentation](https://docs.nano-gpt.com/)
- [NanoGPT CLI Reference](references/cli.md)
- [NanoGPT Workflows](references/workflows.md)
- [ClawHub Skill Page](https://clawhub.ai/icework/skills/nano-gpt-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Terminal text or JSON, with optional image and video files written to local paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NANO_GPT_API_KEY; prompts and explicitly provided media are sent to the configured NanoGPT endpoint.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
