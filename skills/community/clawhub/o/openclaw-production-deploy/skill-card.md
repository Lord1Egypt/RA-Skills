## Description:

Provides guidance and scripts for deploying the OpenClaw chat interface locally and in production, including service registration, startup configuration, monitoring, performance tuning, backup, and recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ynxiyan](https://clawhub.ai/user/ynxiyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure an OpenClaw chat interface for local or production use across Windows, Linux, and macOS. It helps set up system services, startup behavior, monitoring, troubleshooting, backup, and recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package combines persistent service setup with scripts that the security evidence describes as unsafe or incomplete.

Mitigation: Review and repair the package before installing, and replace the systemd installer with a dedicated gateway service that does not rerun the deployment script.

Risk: The deployment guidance can expose the web UI broadly on the network.

Mitigation: Default the web UI to localhost unless TLS and firewall allowlists are configured.

Risk: OpenClaw installation steps may use unpinned versions or default-branch code.

Mitigation: Pin exact OpenClaw versions and avoid running unreviewed latest or default-branch code.

Risk: Production token files may be created or referenced during setup.

Mitigation: Protect token files with restrictive permissions and review token handling before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ynxiyan/skills/openclaw-production-deploy)
- [Production Setup Guide](artifact/docs/PRODUCTION-SETUP.md)
- [Bilibili OpenClaw Chat Interface Tutorial](https://www.bilibili.com/video/BV1VkQBBfEcd)
- [OpenClaw Deployment Guide](https://docs.openclaw.ai/deployment)
- [OpenClaw Production Deployment](https://docs.openclaw.ai/deployment/production)
- [OpenClaw Performance Documentation](https://docs.openclaw.ai/performance)
- [OpenClaw Security Guide](https://docs.openclaw.ai/security)
- [OpenClaw GitHub Discussions](https://github.com/openclaw/openclaw/discussions)
- [OpenClaw Issue Tracker](https://github.com/openclaw/openclaw/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, configuration snippets, and JavaScript deployment scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes production deployment guidance, environment checks, service setup commands, monitoring guidance, backup and recovery steps, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
