## Description: <br>
Generates 3D models from text prompts or images using Tencent Cloud Hunyuan 3D 3.0 and 3.1, including text-to-3D, image-to-3D, multi-view, geometry-only, sketch, and smart-topology workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neck-cn](https://clawhub.ai/user/Neck-cn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to submit Tencent Cloud Hunyuan 3D generation jobs from text, image, or multi-view image inputs and retrieve generated model file URLs. It supports one-step submit-and-poll usage as well as separate submit and query workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal script execution can automatically install the unpinned tencentcloud-sdk-python package into the user's Python environment. <br>
Mitigation: Install reviewed and pinned dependencies in a controlled virtual environment before running the skill scripts. <br>
Risk: Prompts, images, and multi-view image references are sent to Tencent Cloud for 3D generation. <br>
Mitigation: Use only inputs appropriate for Tencent Cloud processing and avoid sending confidential or restricted images unless approved for that service. <br>
Risk: The skill requires Tencent Cloud credentials in environment variables. <br>
Mitigation: Provide credentials through scoped environment variables or temporary credentials and avoid hard-coding secrets in scripts, prompts, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Neck-cn/hy-3d-generation) <br>
- [Tencent Cloud 3D Visual Creation Console](https://console.cloud.tencent.com/ai3d) <br>
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [JSON responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Tencent Cloud job IDs, status values, generated 3D model file URLs, and optional preview image URLs; result URLs may be time-limited.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
