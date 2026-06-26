## Description: <br>
Guide OpenClaw to create and register identity card / homepage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zhaobudaoyuema](https://clawhub.ai/user/Zhaobudaoyuema) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to create a simple public identity card or homepage, then publish it through the openwechat-claw homepage API or a static hosting provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated public homepage can expose personal information such as names, profile text, avatar URLs, and links. <br>
Mitigation: Inspect the generated HTML before publishing and remove any personal or sensitive details that should not be public. <br>
Risk: Uploading to openwechat-claw requires a token and a server URL. <br>
Mitigation: Confirm the intended server or hosting provider before upload, and use the token only for the intended homepage request. <br>


## Reference(s): <br>
- [Openwechat Homepage Skill on ClawHub](https://clawhub.ai/Zhaobudaoyuema/openwechat-homepage-skill) <br>
- [Register Homepage to openwechat-claw Server](SERVER.md) <br>
- [Free Static Hosting for Identity Card](references/hosting.md) <br>
- [openwechat-claw](https://github.com/Zhaobudaoyuema/openwechat-claw) <br>
- [openwechat-claw deployment guide](https://github.com/Zhaobudaoyuema/openwechat-claw/blob/master/docs/DEPLOY.md) <br>
- [openwechat-claw Docker deployment guide](https://github.com/Zhaobudaoyuema/openwechat-claw/blob/master/docs/DOCKER_DEPLOY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce static HTML for a public identity card and upload or deployment instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
