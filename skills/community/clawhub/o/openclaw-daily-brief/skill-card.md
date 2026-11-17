## Description:

Send a daily operational brief from your self-hosted OpenClaw to Telegram — agent health, unresolved issues, and weekly evolution highlights, every morning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baobaodawang-creater](https://clawhub.ai/user/baobaodawang-creater)

### License/Terms of Use:

MIT-0

## Use Case:

Self-hosted OpenClaw users use this skill to collect recent gateway and capability-evolver signals, summarize them with a configured secretary agent, and send a concise daily operations brief to Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily operational summaries may send private OpenClaw activity, logs, or unresolved issue details to Telegram.

Mitigation: Use a restricted Telegram bot and chat, redact tokens and private data, and avoid logging secrets.

Risk: A recurring cron job can automatically send generated reports before a user reviews them.

Mitigation: Validate the generated report before enabling unattended delivery, especially when first deploying or changing the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baobaodawang-creater/skills/openclaw-daily-brief)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and cron examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a recurring Telegram-ready operational summary from local OpenClaw logs and evolver output.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
