## Description:

Use when Codex, Hermes, OpenClaw, Claude Code, Cowork, or another AI agent needs to plan, review, implement, audit, or improve email work focused on open, inspectable email campaign operations for agents that need clear audit trails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to plan, audit, migrate, QA, and safely execute email campaign operations with clear audit trails and approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email exports, contact lists, suppression files, logs, DNS settings, and live sends may contain sensitive or operationally risky data.

Mitigation: Use the skill for audit-style campaign operations, limit access to necessary artifacts, and require explicit human approval before any production email-system change.

Risk: High-risk email operations such as live sends, contact imports, suppression edits, DNS/authentication changes, provider migrations, and destructive cleanup can affect recipients or production systems.

Mitigation: Keep these actions behind explicit approval gates and include rollback or restore notes before execution.

## Reference(s):

- [OpenClaw Email Skill Operating Checklist](references/operating-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/polnikale/skills/openclawemailskill)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance, playbooks, checklists, review packets, and runbooks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit approval before live sends, contact imports, DNS/authentication changes, suppression edits, production automation changes, or destructive cleanup.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
