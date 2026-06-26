## Description: <br>
Media Generation helps agents generate images, edit existing images, create short videos, run inpainting and outpainting workflows, use reference images as provider inputs, batch media jobs from manifests, and fetch returned media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijiazhen0623](https://clawhub.ai/user/lijiazhen0623) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route media-production requests to the appropriate helper for image generation, image editing, video generation, reference-image transport, batch execution, and media retrieval. It is intended for reusable workflows that save generated outputs to local media folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected media files, provider responses, and optional logs may contain sensitive information. <br>
Mitigation: Avoid confidential media unless the configured provider is trusted, and treat batch summary files as sensitive logs. <br>
Risk: The skill uses configured media-provider API credentials and can upload prompts and selected media to those providers. <br>
Mitigation: Confirm provider configuration and credential scope before running helper commands. <br>
Risk: Provider-returned URLs may be downloaded into local temporary media folders. <br>
Mitigation: Review downloaded outputs and keep generated files in the documented tmp/images or tmp/videos folders. <br>


## Reference(s): <br>
- [Model Capabilities](references/model-capabilities.md) <br>
- [Reference-Image Workflow](references/reference-image-workflow.md) <br>
- [Batch Workflows](references/batch-workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved under tmp/images, generated videos are saved under tmp/videos, and optional batch summaries may be written as JSON.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
