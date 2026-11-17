## Description:

Build, debug, and contribute to the MEGAcmd project using C++, CMake, and vcpkg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alefsanderribeiro](https://clawhub.ai/user/alefsanderribeiro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compile MEGAcmd from source, configure development environments, run tests, debug server or client issues, create packages, and understand the project's internal architecture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes normal development commands that can change the host, including package installation, repository cloning, submodule initialization, Docker builds, and local installation.

Mitigation: Review commands before execution and prefer a dedicated development directory or isolated build environment.

Risk: Debugging or integration testing with real MEGA account data can expose account-specific files, folders, or logs to the working environment.

Mitigation: Use a test account or sanitized data when possible, and review before starting or debugging MEGAcmd with real account data.

## Reference(s):

- [MEGAcmd for Developer on ClawHub](https://clawhub.ai/alefsanderribeiro/skills/megacmd-developer)
- [MEGAcmd GitHub](https://github.com/meganz/MEGAcmd)
- [MEGA SDK](https://github.com/meganz/sdk)
- [vcpkg](https://github.com/microsoft/vcpkg)
- [CMake](https://cmake.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose host-changing development commands that require user approval before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
