## Description: <br>
Analyze images using MiniMax CLI (mmx-cli) for vision tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gawainchin](https://clawhub.ai/user/gawainchin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route explicit MiniMax vision requests through the MiniMax CLI for local-file or URL-based image analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MiniMax API keys can be exposed through shared terminals, logs, screenshots, or committed files. <br>
Mitigation: Authenticate only in trusted environments and avoid displaying or storing real API keys in shared or persistent outputs. <br>
Risk: Images submitted for analysis may contain sensitive content and are sent to MiniMax through the CLI. <br>
Mitigation: Analyze only images whose contents the user is comfortable sending to MiniMax. <br>
Risk: Users may install or authenticate against an unintended CLI package or account page. <br>
Mitigation: Verify the mmx-cli package and MiniMax account page before installation or authentication. <br>


## Reference(s): <br>
- [MiniMax Vision Skill on ClawHub](https://clawhub.ai/gawainchin/minimax-vision-skill) <br>
- [gawainchin ClawHub Profile](https://clawhub.ai/user/gawainchin) <br>
- [MiniMax API Key Page](https://platform.minimax.io/user-center/basic-information/interface-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and returned image-analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mmx-cli, MiniMax authentication, and user-provided local image paths or image URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
