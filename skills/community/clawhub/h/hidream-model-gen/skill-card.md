## Description: <br>
Generate images and videos using Vivago AI (智小象) platform. Supports text-to-image, image-to-image, image-to-video, and keyframe-to-video generation. Use when the user wants to create AI-generated images or videos, transform existing images, or perform image style transfer through the Vivago AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhy2015](https://clawhub.ai/user/zhy2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to call Vivago AI for image and video generation, image transformation, and image-to-video workflows from prompts or source images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts and images are sent to Vivago for generation workflows. <br>
Mitigation: Use the skill only when sharing that content with Vivago is acceptable, and avoid sensitive personal photos unless there is explicit consent and a clear reason. <br>
Risk: The Vivago API token is a credential for the generation service. <br>
Mitigation: Store the token in the HIDREAM_AUTHORIZATION environment variable and avoid passing or logging it in command-line arguments. <br>
Risk: The bundled template catalog includes sensitive person-image templates without enough warnings or guardrails. <br>
Mitigation: Review the template catalog before installation and remove, gate, or require manual approval for templates involving adult content, deceased people, endorsements, or protected-attribute defaults. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhy2015/hidream-model-gen) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zhy2015) <br>
- [Vivago AI](https://vivago.ai/) <br>
- [Vivago token endpoint](https://vivago.ai/prod-api/user/token) <br>
- [Vivago API base endpoint](https://vivago.ai/api/gw) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Files, Images, Videos, JSON] <br>
**Output Format:** [Command-line or Python API execution that produces JSON result files plus generated image or video URLs/assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Vivago API token in HIDREAM_AUTHORIZATION; generated resources are written under the configured output path, commonly assets/.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
