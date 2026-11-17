## Description:

Guides an agent through a TeslaMate deployment workflow for local or remote Debian/Ubuntu hosts, including target selection, pre-flight checks, deployment script execution, health checks, and a usage document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinbj2008](https://clawhub.ai/user/martinbj2008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to perform a fresh TeslaMate installation on an existing local or remote Debian/Ubuntu host. It helps verify prerequisites, run the deployment flow, check service health, and produce user-facing access and operations notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests privileged deployment authority for services that handle sensitive Tesla telemetry.

Mitigation: Use it only on a trusted host and network, and review the deployment steps before execution.

Risk: Release evidence reports missing scripts and loosely scoped shell or SSH commands.

Mitigation: Verify the expected deployment scripts are present and inspect them before running any local or remote command.

Risk: Release evidence flags weak/default secrets and exposed services.

Mitigation: Generate strong unique secrets before first startup and restrict exposed ports with a firewall or VPN.

Risk: Tesla authentication material may be required during setup.

Mitigation: Do not paste Tesla tokens into chat or terminal commands; enter them only through the intended TeslaMate interface.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/martinbj2008/skills/my-teslamate)
- [Server-Resolved Source Repository](https://github.com/martinbj2008/my_teslamate)
- [TeslaMate Initial Setup Guide](https://docs.teslamate.org/docs/guides/initial_setup)
- [TeslaMate Backup Guide](https://docs.teslamate.org/docs/guides/backup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a deployment usage document and report service access URLs, health-check results, credentials guidance, and troubleshooting steps.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
