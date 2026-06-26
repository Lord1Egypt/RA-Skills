## Description: <br>
ComfyUI Client helps an agent load ComfyUI workflows, update prompts and image inputs, submit image or video generation jobs, poll for results, and download generated outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imjszhang](https://clawhub.ai/user/imjszhang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill when a user asks to generate or edit images, create image-to-video outputs, or automate ComfyUI workflows from prompts and reference images. It assumes a reachable ComfyUI server and required workflow models installed in that ComfyUI environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, workflow data, and uploaded images may be sent to a configured ComfyUI server. <br>
Mitigation: Prefer a local ComfyUI server or a trusted remote endpoint, and avoid sending sensitive prompts or images unless the server retention and access controls are acceptable. <br>
Risk: Generated outputs are saved to local output folders and may contain sensitive content. <br>
Mitigation: Review and clean the ComfyUI output folders after use, especially before sharing the workspace or generated sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imjszhang/js-comfyui-client) <br>
- [Publisher profile](https://clawhub.ai/user/imjszhang) <br>
- [README.md](artifact/README.md) <br>
- [Workflow path reference](artifact/references/workflow_paths.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; ComfyUI runs produce JSON session records plus generated image or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates per-session output folders under work_dir/comfyui_output with session_info.json, workflow.json, result.json, generated files, and error.json when failures occur.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter, package.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
