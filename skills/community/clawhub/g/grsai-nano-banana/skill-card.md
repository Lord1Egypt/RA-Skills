## Description: <br>
Uses the grsai nano-banana model to generate images from text prompts or reference-image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ruiww](https://clawhub.ai/user/Ruiww) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent generate or transform images with grsai and save the resulting image file locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and reference image URLs to the grsai provider. <br>
Mitigation: Use the skill only when the provider is trusted for the intended content and avoid sending sensitive prompts or private image URLs. <br>
Risk: The skill requires a paid grsai API key. <br>
Mitigation: Use a dedicated, revocable API key with spending limits where possible, and avoid passing real keys directly in shell command history. <br>
Risk: Changing the base URL redirects requests to a different service. <br>
Mitigation: Keep the default base URL unless the replacement endpoint is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ruiww/grsai-nano-banana) <br>
- [grsai homepage](https://grsai.ai/) <br>
- [grsai nano-banana documentation](https://grsai.ai/zh/dashboard/documents/nano-banana) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated images are saved as PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, curl, Python 3.10+, requests, and a grsai API key; supports async polling and custom output directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
