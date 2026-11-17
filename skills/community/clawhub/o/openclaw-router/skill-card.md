## Description:

Routes OpenClaw requests across local and cloud language or vision models to balance capability, verification needs, and cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pepsiboy87](https://clawhub.ai/user/pepsiboy87)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to configure and apply model-routing choices for OpenClaw workflows, including local-first routing, cloud escalation, token and cost tracking, and optional image analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can detect local API-key environment variables and may route prompts or user-selected images to configured cloud providers.

Mitigation: Review provider configuration before use, avoid sending sensitive prompts or images to unapproved providers, and keep API keys in a secret manager or scoped environment rather than persistent shell files.

Risk: The documentation includes unsafe install and credential-handling guidance.

Mitigation: Review installation commands before execution, prefer signed packages or checksummed downloads, and avoid piping remote install scripts directly into a shell.

Risk: The skill writes router configuration under the user's home directory.

Mitigation: Inspect generated files under ~/.openclaw before relying on them in production and ensure file permissions match the user's security requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pepsiboy87/skills/openclaw-router)
- [Project homepage](https://github.com/pepsiboy87/openclaw-router)
- [Usage examples](docs/EXAMPLES_en.md)
- [Vision guide](docs/VISION_GUIDE.md)
- [FAQ](docs/FAQ_en.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python snippets, YAML configuration examples, and text routing or image-analysis results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local model choices, cloud provider selections, token estimates, cost estimates, and configuration state.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence; artifact metadata also contains 1.0.0 and 3.0.0 references requiring review)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
