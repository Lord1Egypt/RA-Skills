## Description: <br>
Nano Banana Pro helps agents generate and edit PNG images with Nano Banana 2 (Gemini 3.1 Flash Image), including image-to-image workflows at 1K, 2K, and 4K. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wegoagain-dev](https://clawhub.ai/user/wegoagain-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative practitioners use this skill to have an agent generate new images or edit existing images through Google's Gemini image API while controlling resolution and output filename. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and input images are sent to Google's Gemini service. <br>
Mitigation: Use the skill only when the user is comfortable sending that content to Gemini and avoid sensitive inputs unless approved. <br>
Risk: API keys may be exposed if passed directly on the command line. <br>
Mitigation: Prefer the GEMINI_API_KEY environment variable instead of the --api-key argument. <br>
Risk: The script creates parent directories and writes the generated PNG to the requested path. <br>
Mitigation: Choose output filenames carefully and verify the target path before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wegoagain-dev/nano-banana-pro-fork) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script saves PNG images to the selected local output path and prints the resolved file path.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
