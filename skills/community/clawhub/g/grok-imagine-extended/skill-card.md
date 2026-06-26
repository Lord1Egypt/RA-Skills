## Description: <br>
Generate images and videos using xAI Grok Imagine Extended for text-to-image, image editing, text-to-video, and image-to-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ademczuk](https://clawhub.ai/user/ademczuk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to call xAI Grok Imagine for image generation, image editing, video generation, and still-image animation, then report the saved media path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and input media are sent to xAI for generation or editing. <br>
Mitigation: Avoid sensitive prompts or private media unless the user intends to send them to xAI. <br>
Risk: Using the skill can incur xAI API charges. <br>
Mitigation: Confirm the selected model, image count, video duration, and expected costs before running generation. <br>
Risk: The skill can read an API key from a plaintext fallback file. <br>
Mitigation: Prefer XAI_API_KEY in the environment and avoid storing credentials in plaintext files such as ~/keys.txt. <br>
Risk: Generated media files are written to the requested output path. <br>
Mitigation: Use a dedicated output folder and review saved files before relying on or sharing them. <br>


## Reference(s): <br>
- [xAI Image Generations Guide](https://docs.x.ai/docs/guides/image-generations) <br>
- [ClawHub Grok Imagine Release](https://clawhub.ai/ademczuk/grok-imagine-extended) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with shell commands and saved media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes image or video files, prints saved paths, requires XAI_API_KEY, and may incur xAI API usage charges.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
