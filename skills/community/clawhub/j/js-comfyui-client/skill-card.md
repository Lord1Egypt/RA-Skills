## Description:

ComfyUI Client helps agents use a running ComfyUI server to load image or video workflows, update prompts and image inputs, submit jobs, poll status, and download generated outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imjszhang](https://clawhub.ai/user/imjszhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to automate ComfyUI image generation, image editing, and image-to-video workflows from text prompts and local or reference images. It is suited for environments where ComfyUI and the workflow-required models are already installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or untrusted ComfyUI server could provide output filenames that write downloaded files outside the intended output directory.

Mitigation: Use a trusted local ComfyUI endpoint where possible and review downloaded output paths before relying on generated files.

Risk: Changing --server or COMFYUI_SERVER_URL to an untrusted host can expose workflow prompts, image inputs, and generated outputs to that host.

Mitigation: Keep the server URL pointed at a trusted ComfyUI instance and avoid sending sensitive inputs to remote or unknown endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imjszhang/skills/js-comfyui-client)
- [Publisher profile](https://clawhub.ai/user/imjszhang)
- [Workflow path reference](artifact/references/workflow_paths.md)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI subgraph documentation](https://docs.comfy.org/interface/features/subgraph)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local file outputs from ComfyUI runs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates session folders containing workflow, result, error, image, and video files when the ComfyUI client is executed.]

## Skill Version(s):

1.2.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
