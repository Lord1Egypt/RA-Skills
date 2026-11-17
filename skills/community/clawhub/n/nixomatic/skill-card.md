## Description:

Run missing tools, runtimes, and development commands through on-demand Nix or Docker environments generated from nixomatic.com URLs without permanently installing software.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ereslibre](https://clawhub.ai/user/ereslibre)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to recover from missing tools, run one-shot utilities, and create reproducible project development environments through Nix or Docker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Nix flakes and generated tool environments can expose the current workspace to code and package execution.

Mitigation: Use the skill only in repositories where remote flakes are acceptable, prefer pinned revisions or local flakes, and get explicit approval before running environment commands.

Risk: Docker execution mounts the current project directory into the container and may provide broad repository write access.

Mitigation: Use read-only or narrow mounts when practical, avoid directories containing secrets, and review the exact Docker command before execution.

Risk: README maintenance behavior can modify project documentation after environment setup.

Mitigation: Ask before editing README files and review the generated Development Environment section before committing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ereslibre/skills/nixomatic)
- [Server-resolved source: ereslibre/homelab](https://github.com/ereslibre/homelab/tree/main/dotfiles/assets/hermes/skills/nixomatic)
- [Nixomatic](https://nixomatic.com)
- [NixOS package search](https://search.nixos.org/packages)
- [Install Nix](https://nixos.org/download/)
- [Install Docker](https://docs.docker.com/get-docker/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or edit a README Development Environment section after successful environment setup.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
