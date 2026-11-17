## Description:

Automates OpenClaw VPS setup, security hardening, multi-agent configuration, messaging integrations, and deployment documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harvnk](https://clawhub.ai/user/harvnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up and harden OpenClaw on Ubuntu or Debian VPS hosts, configure multi-agent workspaces, connect messaging platforms, and generate deployment notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firewall, SSH, cron, and backup changes can affect VPS access or availability if applied without a rollback plan.

Mitigation: Keep an existing admin SSH session open, confirm console or recovery access, and back up SSH and firewall configuration before applying changes.

Risk: API keys and messaging bot tokens may be exposed or stored in unsuitable locations during setup.

Mitigation: Verify where credentials will be stored before use and limit access to the deployment user and required services.

## Reference(s):

- [OpenClaw Setup Assistant on ClawHub](https://clawhub.ai/harvnk/skills/openclaw-setup-assistant)
- [Harvnk Publisher Profile](https://clawhub.ai/user/harvnk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup-specific deployment documentation, security checklists, health checks, backup steps, and messaging integration instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
