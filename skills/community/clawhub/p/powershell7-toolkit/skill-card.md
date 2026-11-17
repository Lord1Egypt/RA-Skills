## Description:

帮助 Windows 用户部署 PowerShell 7 和常用命令行工具，并配置 UTF-8 编码及日常 shell 设置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujianyu](https://clawhub.ai/user/yujianyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users on Windows use this skill to install or upgrade PowerShell 7 and supporting CLI tools, reduce encoding and command quoting problems, and configure shell defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may trust and execute packages from sources that have not been verified.

Mitigation: Review the package source and selected download before installation; compare it with official PowerShell release information and use the installer’s -CheckOnly option first.

Risk: Installation can change user files and settings, including PATH, PowerShell profiles, registry entries, and shell associations.

Mitigation: Review the scripts and planned changes before running them, keep a way to restore edited settings, and use -SkipDefaults when you only want to install the tools.

Risk: Several components were only partially inspected and one image could not be fully interpreted by the security scan.

Mitigation: Review the remaining package content and complete a security assessment before installation.

## Reference(s):

- [Project repository](https://github.com/yujianyu/ps7-toolkit)
- [PowerShell releases](https://github.com/PowerShell/PowerShell/releases)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with PowerShell code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-focused instructions for PowerShell 5.1 and PowerShell 7.]

## Skill Version(s):

1.1.8 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
