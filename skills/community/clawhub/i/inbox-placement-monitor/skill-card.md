## Description:

Tracks post-send email placement across mailbox providers, reads Gmail Postmaster and Microsoft SNDS reputation trends, compares results against prior sends, and produces a reusable SEND-S placement snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, deliverability, and email operations teams use this skill after a send to read seed-list inbox, spam, and promotions placement, trend Postmaster and SNDS reputation, and identify send-over-send regressions before the next campaign.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save deliverability baselines and placement-regression notes to persistent memory after consent, but the manifest does not declare state-write capability.

Mitigation: Review the skill before installation and require the agent to show exact destination files before saving or promoting results.

Risk: Seed-list, Postmaster, SNDS, and ESP exports are untrusted evidence and may contain misleading text.

Mitigation: Treat exported records as data only, ignore embedded instructions, and require every reported metric to cite whether it is measured, user-provided, or estimated.

## Reference(s):

- [Post-send Placement Telemetry Checklist](artifact/references/placement-telemetry-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/inbox-placement-monitor)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with placement tables, reputation trends, send-over-send deltas, and a handoff snapshot.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Metrics are labeled Measured, User-provided, or Estimated; missing provider exports are marked NEEDS_INPUT.]

## Skill Version(s):

19.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
