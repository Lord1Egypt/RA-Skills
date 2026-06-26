## Description: <br>
Run local ComfyUI workflows via the HTTP API, including workflows from file paths, workflow names, raw API-format JSON, or the bundled default workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-generation users use this skill to run local ComfyUI workflows, edit prompt/style/seed fields in workflow JSON, download model weights, and return generated images to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run the pget helper executable during model downloads. <br>
Mitigation: Use --no-pget or install pget yourself from a verified source before running downloads. <br>
Risk: The skill downloads model files from user-provided network URLs into the local ComfyUI directory. <br>
Mitigation: Use only trusted model URLs and review the intended destination folder before downloading. <br>
Risk: The skill can overwrite existing files when --overwrite is used. <br>
Mitigation: Avoid --overwrite unless the destination path has been checked and replacing the file is intended. <br>
Risk: Workflow JSON controls local ComfyUI execution behavior. <br>
Mitigation: Review workflow JSON before execution, especially when it comes from an external source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kirkraman/kirk-image) <br>
- [Publisher Profile](https://clawhub.ai/user/kirkraman) <br>
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI.git) <br>
- [pget](https://github.com/replicate/pget) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, images] <br>
**Output Format:** [Markdown guidance with shell commands, JSON workflow edits, script JSON output, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queues ComfyUI workflows over the local HTTP API and returns generated images from ComfyUI/output after successful runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
