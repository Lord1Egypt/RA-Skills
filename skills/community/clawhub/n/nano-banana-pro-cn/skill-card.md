## Description: <br>
Nano Banana Pro CN helps agents generate and edit images through APIYI's NanoBananaPro image service with configurable aspect ratios, resolutions, and optional input images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate new images or edit existing images for social media, marketing, personal creative, and presentation workflows through APIYI-backed image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to APIYI for remote processing. <br>
Mitigation: Use only with APIYI and publisher trust, and avoid sending confidential, personal, or regulated images unless remote processing is acceptable. <br>
Risk: API credentials can be exposed if shared broadly or passed through command history. <br>
Mitigation: Use a dedicated API key and prefer environment variables or a secret manager over command-line keys. <br>


## Reference(s): <br>
- [Common use cases](references/scene.md) <br>
- [APIYI](https://apiyi.com/) <br>
- [APIYI API console](https://api.apiyi.com) <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/nano-banana-pro-cn) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an APIYI API key, prompt text, optional output filename, aspect ratio, resolution, and up to 14 input images.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
