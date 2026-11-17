## Description:

Serve a quantized language model locally on an Apple Silicon Mac with mlx-optiq and an OpenAI-compatible endpoint. Use when the user wants to run a model on their own Mac, pick a model that fits their memory, connect a tool to a local server, or check local speed and quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sandeep85das](https://clawhub.ai/user/sandeep85das)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Apple Silicon Mac users can use this skill to check compatibility, choose a quantized model that fits available memory, run it locally, connect compatible clients, and assess speed and quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model downloads require several gigabytes of storage and can begin when the server starts.

Mitigation: Get user approval before downloading or starting the server, and check available memory and model size first.

Risk: Exposing the local model server beyond the Mac can allow unintended network access.

Mitigation: Keep the server bound to 127.0.0.1 unless network access is deliberate and authenticated; stop it when finished.

## Reference(s):

- [MLX-OptiQ documentation](https://mlx-optiq.com)
- [MLX-OptiQ models](https://mlx-optiq.com/models)
- [Troubleshooting local serving](artifact/references/troubleshooting.md)
- [ClawHub release page](https://clawhub.ai/sandeep85das/skills/optiq-local-models)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scoped to Apple Silicon Macs using an already-installed mlx-optiq.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
