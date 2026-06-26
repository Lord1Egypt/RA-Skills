## Description: <br>
Complete step-by-step installation guide for OpenClaw on Windows 10/11 with WSL2, includes common pitfalls and solutions from real installation experience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aslancootl](https://clawhub.ai/user/aslancootl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and AI assistants use this skill to guide OpenClaw installation on Windows 10/11 with WSL2, including WSL setup, Ubuntu configuration, OpenClaw installation, desktop shortcuts, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide includes broad security and privilege changes, including passwordless sudo and optional root usage. <br>
Mitigation: Review and modify privilege-related steps before installation; prefer a normal user with standard sudo authentication unless there is a clear operational need. <br>
Risk: The guide runs downloaded installers and an install script during setup. <br>
Mitigation: Verify downloaded files and installer sources before execution, especially when using mirrors or pre-downloaded files. <br>
Risk: The guide includes firewall changes and troubleshooting suggestions that may reduce local security controls. <br>
Mitigation: Restrict or skip inbound firewall rules unless remote access is required, and avoid disabling antivirus or Core Isolation except as a temporary last-resort troubleshooting step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aslancootl/openclaw-win-install-ai-assist) <br>
- [Microsoft WSL releases](https://github.com/microsoft/WSL/releases/latest) <br>
- [Microsoft WSL manual install guidance](https://learn.microsoft.com/zh-cn/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package) <br>
- [Ubuntu 22.04 LTS WSL image](https://cloud-images.ubuntu.com/wsl/jammy/current/) <br>
- [Node.js Linux distribution](https://nodejs.org/dist/v22.18.0/) <br>
- [OpenClaw source archive](https://github.com/openclaw-ai/openclaw/archive/refs/heads/main.zip) <br>
- [OpenClaw install script](https://molt.bot/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese installation steps with troubleshooting notes.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence; artifact metadata/frontmatter show 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
