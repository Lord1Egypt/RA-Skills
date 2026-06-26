## Description: <br>
Use Jimeng AI 4.0 (Volcengine) to generate images from text or image references, and optionally send results to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tangc](https://clawhub.ai/user/Tangc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate PNG image results from text prompts or reference image URLs with Jimeng AI 4.0. They can return an image URL directly or optionally send the generated image through Feishu when a target user is provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and reference image URLs are sent to Volcengine, and target mode sends the generated image URL and caption through a local Feishu bridge. <br>
Mitigation: Avoid sensitive prompts and private reference image URLs unless those services are approved for the data, and use target mode only with the intended Feishu recipient. <br>
Risk: The helper passes the Volcengine secret key through a process argument while generating request signatures. <br>
Mitigation: Use a dedicated low-privilege Volcengine key and avoid running the helper on shared machines where process arguments may be visible to other users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tangc/jimeng-t2i-i2i-image-generator) <br>
- [Volcengine visual API endpoint](https://visual.volcengineapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Shell command output with generated image URLs and optional Feishu delivery status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are PNG assets returned as service-hosted URLs; i2i mode may use a default reference image when no reference URL is supplied.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
