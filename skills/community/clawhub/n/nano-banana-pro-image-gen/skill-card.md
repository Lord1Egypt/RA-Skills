## Description: <br>
Image generation and editing skill for creating new images or modifying existing images through APIYI's NanoBananaPro image service, with support for common aspect ratios and 1K, 2K, and 4K resolution options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate marketing, social media, presentation, personal creative, and product images from prompts, or to edit existing images with natural-language instructions. It is designed to run local Node.js or Python commands that call the APIYI-hosted image generation endpoint and save image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference or edit images are sent to APIYI and downstream model services. <br>
Mitigation: Use the skill only when that external processing is acceptable, and avoid submitting secrets, private documents, or sensitive images. <br>
Risk: The skill requires an APIYI API key, which could be exposed if passed directly on the command line. <br>
Mitigation: Prefer the APIYI_API_KEY environment variable and avoid sharing command histories or logs that contain credentials. <br>


## Reference(s): <br>
- [Common usage scenarios](references/scene.md) <br>
- [APIYI service](https://api.apiyi.com) <br>
- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/nano-banana-pro-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PNG image files, may accept up to 14 input images for editing, and requires APIYI_API_KEY or an API key argument.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
