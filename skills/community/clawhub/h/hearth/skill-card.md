## Description:

Hearth checks the health of user-configured homelab devices with read-only network, system, service, and application probes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nj070574-gif](https://clawhub.ai/user/nj070574-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Homelab administrators and systems operators use Hearth to check configured devices, spot degraded services or applications, and investigate failed health checks without modifying remote hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Health probes connect to configured hosts and may expose credentials if access is not controlled.

Mitigation: Run only from a bridgehead you control against devices you own; use a dedicated unprivileged SSH key instead of password authentication when possible.

Risk: Disabling SSH host-key verification can expose connections to impersonation.

Mitigation: Keep HEARTH_SSH_STRICT set to accept-new or yes and verify unexpected host-key changes before reconnecting.

Risk: Misconfigured user-defined command probes or repeated sweeps may cause unintended activity on monitored devices.

Mitigation: Review the device inventory and confirm custom probes are read-only before enabling full sweeps, watch mode, or scheduled runs.

## Reference(s):

- [Hearth on ClawHub](https://clawhub.ai/nj070574-gif/skills/hearth)
- [Configuration reference](artifact/docs/CONFIG.md)
- [Probe reference](artifact/docs/PROBES.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or Markdown; optional JSON health report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-device OK, DEGRADED, or DOWN status with reasons and an overall summary; unavailable probes are identified.]

## Skill Version(s):

0.3.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
