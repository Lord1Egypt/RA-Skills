## Description: <br>
Generate new images and edit existing images with xAI Grok Imagine from a local OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to run xAI Grok Imagine image generation and editing from a local OpenClaw workspace. It supports prompt-based generation, batch variations, source-image edits, style transfer, cleanup, background replacement, product art, and poster concepts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and source images are sent to xAI's remote API. <br>
Mitigation: Do not submit private prompts or source images unless sending them to xAI is acceptable for the user's environment. <br>
Risk: The xAI API key is sensitive credential material. <br>
Mitigation: Keep XAI_API_KEY protected and avoid exposing it in commands, logs, committed files, or shared output. <br>
Risk: Generated images, prompts, temporary URLs, and response metadata may remain in the local output directory. <br>
Mitigation: Review or clean the output directory when generated artifacts or metadata should not be retained. <br>


## Reference(s): <br>
- [xAI Grok Imagine reference](references/api-reference.md) <br>
- [Prompt Templates](references/prompt-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; the local script saves generated image files and JSON response metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY. Generation can request multiple outputs, and edit mode accepts one to three source images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
