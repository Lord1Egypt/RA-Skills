## Description: <br>
Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DyCathecorde](https://clawhub.ai/user/DyCathecorde) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate new images, edit a single image, or compose up to 14 input images through Google's Gemini image API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to Google Gemini. <br>
Mitigation: Avoid sensitive images or prompts unless permitted by the user's data policy. <br>
Risk: Gemini API credentials may be exposed if passed directly on the command line. <br>
Mitigation: Prefer a dedicated or limited API key stored in the environment. <br>
Risk: The script resolves Python dependencies with uv. <br>
Mitigation: Review uv-resolved dependencies when supply-chain control matters. <br>


## Reference(s): <br>
- [Google AI Documentation](https://ai.google.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands; runtime output is text plus saved PNG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; supports 1K, 2K, and 4K output resolutions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
