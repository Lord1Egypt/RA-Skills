## Description:

墨记 (moji-daily) helps an agent manage daily tasks through Chinese-language chat, scheduled reviews, local Markdown task files, and rollover of unfinished items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afeicn](https://clawhub.ai/user/afeicn)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to track daily work in Chinese-language chat, with morning planning, midday progress checks, evening summaries, and local Markdown task records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional cron snippets send scheduled prompts to a Feishu channel.

Mitigation: Confirm the intended Feishu channel before enabling the cron configuration.

Risk: Casual task-management phrases may update local Markdown task files.

Mitigation: Review task changes when reporting additions, cancellations, completions, or rollovers in chat.

## Reference(s):

- [Detailed Workflow](references/workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/afeicn/skills/moji-daily)
- [Publisher Profile](https://clawhub.ai/user/afeicn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese-language chat responses, Markdown task files, and cron configuration JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores task records locally in tasks/YYYY-MM-DD.md and can emit optional cron setup configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
