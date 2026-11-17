## Description:

Tracks AI API token usage, call counts, response duration, and estimated USD costs for configured models such as MiniMax and OpenAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record LLM token consumption, estimate model costs, review daily or aggregate usage reports, and reset local cost history when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cost reports may be inaccurate if pricing data is stale, default pricing is used, or the hard-coded pricing path does not match the installed location.

Mitigation: Review and update config/pricing.json and installation paths before relying on totals for budgeting or audit decisions.

Risk: Malformed or negative usage inputs can corrupt accumulated totals.

Mitigation: Validate token and duration inputs at integration points and inspect reports for anomalies before using the data operationally.

Risk: Resetting statistics changes persistent local cost history, even though a backup is written.

Mitigation: Restrict reset use to trusted operators and retain backup files when cost history is needed for review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/huo15-cost-tracker)
- [Publisher profile](https://clawhub.ai/user/jobzhao15)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown and terminal text with shell command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local cost statistics as JSON and prints cost reports in the terminal.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
