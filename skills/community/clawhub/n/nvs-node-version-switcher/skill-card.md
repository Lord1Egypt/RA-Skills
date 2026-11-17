## Description:

Manage Node.js versions using NVS (Node Version Switcher). Use when switching Node.js versions, installing new versions, managing version aliases, or when the user mentions NVS, node version management, or needs to change the active Node.js version in the current environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuzeyu22](https://clawhub.ai/user/zhuzeyu22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, switch, and troubleshoot Node.js versions with NVS across local development environments and project workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled installer can fetch and immediately run unpinned remote shell code.

Mitigation: Review the installer before use, prefer a trusted package manager or pinned verified NVS release, and run the bundled install script only after accepting the remote-code execution and shell-configuration changes.

Risk: Automatic switching and persistent defaults can change the active Node.js version for future shell sessions or directories.

Mitigation: Confirm the intended project version before enabling auto-switching or setting persistent defaults, and verify the active version with NVS status commands.

## Reference(s):

- [NVS upstream repository](https://github.com/jasongin/nvs)
- [Node.js nightly downloads](https://nodejs.org/download/nightly/)
- [io.js distributions](https://iojs.org/dist/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, configuration snippets, and short explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OS-specific install commands, Node.js version selections, alias names, and troubleshooting checks.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
