## Description: <br>
Use the Keevx API to generate images from prompts and reference images, with support for standard and professional modes, 1K/2K/4K output quality, multiple aspect ratios, batch generation, and task status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-xiling](https://clawhub.ai/user/baidu-xiling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to call Keevx image generation from an agent workflow, including prompt-only generation, reference-image generation, batch requests, and task status polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images are sent to Keevx outside the local machine. <br>
Mitigation: Use only content approved for that provider, avoid confidential or regulated images unless authorized, and use a revocable API key when available. <br>
Risk: Optional callback URLs receive task completion data from the external service. <br>
Mitigation: Provide callback URLs only for endpoints you control and trust. <br>
Risk: Generated image URLs are retained for a limited time. <br>
Mitigation: Download generated images promptly when the result is needed beyond the retention window. <br>


## Reference(s): <br>
- [Keevx documentation](https://docs.keevx.com) <br>
- [Keevx API base endpoint](https://api.keevx.com/v1) <br>
- [ClawHub skill page](https://clawhub.ai/baidu-xiling/keevx-image-generate) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Keevx request guidance, upload and polling commands, task IDs, and generated image URLs returned by the API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
