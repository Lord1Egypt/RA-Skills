## Description:

Installs, configures, manages, and troubleshoots the Pixel Agents Dashboard, a real-time pixel art operations dashboard for OpenClaw deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaffer1979](https://clawhub.ai/user/jaffer1979)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up and manage a local dashboard that visualizes OpenClaw agent activity, monitors hardware and services, and supports spawning agent tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard exposes powerful controls and agent conversation data over unauthenticated network services.

Mitigation: Install only in a trusted local environment, bind the service to localhost or place it behind authentication, and avoid exposing port 5070 to a network.

Risk: Remote administration features may rely on SSH access and sensitive credentials.

Mitigation: Prefer SSH keys over passwords and keep secrets in environment variables or protected local configuration.

Risk: Dependency risk may affect real deployments.

Mitigation: Update vulnerable dependencies before relying on the dashboard for production or operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaffer1979/skills/openclaw-pixel-agents-dashboard)
- [OpenClaw](https://openclaw.ai)
- [Artifact README](artifact/README.md)
- [Example dashboard configuration](artifact/dashboard.config.example.json)
- [Asset license](artifact/public/assets/ASSET-LICENSE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local dashboard configuration files and provide service-management commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
