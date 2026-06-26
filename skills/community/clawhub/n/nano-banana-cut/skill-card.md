## Description: <br>
Nano Banana Cut provides a local web UI and CLI utilities for generating images with AceData Nano Banana models, slicing images into 2/4/6/9 grids, and managing generated works. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyunnet](https://clawhub.ai/user/xiyunnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and external users can use this skill to run a local image-generation and slicing workflow for short-form visual content, reference-image editing, gallery management, and bulk export of generated assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local web server exposes broad unauthenticated file, admin, credential, and shutdown controls. <br>
Mitigation: Run only on a trusted local machine, keep the server bound to localhost and away from untrusted networks, and review the skill before installing. <br>
Risk: Prompts, images, and generated assets may be sent to external AceData services during generation or upload workflows. <br>
Mitigation: Use limited AceData credentials and avoid sensitive images or prompts until authentication, CSRF checks, path confinement, and stronger secret handling are added. <br>
Risk: File serving and path handling require review before use in shared or network-accessible environments. <br>
Mitigation: Confine file operations to an application workspace and remove arbitrary file serving before broader deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiyunnet/nano-banana-cut) <br>
- [AceData Nano Banana access link](https://share.acedata.cloud/r/1uN88BrUTQ) <br>
- [AceData Nano Banana image API](https://api.acedata.cloud/nano-banana/images) <br>
- [AceData Nano Banana task API](https://api.acedata.cloud/nano-banana/tasks) <br>
- [AceData file upload API](https://platform.acedata.cloud/api/v1/files/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with command examples, JSON API responses, generated image files, sliced image files, thumbnails, and ZIP archives.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated assets may include original images, 480p thumbnails, grid slices, and task metadata files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
