## Description:

Guides local text-to-video and image-to-video setup in ComfyUI on an 8 GB VRAM Windows laptop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to configure a local ComfyUI video-generation environment on an 8 GB VRAM Windows laptop, select compatible Wan or LTX models, and troubleshoot short video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup recommends a persistent global GitHub redirect through a third-party mirror.

Mitigation: Prefer direct GitHub access or a trusted scoped proxy; if a mirror is necessary, verify and pin the source, then remove any temporary global rewrite.

Risk: Updating GPU drivers and Torch/CUDA can affect the local video-generation environment.

Mitigation: Treat driver and dependency changes as deliberate system maintenance; check compatibility and review changes before installing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lingyu9495-source/skills/lowvram-ai-video-comfyui)
- [ComfyUI installation and troubleshooting](references/comfyui-install-troubleshooting.md)
- [Wan 2.1 text-to-video workflow template](templates/wan21_t2v_workflow.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON workflow]

**Output Format:** [Markdown guidance with commands and a ComfyUI workflow JSON template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes a workflow for producing short local MP4 videos; the skill itself supplies instructions and a template, not video files.]

## Skill Version(s):

1.1.1 (source: server-resolved ClawHub release; bundled frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
