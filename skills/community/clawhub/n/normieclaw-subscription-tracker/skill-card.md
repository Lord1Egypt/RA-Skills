## Description:

Tracks recurring charges from user-provided bank and credit-card statements, alerts on renewals, duplicates, price increases, and trials, and helps users export or cancel subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill with an OpenClaw agent to identify and manage recurring subscription charges from manually provided CSV or PDF statements without bank linking. It supports renewal reminders, duplicate and overlap review, price-change detection, free-trial tracking, cancellation guidance, and exports for reporting or Budget Buddy Pro.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive bank and credit-card statement data, and statement contents may be sent to the user's model provider during agent processing.

Mitigation: Use only in a trusted agent environment, redact statements where practical, review the model provider's data terms, and delete local statement archives when they are no longer needed.

Risk: CSV, Markdown, and JSON exports contain subscription and spending data that can reveal financial habits.

Mitigation: Store exports deliberately, restrict file permissions, avoid sharing them through unsecured channels, and delete obsolete exports.

Risk: Custom export paths can replace unintended user files if misused.

Mitigation: Prefer the default export directory unless the destination path has been reviewed and confirmed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nollio/skills/normieclaw-subscription-tracker)
- [Publisher Profile](https://clawhub.ai/user/nollio)
- [README](README.md)
- [Security](SECURITY.md)
- [Dashboard Spec](dashboard-kit/DASHBOARD-SPEC.md)
- [Dashboard Manifest](dashboard-kit/manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration, guidance]

**Output Format:** [Agent-facing text and Markdown with local shell commands; exports can be CSV, Markdown, or Budget Buddy JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local statement files and subscription records; exported files should be treated as sensitive financial data.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact files mention 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
