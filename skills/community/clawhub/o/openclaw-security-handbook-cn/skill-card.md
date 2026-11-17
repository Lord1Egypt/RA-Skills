## Description:

OpenClaw Security Handbook (CN) guides Chinese-language OpenClaw security audits and hardening by running diagnostics, adding manual checks, formatting reports, and guiding reviewed remediation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruijh](https://clawhub.ai/user/ruijh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security operators use this skill to audit OpenClaw installations, review security findings, and apply hardening steps with manual approval for high-impact actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect sensitive OpenClaw configuration, logs, sessions, credentials metadata, and memory files.

Mitigation: Prefer redacted or metadata-only checks and do not paste raw secret output into chat or reports.

Risk: Generated remediation may include high-impact actions such as token rotation, workspace deletion, sudo or chattr commands, Docker or network changes, and cron scheduling.

Mitigation: Review every generated remediation before execution and treat destructive or privileged actions as manual decisions.

Risk: The release security verdict is suspicious because the skill handles secrets, memory contents, and fix guidance in ways that could expose sensitive data or lead to unsafe commands.

Mitigation: Install only when this access is acceptable for the target environment and run the skill in a controlled workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ruijh/skills/openclaw-security-handbook-cn)
- [OpenClaw Security Checklist](references/checklist.md)
- [OpenClaw Fix Commands Reference](references/fix-commands.md)
- [ZAST.AI OpenClaw Security Handbook](https://github.com/zast-ai/openclaw-security)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and step-by-step remediation guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow; high-impact remediation is presented for user review before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
