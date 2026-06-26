## Description: <br>
Uses a local helper script and GMNCODE API key as a fallback for image understanding when the built-in OpenClaw image tool is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[io2077](https://clawhub.ai/user/io2077) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route image-description, character-identification, style-analysis, and screenshot-understanding tasks through a local GMNCODE helper when the standard image tool is not working. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an unreviewed local helper script that can send images and prompts to GMNCODE. <br>
Mitigation: Review the helper script before installation and use the skill only with images approved for GMNCODE processing. <br>
Risk: The skill requires GMNCODE_API_KEY, which could expose broader account access if mishandled. <br>
Mitigation: Use a limited-scope API key and manage it through the local environment rather than embedding it in skill files or prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/io2077/local-gmncode-vision) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Image prompts are sent through a local helper that uses GMNCODE_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
