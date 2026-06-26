## Description: <br>
Generate/edit images with nanobanana2 (Gemini 3.1 Flash Image preview). Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 512/1K/2K/4K; aspect ratios; use --input-image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zealman2025](https://clawhub.ai/user/zealman2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to generate new images or edit existing local images through Google's Gemini image API, with controls for prompt, input image, resolution, aspect ratio, and output filename. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to Google's Gemini API for third-party processing. <br>
Mitigation: Use this skill only with prompts and images that may be processed under the applicable Google API terms and privacy requirements; avoid confidential or regulated images unless those requirements allow it. <br>
Risk: API keys may be exposed if pasted into chat or command arguments. <br>
Mitigation: Prefer GEMINI_API_KEY or a platform secret store instead of passing API keys in conversation text or shell history. <br>
Risk: Generated or edited images may not match the intended prompt, resolution, or editing constraint. <br>
Mitigation: Use the documented draft-iterate-final workflow, inspect outputs before reuse, and keep filenames unique so previous outputs are not overwritten unintentionally. <br>


## Reference(s): <br>
- [Google Gemini API image generation documentation](https://ai.google.dev/gemini-api/docs/image-generation?hl=zh-cn) <br>
- [ClawHub skill page](https://clawhub.ai/zealman2025/nanobanana2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands; generated PNG image files and saved file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated or edited images are saved to the user's working directory or to the path supplied in the filename argument.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
