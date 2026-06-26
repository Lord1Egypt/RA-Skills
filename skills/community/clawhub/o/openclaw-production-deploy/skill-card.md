## Description: <br>
Provides OpenClaw local and production deployment guidance, including service registration, autostart configuration, monitoring, performance tuning, backup, and recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ynxiyan](https://clawhub.ai/user/ynxiyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan and execute an OpenClaw production deployment with environment checks, service setup, monitoring, backup, and troubleshooting steps. It is intended for teams that need repeatable local or server deployment instructions rather than an interactive application runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment helper can make persistent privileged system changes such as service registration, autostart configuration, and systemd or launchd setup. <br>
Mitigation: Review commands before execution, test in an isolated environment first, and run production changes only under normal change-control procedures. <br>
Risk: The security review notes unsafe, under-scoped deployment behavior and a service entrypoint that should be verified before use. <br>
Mitigation: Verify and fix the service entrypoint, confirm generated service files, and validate the resulting OpenClaw process before enabling automatic restart. <br>
Risk: The artifact handles sensitive credentials and exposes services on network interfaces when configured for production access. <br>
Mitigation: Keep authentication enabled, use a strong token, prefer HTTPS for remote access, and avoid disabling authentication outside isolated tests. <br>
Risk: The artifact may use unpinned OpenClaw, npm, Git, or registry behavior during installation. <br>
Mitigation: Use pinned OpenClaw, npm, and Git versions, avoid persistent npm registry changes, and record installed versions for rollback. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ynxiyan/openclaw-production-deploy) <br>
- [OpenClaw deployment guide](https://docs.openclaw.ai/deployment) <br>
- [OpenClaw production deployment](https://docs.openclaw.ai/deployment/production) <br>
- [OpenClaw performance guide](https://docs.openclaw.ai/performance) <br>
- [OpenClaw security guide](https://docs.openclaw.ai/security) <br>
- [OpenClaw GitHub discussions](https://github.com/openclaw/openclaw/discussions) <br>
- [Bilibili tutorial referenced by artifact](https://www.bilibili.com/video/BV1VkQBBfEcd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment steps, generated service configuration, monitoring commands, backup guidance, and troubleshooting instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
