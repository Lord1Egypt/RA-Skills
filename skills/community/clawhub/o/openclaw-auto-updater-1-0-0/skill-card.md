## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q262045312-ui](https://clawhub.ai/user/q262045312-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Clawdbot users and developers use this skill to configure scheduled daily updates for Clawdbot and installed skills, then receive a concise summary of version changes and failures after each run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled unattended updates can modify Clawdbot and installed skills without per-update approval or pinned versions.

Mitigation: Prefer a dry-run or notify-first setup, pin or approve specific updates where possible, and verify how to inspect and remove the cron job before enabling it.

Risk: Automatic update failures or partial updates can leave Clawdbot and installed skills on different versions.

Mitigation: Review the delivered update summary, inspect logs for failures, and run manual update or doctor commands before relying on the environment.

## Reference(s):

- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure recurring scheduled updates and produce daily update summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
