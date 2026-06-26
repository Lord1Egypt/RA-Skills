## Description: <br>
Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image). Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 1K/2K/4K; use --input-image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate new images or edit existing images through Google's Gemini image service, including iterative draft-to-final image workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to Google's Gemini service for external processing. <br>
Mitigation: Do not submit screenshots, documents, credentials, private photos, regulated data, or other sensitive content unless external processing is acceptable. <br>
Risk: Generation and editing require a valid Gemini API key and may fail because of missing credentials, permissions, quota, or inaccessible input image paths. <br>
Mitigation: Check that uv is available, GEMINI_API_KEY or --api-key is set, and any --input-image path exists before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/nano-banana-pro) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/steipete) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated or edited PNG image files are saved to the working directory.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports prompt text, optional input image path, output filename, API key, and 1K, 2K, or 4K image resolution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
