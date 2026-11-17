## Description:

Install a complete proactive outreach system — idle detection, randomized dice delivery, topic-driven crawler, share queue, and persona-based messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leslie311](https://clawhub.ai/user/leslie311)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to install an OpenClaw-based proactive outreach system that detects idle periods, queues interesting content, and sends occasional persona-aware messages. It is intended for users who intentionally want autonomous background outreach from their agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent background jobs that can proactively send messages while the user is idle.

Mitigation: Install only when autonomous outreach is intended, use a Telegram target you control, set quiet hours and daily caps, and audit the installed OpenClaw cron jobs after setup.

Risk: The installer has an unsafe pattern that should be reviewed before execution.

Mitigation: Review or patch install.sh before running it, and prefer --dry-run or --no-cron before enabling scheduled jobs.

Risk: Optional external heartbeat URLs may disclose monitoring events to a third-party service.

Mitigation: Leave external heartbeat URLs unset unless remote monitoring is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leslie311/skills/idle-ping)
- [OpenClaw](https://openclaw.ai)
- [README.md](README.md)
- [LICENSE](LICENSE)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installer guidance, cron job prompts, shell commands, configuration templates, and proactive outbound message text.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
