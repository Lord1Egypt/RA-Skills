## Description:

PC Master helps an agent control a Windows PC from WSL2 by opening and closing applications, managing processes, taking screenshots, controlling windows, and working with Windows files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amirgu](https://clawhub.ai/user/amirgu)

### License/Terms of Use:


## Use Case:

Developers and power users working in WSL2 use this skill to let an agent inspect and control the Windows host for application management, process checks, screenshots, file operations, and system information tasks. It is intended for trusted Windows desktop automation where the user wants host-level actions performed from a WSL2 shell.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad Windows host control from WSL2, including process management, screenshots, and Windows file access.

Mitigation: Use it only on trusted hosts when the user explicitly wants Windows desktop control, and confirm exact targets before executing host-level actions.

Risk: Forced app termination, arbitrary app names, URLs, screenshots, and file paths can disrupt work or expose sensitive local information.

Mitigation: Treat those inputs as sensitive, avoid untrusted or pasted command-like input, and ask for confirmation before terminating apps, opening URLs, capturing screenshots, or accessing Windows paths.

## Reference(s):

- [Common Windows App Executable Names](references/windows-apps.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a WSL2 environment with Windows interop and can affect the Windows host.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
