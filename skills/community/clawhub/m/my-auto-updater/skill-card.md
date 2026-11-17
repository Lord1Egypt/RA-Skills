## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockyzhuo](https://clawhub.ai/user/rockyzhuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to configure a scheduled update routine that keeps Clawdbot and installed skills current and reports changes or failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily automatic updates can change Clawdbot and every installed skill without review.

Mitigation: Prefer a check-only or approval-before-apply workflow, pin trusted versions or publishers, keep rollback steps, and review any command before using elevated privileges.

Risk: Update failures can leave partial updates or require manual intervention.

Mitigation: Report partial successes and failures clearly, check versions after runs, and use dry-run or list commands before applying broad updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rockyzhuo/skills/my-auto-updater)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)
- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure a daily cron-driven update routine and produce concise update summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact _meta.json, and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
