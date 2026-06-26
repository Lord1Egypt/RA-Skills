## Description: <br>
Image Outpainting - Pro Pack on RunComfy helps agents extend still images beyond their original canvas, change aspect ratio, and preserve source content by selecting suitable RunComfy image editing routes through the runcomfy CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to outpaint, uncrop, or resize still images with RunComfy-hosted image editing models while receiving route selection guidance and CLI invocation patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the runcomfy CLI and a RunComfy account token. <br>
Mitigation: Install the CLI only from a verified package source and protect RUNCOMFY_TOKEN as an account credential. <br>
Risk: Image URLs and prompts are submitted to RunComfy for processing. <br>
Mitigation: Submit only image URLs and prompts the user is comfortable sending to RunComfy. <br>
Risk: Outpainting results may diverge from the requested edit or alter source content. <br>
Mitigation: Review generated outputs before using them and rerun with stronger preservation prompts when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/image-outpainting-runcomfy) <br>
- [RunComfy homepage](https://www.runcomfy.com) <br>
- [RunComfy CLI docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=image-outpainting-runcomfy) <br>
- [Best image editing models collection](https://www.runcomfy.com/models/collections/best-image-editing-models?utm_source=clawhub&utm_medium=skill&utm_campaign=image-outpainting-runcomfy) <br>
- [Nano Banana 2 Edit model](https://www.runcomfy.com/models/google/nano-banana-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=image-outpainting-runcomfy) <br>
- [ComfyUI workflows](https://www.runcomfy.com/comfyui-workflows?utm_source=clawhub&utm_medium=skill&utm_campaign=image-outpainting-runcomfy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent to produce RunComfy CLI commands and configuration steps; generated image files are produced by RunComfy after command execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
