## Description:

Deploy OpenClaw cloud gateway scenarios with Tailscale, SSH tunneling, environment checks, firewall setup, persistent services, and local control guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marshong-86](https://clawhub.ai/user/marshong-86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select and run OpenClaw deployment plans for cloud gateway, remote gateway, or dual cloud/local gateway setups. It helps prepare dependencies, network access, service startup, diagnostics, and follow-up configuration commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release uses root/admin automation and creates persistent services.

Mitigation: Review each startup task and systemd service before installation, prefer a dedicated non-root service account where supported, and document removal steps before production use.

Risk: The scripts use curl-to-shell and unpinned package installation patterns.

Mitigation: Replace remote installer pipes with verified package installs, pin npm and operating-system package versions, and validate checksums or trusted package sources.

Risk: Gateway and sync ports are opened for network access.

Mitigation: Restrict ports to Tailscale or other trusted sources in host firewalls and cloud security groups, and avoid exposing ports 18789 or 18790 publicly.

Risk: Some gateway flows use insecure WebSocket URLs or allow-unconfigured startup behavior.

Mitigation: Use secure transport where supported, remove allow-unconfigured flags unless explicitly needed, and verify authentication is enabled before accepting remote connections.

Risk: Generated tokens and local gateway configuration can grant access to the deployment.

Mitigation: Store tokens with restrictive permissions, avoid sharing diagnostic output that contains secrets, and rotate tokens after setup or troubleshooting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marshong-86/skills/openclaw-two-way-deployment)
- [Tailscale Download](https://tailscale.com/download)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash and PowerShell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes privileged deployment steps, gateway configuration, firewall changes, service setup, and diagnostic commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
