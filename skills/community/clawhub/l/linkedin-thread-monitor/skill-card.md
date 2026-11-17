## Description:

Track which of your LinkedIn comments earned author replies, classify thread timing, and route warm threads to follow-up draft assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to monitor recent LinkedIn comment threads, identify author replies during the highest-value follow-up window, and prepare public replies or thread-specific DMs for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an Apify token to retrieve recent LinkedIn thread data.

Mitigation: Install only when that token use and data retrieval are acceptable for the account and workflow.

Risk: Suggested replies, DMs, and growth tactics may be inappropriate for the user's voice, outreach standards, or LinkedIn rules.

Mitigation: Review every suggested reply, DM, and tactic manually before posting or sending.

Risk: Coordinated engagement or outreach patterns can violate platform rules or create reputational risk.

Mitigation: Avoid coordinated engagement, generic outreach, and any action that conflicts with LinkedIn rules or the user's outreach standards.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sergebulaev/skills/linkedin-thread-monitor)
- [Output specification](artifact/references/output-spec.md)
- [Thread timing matrix](artifact/references/thread-timing.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables, thread previews, suggested replies, DM drafts, and weekly roll-up summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use an Apify token to retrieve recent LinkedIn thread data; without a token, it falls back to user-provided recent comment URLs.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
