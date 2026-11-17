## Description:

Unified security suite for agent workspaces. Installs, configures, and orchestrates all 11 OpenClaw security tools in one command -- integrity, secrets, permissions, network, audit trail, signing, supply chain, credentials, injection defense, compliance, and incident response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and security engineers use this skill to install, initialize, update, scan, and monitor a workspace with the OpenClaw security tool suite from a single orchestrator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can bulk install, update, and execute many dependent security skills.

Mitigation: Review or pin the 11 dependent skills before installation or update, and run commands only in workspaces where those tools are trusted.

Risk: The protect command can trigger state-changing remediation through dependent Pro tools.

Mitigation: Run scan or status first, review findings, and execute protect only with explicit operator approval.

Risk: Unattended update or protect runs may apply changes without sufficient review.

Mitigation: Avoid unattended update and protect runs; capture command output and review each dependent tool's result.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atlaspa/skills/openclaw-security)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [openclaw-warden](https://github.com/AtlasPA/openclaw-warden)
- [openclaw-sentry](https://github.com/AtlasPA/openclaw-sentry)
- [openclaw-arbiter](https://github.com/AtlasPA/openclaw-arbiter)
- [openclaw-signet](https://github.com/AtlasPA/openclaw-signet)
- [openclaw-ledger](https://github.com/AtlasPA/openclaw-ledger)
- [openclaw-egress](https://github.com/AtlasPA/openclaw-egress)
- [openclaw-sentinel](https://github.com/AtlasPA/openclaw-sentinel)
- [openclaw-vault](https://github.com/AtlasPA/openclaw-vault)
- [openclaw-bastion](https://github.com/AtlasPA/openclaw-bastion)
- [openclaw-marshal](https://github.com/AtlasPA/openclaw-marshal)
- [openclaw-triage](https://github.com/AtlasPA/openclaw-triage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3. Install and update commands require the ClawHub CLI. The protect command can execute state-changing countermeasures through dependent skills.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
