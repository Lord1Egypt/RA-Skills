## Description: <br>
Guides an agent through using Grok Imagine to generate images from user prompts, save them locally, and optionally send them through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[279458179](https://clawhub.ai/user/279458179) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to create an image with Grok Imagine, then save the generated image and optionally share the selected local file through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can open Grok Imagine in the user's browser profile and operate the desktop to save generated images. <br>
Mitigation: Confirm the intended browser account, close unrelated sensitive windows, and review the generated image before saving or sharing it. <br>
Risk: The workflow can send a selected local image file to Feishu. <br>
Mitigation: Replace example file paths with the actual intended image and confirm the Feishu recipient or channel before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/279458179/grok-image-generate) <br>
- [Grok Imagine](https://grok.com/imagine) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown with JavaScript and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow may reference local image file paths selected by the user or agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
