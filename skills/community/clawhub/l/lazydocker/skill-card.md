## Description:

Helps agents guide users through lazydocker, a terminal UI for managing Docker and Docker Compose resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to install and operate lazydocker for Docker containers, images, volumes, networks, and Docker Compose services. It supports setup checks, TUI navigation, configuration, log and resource inspection, remote Docker connection guidance, cleanup workflows, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance can run mutable remote code or download latest release artifacts.

Mitigation: Prefer package-manager installation or pinned releases with checksum or signature verification, and review commands before execution.

Risk: Docker socket access, container exec, prune/delete, and environment-variable inspection can grant broad host control or expose sensitive data.

Mitigation: Confirm the target host and environment before executing Docker operations, avoid exposing Docker on tcp://0.0.0.0:2375, and use SSH or TLS-protected remote Docker connections.

Risk: Remote Docker management can affect the wrong host if DOCKER_HOST or Docker context is misconfigured.

Mitigation: Verify Docker context and daemon identity with docker info before launching lazydocker or running lifecycle operations.

## Reference(s):

- [Installation guide](guides/01-installation.md)
- [Quickstart guide](guides/02-quickstart.md)
- [Advanced usage guide](guides/03-advanced-usage.md)
- [Troubleshooting guide](troubleshooting.md)
- [lazydocker GitHub project](https://github.com/jesseduffield/lazydocker)
- [lazydocker releases](https://github.com/jesseduffield/lazydocker/releases)
- [lazydocker configuration documentation](https://github.com/jesseduffield/lazydocker/blob/master/docs/Config.md)
- [lazydocker issues](https://github.com/jesseduffield/lazydocker/issues)
- [lazydocker discussions](https://github.com/jesseduffield/lazydocker/discussions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and YAML or JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker and lazydocker binaries; guidance may include Docker socket access, container exec, cleanup, and remote host connection steps.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
