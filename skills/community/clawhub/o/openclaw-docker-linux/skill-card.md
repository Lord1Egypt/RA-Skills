## Description:

Run OpenClaw inside Docker on Linux and configure remote access through Tailscale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Linux system administrators use this skill to install and configure OpenClaw in Docker, manage its gateway, and enable remote access through Tailscale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker administration can grant lasting root-equivalent access to the host.

Mitigation: Review the setup commands and Docker group implications before granting access; remove group membership when it is no longer needed.

Risk: Containers can expose host files and credentials through mounted directories.

Mitigation: Keep optional credential mounts disabled unless required, and mount only directories the container needs.

Risk: An exposed gateway or stale Tailscale Serve route can make the service reachable remotely.

Mitigation: Keep host port publishing on 127.0.0.1, restrict tailnet access, and confirm forwarding is removed when stopping.

Risk: API keys, gateway tokens, and OpenClaw state may be exposed if local files or the container image are not protected.

Mitigation: Protect .env and OpenClaw state, verify and pin the container image before deployment, and review scripts before running them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/djc00p/skills/openclaw-docker-linux)
- [Quickstart](artifact/references/quickstart.md)
- [Docker configuration](artifact/references/docker-config.md)
- [Critical gotchas](artifact/references/gotchas.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Docker setup script](artifact/references/docker-setup.sh)
- [Container startup script](artifact/references/start.sh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline shell commands, scripts, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup steps, operational commands, security guidance, and troubleshooting advice]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
