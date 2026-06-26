## Description: <br>
Generate images via APIYI (Gemini 3.1 Flash Image Preview) from text descriptions, with keyword extraction, prompt restructuring, and direct image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunni123](https://clawhub.ai/user/yunni123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn text descriptions into APIYI-generated images. It guides prompt selection and restructuring, then runs a Python script to submit the confirmed prompt and save the resulting image locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Final image prompts are sent to APIYI, which may expose sensitive user-provided text to an external service. <br>
Mitigation: Avoid private, confidential, or regulated data in prompts and only generate after the user confirms the final prompt. <br>
Risk: The skill requires an APIYI API key and can accept a key on the command line. <br>
Mitigation: Prefer environment or protected OpenClaw configuration storage over command-line key arguments. <br>
Risk: Generated image files are written to local paths and custom filenames can overwrite existing files. <br>
Mitigation: Choose output filenames deliberately, use timestamped names where practical, and review the saved path before relying on the file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yunni123/nanobanana2-apiyi) <br>
- [APIYI Gemini image generation endpoint](https://api.apiyi.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated images are saved as PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an APIYI API key; supports 1:1, 16:9, and 9:16 aspect ratios with 1K or 2K image size options.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
