## Description: <br>
Generate or edit images with Nano Banana Pro, Gemini 3 Pro Image, using text-to-image and image-to-image workflows with 1K, 2K, and 4K output options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Keyserkazi1](https://clawhub.ai/user/Keyserkazi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate new PNG images or edit existing images through Google's Gemini image API. It is suited for creative image creation, image modification, prompt iteration, and resolution-controlled output generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gemini API keys may be exposed if passed directly on the command line. <br>
Mitigation: Prefer GEMINI_API_KEY or another secure secret workflow, and use a limited-scope Gemini key where possible. <br>
Risk: Prompts and input images are processed by Google's Gemini service. <br>
Mitigation: Avoid sending confidential prompts or images unless the user accepts external processing by Google. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Keyserkazi1/nano-banana-pro1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated image files are saved as PNG by the skill script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses prompt, filename, optional input image, optional resolution, and Gemini API key parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
