## Description:

Hook Guard adds a three-level safety layer for AI agents by requiring confirmation for dangerous actions, backing up important edits, and recording routine activity in an audit log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Hook Guard to add operation-level safeguards around agent file edits, command execution, external messaging, backups, and audit reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic backups may retain plaintext copies of sensitive files such as .env, private keys, token stores, and production configs.

Mitigation: Exclude secret-bearing files from automatic backup and restrict backup file permissions before enabling the skill broadly.

Risk: Audit logs can record broad agent activity metadata and may be reused across sessions.

Mitigation: Keep logs limited to operation metadata, restrict log permissions, and require explicit opt-in before cross-session audit reuse.

## Reference(s):

- [Hook Guard ClawHub release](https://clawhub.ai/wavmson/skills/hook-guard)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces confirmation prompts, backup notices, audit summaries, and AGENTS.md-style guard rules.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
