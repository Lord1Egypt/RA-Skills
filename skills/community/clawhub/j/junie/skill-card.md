## Description:

Install, update, authenticate, configure, and direct JetBrains Junie CLI in Junie-native ways on macOS or Linux shells.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inertia186](https://clawhub.ai/user/inertia186)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install or configure JetBrains Junie CLI, bootstrap Junie-native project layout, and brief Junie as a focused implementation or review partner under host-agent oversight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can download and execute external JetBrains Junie installer or package-manager code as the current user.

Mitigation: Install only when JetBrains Junie is trusted, prefer a reviewed or pinned package-manager path where available, and review the installer path before execution.

Risk: The skill can persist Junie settings in user or project configuration files, including provider choices and optional credentials.

Mitigation: Inspect config changes before writing them and keep API keys in environment variables unless durable storage is explicitly desired.

Risk: Launching Junie tasks may share repository context with the selected model or provider.

Mitigation: Confirm the effective model and provider before launch, and scope prompts or read-only checks to the minimum repository context needed.

## Reference(s):

- [Headless Terminal Fit](references/headless-terminal-fit.md)
- [Junie Doc Notes](references/junie-doc-notes.md)
- [Junie CLI Account and Token Page](https://junie.jetbrains.com/cli)
- [Junie macOS/Linux Installer](https://junie.jetbrains.com/install.sh)
- [Junie Windows Installer](https://junie.jetbrains.com/install.ps1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and helper-script guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or merge Junie configuration files and may run local installation, bootstrap, or usage-summary helper scripts when directed.]

## Skill Version(s):

1.0.0 (source: release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
