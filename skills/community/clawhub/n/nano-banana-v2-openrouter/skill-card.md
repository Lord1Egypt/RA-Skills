## Description: <br>
Generates and edits images with Gemini 3.1 Flash Image Preview through OpenRouter, supporting text-to-image, image-to-image, and 0.5K, 1K, 2K, and 4K outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tclxhai-lv](https://clawhub.ai/user/tclxhai-lv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users use this skill to generate new images or edit existing images from prompts through OpenRouter. It helps agents produce command-line image generation and editing runs while preserving output paths for the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and input images are sent to OpenRouter and Gemini during generation or editing. <br>
Mitigation: Use the skill only when sharing that content with the model provider is acceptable for the user's privacy and compliance requirements. <br>
Risk: API keys can be exposed if pasted into chat or passed directly on the command line. <br>
Mitigation: Prefer OPENROUTER_API_KEY from the environment or a secret manager instead of passing keys in prompts or command history. <br>
Risk: Generated files may overwrite existing local files when reused filenames are supplied. <br>
Mitigation: Use unique timestamped output filenames and confirm output paths before running the script. <br>


## Reference(s): <br>
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions) <br>
- [ClawHub skill page](https://clawhub.ai/tclxhai-lv/nano-banana-v2-openrouter) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands and saved PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and OPENROUTER_API_KEY; generated or edited images are written as PNG files to the user's working directory or requested output path.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
