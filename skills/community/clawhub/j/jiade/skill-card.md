## Description:

Generate images with FLUX models through the inference.sh CLI, including text-to-image, image-to-image, LoRA fine-tuning, and custom style workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lihai2582424632-droid](https://clawhub.ai/user/lihai2582424632-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative technical users use this skill to run FLUX image generation and transformation workflows through inference.sh CLI commands, including LoRA-based custom style generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a mutable remote CLI install command that can execute local code.

Mitigation: Use a manually downloaded, version-pinned, checksum-verified inference.sh CLI install and avoid elevated privileges.

Risk: Optional related skill installs broaden the installed capability set beyond this FLUX helper.

Mitigation: Install optional related skills only after separately reviewing that they are trusted and needed.

Risk: Prompts and image URLs may be sent to inference.sh during model runs.

Mitigation: Do not include secrets, private images, or internal-only URLs unless that data sharing is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lihai2582424632-droid/skills/jiade)
- [inference.sh](https://inference.sh)
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt)
- [Running Apps](https://inference.sh/docs/apps/running)
- [Image Generation Example](https://inference.sh/docs/examples/image-generation)
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to prepare prompts, image URLs, and inference.sh CLI invocations for FLUX model workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact _meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
