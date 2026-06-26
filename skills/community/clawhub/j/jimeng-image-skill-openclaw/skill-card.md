## Description: <br>
Generate images from text prompts using the Jimeng API with customizable size, scale, seed, and output path via Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gkhcsc](https://clawhub.ai/user/gkhcsc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to call the Jimeng/Volcengine image generation API from a text prompt and save the returned PNG locally for delivery to a user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Jimeng/Volcengine API credentials. <br>
Mitigation: Use a dedicated API key where possible and manage credentials through environment variables or the configured local environment file. <br>
Risk: Prompts are sent to an external image generation provider. <br>
Mitigation: Avoid confidential or sensitive prompt content unless that provider and account setup are approved for the use case. <br>
Risk: Generated PNG files are saved locally and may contain sensitive content. <br>
Mitigation: Review, protect, or delete files in the output directory according to local data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gkhcsc/jimeng-image-skill-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Python script parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script saves generated PNG files to the configured output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
