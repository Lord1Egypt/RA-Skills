## Description:

Complete step-by-step installation guide for OpenClaw on Windows 10/11 with WSL2, including common pitfalls and solutions from real installation experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aslancootl](https://clawhub.ai/user/aslancootl)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and AI assistants use this skill to guide installation and troubleshooting of OpenClaw on Windows 10/11 through WSL2. It covers one-click and custom-drive WSL setup, OpenClaw installation, environment configuration, and common recovery steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified online installers or mirrored downloads may execute code with elevated privileges.

Mitigation: Use official Microsoft, Ubuntu, Node.js, and OpenClaw release channels; verify signatures or hashes where available; avoid piping downloaded scripts directly into a shell.

Risk: Broad administrator, root, or passwordless sudo access can expand the impact of a bad command or compromised installer.

Mitigation: Run routine OpenClaw tasks as a normal WSL user, do not add `NOPASSWD: ALL`, and reserve administrator or root sessions for narrowly scoped setup steps.

Risk: Troubleshooting steps that weaken host protections can leave Windows exposed after installation.

Mitigation: Do not disable antivirus or Memory Integrity as a default fix, and restrict any firewall rule to the smallest trusted scope needed for the OpenClaw service.

Risk: The scanner verdict is suspicious because the guide combines real installation instructions with security-weakening recommendations.

Mitigation: Review and tighten the guide before execution, especially download, privilege, firewall, and host-security steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aslancootl/skills/openclaw-win-install-ai-assist)
- [Microsoft WSL releases](https://github.com/microsoft/WSL/releases/latest)
- [Ubuntu 22.04 WSL images](https://cloud-images.ubuntu.com/wsl/jammy/current/)
- [Node.js v22.18.0 downloads](https://nodejs.org/dist/v22.18.0/)
- [OpenClaw source archive](https://github.com/openclaw-ai/openclaw/archive/refs/heads/main.zip)
- [Microsoft WSL manual install documentation](https://learn.microsoft.com/zh-cn/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package.)
- [OpenClaw Browser Relay extension](https://chromewebstore.google.com/detail/openclaw-browser-relay/nglingapjinhecnfejdcpihlpneeadjp)
- [Feishu Developer Portal](https://open.feishu.cn/?lang=zh-CN)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese installation guidance for Windows and WSL2 workflows.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
