## Description:

Installs, verifies, repairs, and diagnoses GPT-Image-2 support for OpenClaw so agents can use model refs like hnbc/gpt-image-2 through the built-in image_generate tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevins9527](https://clawhub.ai/user/kevins9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install and troubleshoot the HNBC GPT-Image-2 image generation provider for image_generate workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and API keys are sent to the HNBC API endpoint.

Mitigation: Confirm api.1415.xin is the intended endpoint, use a dedicated revocable HNBC API key, and avoid sensitive prompts unless the service is trusted.

Risk: The installer replaces any existing local ~/.openclaw/extensions/hnbc plugin.

Mitigation: Back up the existing hnbc extension directory before running scripts/install.sh.

Risk: A custom HNBC baseUrl receives the configured API key.

Mitigation: Use only trusted custom base URLs and treat the endpoint configuration as sensitive.

Risk: The running OpenClaw gateway can keep an older provider registry after installation.

Mitigation: Restart the gateway only with user approval, then verify image_generate(action="list") and test generation without a resolution parameter.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/kevins9527/skills/gpt-image-2-toolkit)
- [GPT-Image-2 for OpenClaw 1.0.1 plan](references/release-1.0.1.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and diagnostic steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install or replace the local hnbc OpenClaw extension and may trigger image generation through the configured HNBC API when used after setup.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
