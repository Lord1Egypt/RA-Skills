## Description:

Monitors token consumption for OpenAI and other models, with daily and weekly bill reports and threshold alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-lucky](https://clawhub.ai/user/mr-lucky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Token Tracker to monitor model token usage, estimate cost, and receive daily or weekly usage reports and threshold alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional hook can run automatically with access to session-compaction events, session status files, and usage records.

Mitigation: Review the hook before installation and enable it only when persistent token logging is required.

Risk: Scheduled reports may announce usage summaries through Telegram, including session IDs, model usage, cost summaries, or event context.

Mitigation: Review scheduled report settings and delivery channels before enabling external announcements.

Risk: The security guidance says the hook logs full context and should validate session keys before production use.

Mitigation: Remove full-context logging and add session-key validation before using the hook in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mr-lucky/skills/my-token-tracker)
- [Publisher profile](https://clawhub.ai/user/mr-lucky)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Plain text and Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include token totals, cost estimates, threshold status, and scheduled report or alert messages.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
