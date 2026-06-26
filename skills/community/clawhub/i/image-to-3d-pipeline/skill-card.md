## Description: <br>
One-click automated pipeline for converting product images into 3D models through image preprocessing, optional enhancement, and 3D generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m15010495895-sudo](https://clawhub.ai/user/m15010495895-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical creators use this skill to prepare product images, call third-party image-to-3D services, monitor generation jobs, and retrieve 3D model outputs for web, mobile AR, or 3D tooling workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact presents a Tripo3D/Replicate workflow but includes Meshy API calls and an undeclared MESHY_API_KEY. <br>
Mitigation: Confirm the intended provider before use, do not provide MESHY_API_KEY unless Meshy is approved, and review pricing and data handling for any third-party service receiving uploaded images. <br>
Risk: Product images are uploaded to third-party services for background removal, enhancement, or 3D generation. <br>
Mitigation: Use only images the user is authorized to upload and avoid confidential or regulated content unless the selected provider is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/m15010495895-sudo/image-to-3d-pipeline) <br>
- [Replicate TripoSR](https://replicate.com/baaas/triposr) <br>
- [remove.bg API](https://www.remove.bg/api) <br>
- [Upscale API](https://upscale.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands, JSON examples, workflow guidance, and model format notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRIPOSR_API_KEY; REMOVE_BG_API_KEY and UPSCALE_API_KEY are optional according to metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
