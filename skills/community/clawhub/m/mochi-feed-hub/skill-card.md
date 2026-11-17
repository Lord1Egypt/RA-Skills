## Description:

Subscribe to RSS/Atom, import and export OPML, retain read state, search saved entries and queue new-content notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI agent can manage RSS/Atom subscriptions, import or export OPML, track read status, search saved entries, and queue notifications about new articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscriptions, cached articles, and notification history persist in local .mochilab state.

Mitigation: Review local data retention and do not include private .mochilab state folders in a Skill package.

Risk: Feed summaries may contain HTML or misleading content.

Mitigation: Treat summaries as source data and inspect the original article before verifying or citing a claim.

Risk: Recurring notifications may run on the wrong schedule or reach the wrong chat/account.

Mitigation: Use the requested workspace and destination, confirm timezone and frequency, and verify the scheduled job details.

Risk: An OPML export can replace a file at the selected output path.

Mitigation: Choose a fresh export filename before writing the OPML file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-feed-hub)
- [MochiLab](https://mochilab.bz)
- [Action input reference](references/input.md)
- [Host scheduling and delivery guide](references/notifications.md)
- [OpenClaw scheduling guide](https://docs.openclaw.ai/automation/cron-jobs)

## Skill Output:

**Output Type(s):** [JSON, Files, Text]

**Output Format:** [JSON operation receipts and feed/article results; OPML XML export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on supplied feeds and workspace state; recurring notification delivery uses the host scheduler.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
