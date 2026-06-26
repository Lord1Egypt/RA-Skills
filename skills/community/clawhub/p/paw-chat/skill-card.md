## Description: <br>
Install and manage Paw - a standalone web chat frontend for OpenClaw Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oriliz](https://clawhub.ai/user/oriliz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, update, or run Paw as a static web chat interface for an OpenClaw Gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The web UI stores a powerful OpenClaw Gateway token in browser storage. <br>
Mitigation: Use only trusted browser profiles and machines, treat the token like a password, and clear browser site data after use on shared or untrusted systems. <br>
Risk: Agent editing and scheduled-task controls can affect future OpenClaw behavior. <br>
Mitigation: Use these controls only when intentionally granting the UI administrative influence over agent files or scheduled tasks. <br>
Risk: Connecting through an untrusted hosted page, local file set, browser profile, or Gateway endpoint can expose credentials or actions. <br>
Mitigation: Install only from a trusted publisher and connect only to trusted Gateway endpoints. <br>


## Reference(s): <br>
- [Paw Chat on ClawHub](https://clawhub.ai/oriliz/paw-chat) <br>
- [OpenClaw Website](https://openclaw.ai) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) <br>
- [Paw Package Repository](https://github.com/openclaw/paw.git) <br>
- [Marked Markdown Parser](https://github.com/markedjs/marked) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation and operating instructions for a static OpenClaw web chat frontend.] <br>

## Skill Version(s): <br>
1.0.6 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
