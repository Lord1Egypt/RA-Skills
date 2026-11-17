## Description:

One-command bootstrap for new OpenClaw installations. Sets up workspace files, self-evolution system (.learnings + hooks + crons), and community skills. Use when setting up a fresh OpenClaw or replicating setup to another machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djangozh](https://clawhub.ai/user/djangozh)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to initialize a new OpenClaw workspace or replicate an existing setup to another machine. It creates workspace memory files, learning logs, hooks, scheduled reviews, and community skill setup commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent memory, hooks, and scheduled review workflows in an OpenClaw workspace.

Mitigation: Install only when persistent workspace automation is intended; inspect generated files, review the self-improving-agent hook before enabling it, and disable cron jobs that are not desired.

Risk: The setup may install unpinned remote packages and community skills.

Mitigation: Pin and verify dependencies and community skill versions before running the bootstrap in a trusted workspace.

Risk: Automatic promotion into AGENTS.md or MEMORY.md could preserve incorrect or unwanted guidance.

Mitigation: Require human review before promoting learning entries or memory updates into long-lived workspace files.

## Reference(s):

- [Architecture](artifact/references/architecture.md)
- [OpenClaw Bootstrap ClawHub listing](https://clawhub.ai/djangozh/skills/openclaw-bootstrap)
- [djangozh ClawHub profile](https://clawhub.ai/user/djangozh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance and files for an OpenClaw workspace; shell commands may install packages, enable hooks, and add scheduled jobs.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
