## Description:

One-click remote OpenClaw deployment via SSH that auto-detects the target environment and selects Docker, Podman, npm, pnpm, or installer-based setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and configure OpenClaw on VPS, cloud, or other remote servers over SSH. It supports automated multi-machine deployment, async progress logging, and post-install model, channel, and gateway configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill performs remote OpenClaw installation but uses risky SSH and installer practices.

Mitigation: Review before use on production hosts, prefer key-based SSH with verified known_hosts, and avoid password-based SSH mode.

Risk: The release security guidance warns about curl-to-bash installer paths and live upstream deployment channels.

Mitigation: Run those installer paths only when the upstream scripts and deployment channel are trusted, and pin package versions or container image digests where possible.

Risk: The release security guidance warns against inline API keys and recommends secret references.

Mitigation: Use environment-variable or secret-reference modes for provider credentials, and avoid passing API keys inline in command arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codeblackhole1024/skills/openclaw-remote-install)
- [OpenClaw installer endpoint](https://openclaw.ai/install.sh)
- [OpenClaw CLI installer endpoint](https://openclaw.ai/install-cli.sh)
- [Docker convenience installer endpoint](https://get.docker.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and configuration options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SSH, package-manager, container, and API-key configuration commands for remote execution.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
