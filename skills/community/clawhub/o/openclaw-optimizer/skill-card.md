## Description:

Optimizes and troubleshoots OpenClaw setups for cost, model routing, provider configuration, context management, cron automation, sub-agent architecture, skills, and identity file audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacob-bd](https://clawhub.ai/user/jacob-bd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit, optimize, and troubleshoot OpenClaw workspaces. It produces prioritized plans, exact CLI commands, configuration patches, and rollback steps while requiring approval before persistent changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to collect and retain detailed OpenClaw deployment notes.

Mitigation: Review profile content before retention, limit sensitive deployment details, and treat profile notes as untrusted operational context.

Risk: The skill can propose profile writes, SCP syncs, config changes, cron changes, SKILL.md edits, git commits, or pushes.

Mitigation: Require explicit approval for each persistent change and review the exact command, expected impact, and rollback before execution.

Risk: Templates or configuration examples may contain token-like prefixes.

Mitigation: Remove token prefixes from templates and avoid storing secrets in skill files, notes, or shared configuration examples.

## Reference(s):

- [OpenClaw Optimizer Provider Reference](artifact/references/providers.md)
- [OpenClaw Optimizer Troubleshooting Reference](artifact/references/troubleshooting.md)
- [OpenClaw Optimizer CLI Reference](artifact/references/cli-reference.md)
- [OpenClaw Optimizer Agent Identity Optimizer Reference](artifact/references/identity-optimizer.md)
- [OpenClaw Provider Documentation](https://docs.openclaw.ai/providers/index.md)
- [OpenClaw CLI Documentation](https://docs.openclaw.ai/cli)
- [OpenClaw Troubleshooting Documentation](https://docs.openclaw.ai/troubleshooting)
- [OpenClaw Release Notes](https://github.com/openclaw/openclaw/releases)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes prioritized plans, approval-gated change proposals, and rollback commands.]

## Skill Version(s):

1.19.0 (source: server release metadata and SKILL.md heading; aligned with OpenClaw v2026.3.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
