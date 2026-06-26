## Description: <br>
Runs and customizes local ComfyUI workflows through the HTTP API to generate images from prompts, supplied workflows, or downloaded model weights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-generation users use this skill to run local ComfyUI API workflows, adjust prompts, styles, and seeds in workflow JSON, download model weights into ComfyUI model folders, and deliver generated images back to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and execute the pget downloader binary automatically when downloading model weights. <br>
Mitigation: Use trusted model URLs, prefer the built-in downloader with --no-pget when automatic binary installation is not acceptable, and verify any downloader before execution. <br>
Risk: Model weight downloads persist files under the user's ComfyUI models directory and can consume significant local storage. <br>
Mitigation: Review the URL list and target subfolder before running downloads, skip unknown sources, and remove unneeded model files after use. <br>
Risk: The skill edits workflow JSON before execution, which can change prompts, style nodes, and seeds in user-supplied workflows. <br>
Mitigation: Inspect workflow changes before queueing sensitive or production workflows and run unclear workflows as-is when prompt or sampler nodes cannot be identified confidently. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/godferylindsay/martin-image) <br>
- [ComfyUI repository](https://github.com/comfyanonymous/ComfyUI) <br>
- [pget downloader](https://github.com/replicate/pget) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON workflow edits, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queues workflows against a local ComfyUI server and reports generated image paths for delivery to the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
