## Description: <br>
Generates images with Tencent HunyuanImage 3.0 from text prompts, with optional reference image URLs for image-to-image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mebusw](https://clawhub.ai/user/mebusw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to ask an agent to generate or vary images through Tencent Cloud HunyuanImage 3.0, including prompt, resolution, seed, watermark, and reference image options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference image URLs are sent to Tencent Cloud for processing. <br>
Mitigation: Use only prompts and images acceptable for Tencent Cloud processing, and avoid confidential prompts or private and signed reference image URLs. <br>
Risk: Tencent Cloud credentials are required for use. <br>
Mitigation: Use a dedicated least-privilege Tencent Cloud key and keep the local .env file private. <br>
Risk: Generated image URLs are valid for a limited time. <br>
Mitigation: Show the full URL in the agent response and remind users to save outputs within the one-hour validity window. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mebusw/hunyuan-text-to-image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image URLs are temporary; prompts and reference image URLs are sent to Tencent Cloud.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
