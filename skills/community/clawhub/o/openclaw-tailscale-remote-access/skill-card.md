## Description:

Configure or repair OpenClaw remote access over Tailscale with a directly executable workflow: inspect state, apply the gateway config, enable Tailscale Serve over HTTPS, validate browser access, and handle origin, DNS, or pairing failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangagentlabs](https://clawhub.ai/user/jiangagentlabs)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to make an OpenClaw gateway reachable through Tailscale Serve over HTTPS and to repair common remote-access failures involving origin checks, DNS, TLS, service state, and device pairing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes OpenClaw and Tailscale state on a remote-access host.

Mitigation: Use it only on hosts where those changes are acceptable, keep an out-of-band admin path available, and avoid running Tailscale state changes from a Tailscale SSH session.

Risk: The workflow handles gateway credentials and diagnostic data, including config contents and pairing files.

Mitigation: Redact tokens and pairing data before sharing output, and check permissions on openclaw.json and generated backup files after running the workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiangagentlabs/skills/openclaw-tailscale-remote-access)
- [Server-Resolved Homepage](https://github.com/JiangAgentLabs/openclaw-tailscale-remote-access)
- [Remote Setup](references/remote-setup.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires host-specific values for the OpenClaw config path, Tailscale MagicDNS hostname, gateway token, and gateway port.]

## Skill Version(s):

1.0.1 (source: server release metadata, SKILL.md metadata.openclaw.version, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
