## Description:

Fetches IT之家 daily, weekly, or monthly ranking articles and formats them for on-demand retrieval or optional delivery to a messaging channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dustink66](https://clawhub.ai/user/dustink66)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to retrieve IT之家 hot article rankings and prepare concise Markdown updates. It can support manual checks or scheduled pushes to a user-selected messaging channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses ithome.com to fetch public ranking pages.

Mitigation: Confirm that external access to ithome.com is allowed before installing or running the skill.

Risk: Optional push and cron usage can send article summaries to the wrong channel, recipient, timezone, or schedule.

Mitigation: Explicitly choose and review the messaging channel, target session, timezone, and recurrence; skip cron setup when only on-demand retrieval is needed.

## Reference(s):

- [IT之家](https://www.ithome.com/)
- [ClawHub skill page](https://clawhub.ai/dustink66/skills/ithome-rank)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with article links and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to ithome.com; optional scheduled delivery depends on the configured channel and recurrence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
