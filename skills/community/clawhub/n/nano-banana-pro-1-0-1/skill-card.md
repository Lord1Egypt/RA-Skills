## Description: <br>
Generate and edit images with Nano Banana Pro using Google's Gemini 3 Pro Image API, including text-to-image and image-to-image workflows at 1K, 2K, and 4K resolutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guogithubname](https://clawhub.ai/user/guogithubname) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate new PNG images or edit existing images from prompts while keeping outputs in the user's working directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to Google's Gemini API when the skill runs. <br>
Mitigation: Avoid sensitive or regulated images unless the user intends to upload them to Google, and make the external API use clear before running the command. <br>
Risk: A Gemini API key is required and may be exposed if passed directly on the command line. <br>
Mitigation: Prefer the GEMINI_API_KEY environment variable over command-line API key arguments. <br>
Risk: Generated files are written to the requested filename or path. <br>
Mitigation: Use unique filenames in a directory the user controls to avoid overwriting or misplacing outputs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [PNG image files with terminal status text and saved-path output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key and supports optional input images plus 1K, 2K, and 4K resolution settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
