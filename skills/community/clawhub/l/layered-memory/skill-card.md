## Description:

Layered Memory helps OpenClaw users manage large local memory files through L0/L1/L2 summaries so agents can search, read, and maintain memory with lower token use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingdadaa](https://clawhub.ai/user/yingdadaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate, maintain, read, and search layered memory files for long-running agent work while reducing token consumption. The OpenClaw hook can remind agents about memory-saving thresholds during session bootstrap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OpenClaw hook can affect agent startup behavior by injecting memory-management reminders.

Mitigation: Review hooks/openclaw/handler.js before enabling the hook and enable it only in workspaces where memory reminders are desired.

Risk: The skill can persist conversation-derived notes in local memory files, which may include sensitive chat content.

Mitigation: Avoid unattended auto-save for sensitive conversations, review saved memory files, and use manual save or dry-run workflows when content sensitivity is uncertain.

Risk: Several CLI paths invoke helper scripts under ~/clawd/scripts that are not bundled in the artifact.

Mitigation: Verify or bundle the required helper scripts before running the CLI, and run the skill only in a trusted local environment.

Risk: Scheduled OpenClaw or cron-style checks can repeatedly inspect active sessions.

Mitigation: Install scheduled jobs only when recurring session checks are acceptable, and tune thresholds, cooldowns, or disable scheduling when not needed.

## Reference(s):

- [README](README.md)
- [Integration Guide](INTEGRATION.md)
- [Auto Trigger Guide](AUTO-TRIGGER.md)
- [Auto Save Guide](AUTO-SAVE-GUIDE.md)
- [Anti-Duplicate Design](ANTI-DUPLICATE.md)
- [Configuration Example](config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, plain-text CLI output, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates L0 abstract and L1 overview files from L2 memory content; can also return read, search, stats, maintenance, archive, summary, and dedupe command output.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence, package.json, CHANGELOG, released 2026-03-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
