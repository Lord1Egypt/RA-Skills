## Description:

Local image generation using Apple MLX via mflux with FLUX.2 Klein and Z-Image Turbo models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pjain](https://clawhub.ai/user/pjain)

### License/Terms of Use:

MIT

## Use Case:

Developers and content creation agents use this skill to install and invoke mflux for local image generation and editing on Apple Silicon Macs. It guides CLI and Python usage, model selection, quantization, and cache expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First use contacts external package and model download sources despite local generation after setup.

Mitigation: Install only after confirming trust in the upstream mflux package and the selected Hugging Face model repositories.

Risk: Model downloads and local caches can consume substantial disk space.

Mitigation: Confirm sufficient free disk space for 8-32GB downloads and plan cache management for ~/.cache/huggingface/.

Risk: Lower-memory Apple Silicon systems may fail or perform poorly with larger models.

Mitigation: Use quantization options or smaller supported models when running on 8GB or otherwise constrained Macs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pjain/skills/mflux)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in local image files when generated commands or code are executed; first use downloads model weights and uses local cache space.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
