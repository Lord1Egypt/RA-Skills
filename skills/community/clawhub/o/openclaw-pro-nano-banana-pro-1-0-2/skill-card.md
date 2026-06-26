## Description: <br>
Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeayoo](https://clawhub.ai/user/jeayoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to generate new images, edit a single input image, or compose up to 14 input images through Gemini 3 Pro Image from an OpenClaw workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to Google's Gemini API. <br>
Mitigation: Use only prompts and images whose external API processing is acceptable for the user's data handling requirements. <br>
Risk: The script creates the requested output file path. <br>
Mitigation: Choose output filenames deliberately and review the saved path before relying on or sharing the generated image. <br>


## Reference(s): <br>
- [Google AI for Developers](https://ai.google.dev/) <br>
- [Google AI Studio API key setup](https://aistudio.google.com/app/apikey) <br>
- [ClawHub release page](https://clawhub.ai/jeayoo/openclaw-pro-nano-banana-pro-1-0-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Text status output with a saved PNG image file path and MEDIA attachment line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, Python 3.10 or newer, and GEMINI_API_KEY; supports 1K, 2K, and 4K output resolutions plus selected aspect ratios.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
