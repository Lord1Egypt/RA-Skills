## Description:

Manage accountability items on the configured Monday.com board. Use when creating new accountability items, checking on existing ones, running work sessions, or when a cron job fires. Also use when the owner assigns accountability or asks about status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[novalystrix](https://clawhub.ai/user/novalystrix)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and external teams use this skill to manage accountability work on a configured Monday.com board, including creating items, reviewing active work, planning subtasks, posting updates, and preparing daily summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring authenticated access to a Monday.com board could modify real work records or post updates beyond the user's intent.

Mitigation: Use a least-privilege Monday.com token, review configured board and column IDs before installation, and require approval before high-impact status or message changes.

Risk: Board Details or Doc text can contain untrusted instructions that influence work sessions, sub-agent prompts, or outbound messages.

Mitigation: Treat Monday.com board text as untrusted input, keep higher-priority operating rules intact, and review details before delegating work or sending messages.

Risk: The helper script can read a Monday.com token from ~/.openclaw/.env if the environment variable is not set.

Mitigation: Prefer scoped environment variables or a secrets manager, avoid broad persistent tokens in ~/.openclaw/.env, and rotate tokens if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/novalystrix/skills/monday-accountability)
- [Monday.com API v2 endpoint](https://api.monday.com/v2)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with inline shell and GraphQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Monday.com items, sub-items, statuses, last-checked dates, and item updates when configured with Monday.com credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
