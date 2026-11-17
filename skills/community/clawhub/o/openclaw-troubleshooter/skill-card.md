## Description:

OpenClaw troubleshooting and repair guidance for Gateway status, configuration errors, port conflicts, risky skill code, and security misconfigurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[345968504](https://clawhub.ai/user/345968504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose OpenClaw Gateway, Control UI, configuration, port, log, and skill-security issues and to receive prioritized repair commands or configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair flows can force-stop processes.

Mitigation: Use check-only mode first and verify each process name and command line before stopping a PID.

Risk: Configuration repair can overwrite openclaw.json.

Mitigation: Back up openclaw.json and manually review proposed allowedOrigins, trustedProxies, and denyCommands changes before applying them.

Risk: Skill-removal guidance can uninstall skills without sufficient confirmation.

Mitigation: Avoid --yes uninstall or fix-all flows unless the exact target skills have been confirmed.

## Reference(s):

- [Openclaw Troubleshooter on ClawHub](https://clawhub.ai/345968504/skills/openclaw-troubleshooter)
- [Publisher profile](https://clawhub.ai/user/345968504)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic reports with inline PowerShell, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized diagnosis, repair recommendations, check-only guidance, and configuration edits.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
