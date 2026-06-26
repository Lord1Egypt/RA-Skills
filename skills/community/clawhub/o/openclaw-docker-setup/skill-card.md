## Description: <br>
Install and configure a fully operational Dockerized OpenClaw instance on macOS from scratch, including browser pairing, Discord channel setup, and optional Gmail and Google Drive integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and OpenClaw users use this skill to set up an isolated Docker-based OpenClaw instance on macOS, configure authentication and Discord access, and optionally connect Gmail or Google Drive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup handles live credentials for Anthropic, Discord, Gmail, and Google Drive, and some steps may display or persist tokens. <br>
Mitigation: Review the setup before installation, use dedicated bot or service accounts where possible, avoid sharing terminal output, and rotate any token or password that appears in logs or screenshots. <br>
Risk: The Dockerized service exposes a local dashboard and optional external integrations. <br>
Mitigation: Bind exposed ports as tightly as possible, keep access allowlists current, and avoid broad personal account access unless the operator accepts that exposure. <br>
Risk: Optional integration steps download external command-line tools. <br>
Mitigation: Prefer pinned or checksummed downloads and review the downloaded tools before use. <br>


## Reference(s): <br>
- [OpenClaw Docker Setup on ClawHub](https://clawhub.ai/chunhualiao/openclaw-docker-setup) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Pitfalls and Solutions](references/pitfalls.md) <br>
- [Gmail Setup via Himalaya](references/gmail-setup.md) <br>
- [Google Drive Setup via gog](references/google-drive-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive setup flow for macOS Docker environments] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
