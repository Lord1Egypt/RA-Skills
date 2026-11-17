## Description:

Koji helps agents provide guidance, commands, and configuration for managing Koji build system tasks, packages, tags, repositories, users, SRPM/RPMs, buildroots, and build operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and build system administrators use this skill to get Koji CLI/API guidance for builds, package ownership, tags, repositories, users, authentication, troubleshooting, and CI/CD-oriented workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact administrative Koji operations could delete, cancel, or change builds, users, permissions, repositories, or tags.

Mitigation: Require explicit user confirmation before delete, cancel-all, ownership, permission, user, repository, or tag changes.

Risk: Disabling TLS verification can weaken the safety of Koji server connections.

Mitigation: Keep TLS verification enabled and confirm certificate settings before using generated configuration guidance.

Risk: Koji authentication material such as keytabs, private keys, certificates, tickets, or config contents may be sensitive.

Mitigation: Avoid exposing credentials or configuration secrets in chat, command output, logs, or generated documentation.

## Reference(s):

- [Koji Documentation](https://koji.fedoraproject.org/docs/)
- [Koji API Documentation](https://koji.fedoraproject.org/docs/developer/)
- [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
- [Fedora DistGit](https://src.fedoraproject.org/)
- [Fedora Build System](https://fedoraproject.org/wiki/Build_System)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory Koji commands and configuration examples for review before execution.]

## Skill Version(s):

2.0.0 (source: evidence release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
