## Description:

Install Chinese/CJK fonts on Linux hosts using distro packages and fontconfig verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[totongf](https://clawhub.ai/user/totongf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and automation agents use this skill to install and verify Chinese/CJK font support on Linux servers, containers, desktops, screenshots, PDFs, browser automation, and headless Chrome or Playwright environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer changes system or container font packages and may require a privileged shell.

Mitigation: Run `scripts/install_chinese_fonts.sh --dry-run` or `--verify-only` first, and execute the installer with privileges only when system-wide CJK font installation is intended.

Risk: The bundled script supports only dnf, yum, and apt-get package managers.

Mitigation: Use the documented manual font installation fallback when those package managers are unavailable or when a specific font family or version is required.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and an executable shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run and verify-only modes for package installation and fontconfig checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
