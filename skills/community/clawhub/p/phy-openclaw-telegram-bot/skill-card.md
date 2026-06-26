## Description: <br>
Build and deploy production OpenClaw Telegram bots, covering media delivery, allowed directories, agent behavior, Docker deployment, layered security, and common deployment gotchas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, debug, harden, and deploy OpenClaw-based Telegram bots, especially bots that deliver generated media and run in Docker or systemd environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes root-level, Docker socket, and production deployment operations that can affect the host environment. <br>
Mitigation: Review before installing or following in production; use a dedicated host or VM, avoid mounting the Docker socket on shared infrastructure, and prefer an unprivileged service user where possible. <br>
Risk: The skill discusses copying auth-profiles.json and relying on file permissions for secrets, which may not protect against exec-capable processes running as the same user or root. <br>
Mitigation: Verify auth-profiles.json does not contain reusable secrets before copying it, minimize exposed environment secrets, and do not rely on chmod 600 alone for isolation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-openclaw-telegram-bot) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell, JSON, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment checklists, security guidance, troubleshooting steps, and configuration examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
