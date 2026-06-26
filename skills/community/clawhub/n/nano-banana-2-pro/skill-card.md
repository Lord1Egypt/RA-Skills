## Description: <br>
Generate/edit images with Nano Banana 2 (Gemini 3.1 Flash Image). Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 512/1K/2K/4K; 14 aspect ratios; up to 14 input images; thinking levels; use --input-image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gybin02](https://clawhub.ai/user/gybin02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative agents use this skill to generate new images or edit existing images through Google's Gemini image API, with controls for resolution, aspect ratio, model choice, input images, and thinking level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented commands point to a different local skill folder than this release's bundled script. <br>
Mitigation: Verify or correct the command path before running so the agent executes this skill's reviewed script. <br>
Risk: Prompts and input images are sent to Google's API, and the script requires a Gemini API key. <br>
Mitigation: Use GEMINI_API_KEY when possible and only provide prompts, images, and credentials that are appropriate to send to the external API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gybin02/nano-banana-2-pro) <br>
- [Publisher profile](https://clawhub.ai/user/gybin02) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Image files, Text] <br>
**Output Format:** [Markdown guidance with inline bash commands; the script writes PNG files and prints status or error text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, a Gemini API key, google-genai, pillow, and Python >=3.10; generated images are saved to the requested filename.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
