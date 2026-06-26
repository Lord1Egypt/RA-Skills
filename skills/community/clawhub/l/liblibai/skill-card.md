## Description: <br>
Use the LiblibAI API to generate AI images from text or existing images, including Ultra models, ComfyUI workflows, and file uploads for creative design and visual content work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shishugen](https://clawhub.ai/user/shishugen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content creators use this skill to call LiblibAI image-generation services from an agent workflow for text-to-image, image-to-image, file upload, and asynchronous generation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and uploaded source images are sent to LiblibAI for generation. <br>
Mitigation: Avoid confidential images, regulated data, and sensitive prompts unless the use has been approved for LiblibAI processing. <br>
Risk: The skill requires LiblibAI access and secret keys. <br>
Mitigation: Use dedicated or revocable API keys and do not print, commit, or share credentials. <br>
Risk: Generated outputs may consume paid LiblibAI credits. <br>
Mitigation: Test with smaller resolutions or lower-cost settings before running larger batches. <br>


## Reference(s): <br>
- [LiblibAI website](https://liblibai.com) <br>
- [LiblibAI API documentation](https://liblibai.feishu.cn/wiki/UAMVw67NcifQHukf8fpccgS5n6d) <br>
- [liblibai npm package](https://www.npmjs.com/package/liblibai) <br>
- [ClawHub skill page](https://clawhub.ai/shishugen/liblibai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated image or task status URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return LiblibAI task UUIDs, status text, image URLs, point costs, and account balance details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
