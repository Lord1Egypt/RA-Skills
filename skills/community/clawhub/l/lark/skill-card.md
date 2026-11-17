## Description:

Deep Lark integration skill. A Digital Command Center powered by a Coordination Diagnosis Engine. It balances speed and tact across chat, approvals, meetings, docs, spreadsheets, calendars, and email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agisearch](https://clawhub.ai/user/agisearch)

### License/Terms of Use:

MIT-0

## Use Case:

Managers, project owners, cross-functional operators, and teams using Lark use this skill to turn chat, approvals, meetings, documents, spreadsheets, calendars, and email into prioritized briefings, drafts, follow-up plans, and controlled routine actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The host Lark connector may access broad workplace collaboration data when credentials are granted.

Mitigation: Use least-privilege Lark app credentials and install only where that connector access is intended.

Risk: Executive Mode may perform authorized routine write actions such as sends, spreadsheet edits, workflow actions, or calendar changes.

Mitigation: Keep Counselor Mode as the default for review-heavy workflows and require explicit confirmation before writes or approval decisions.

Risk: High-sensitivity communications or operational updates can create organizational friction if executed without context.

Mitigation: Require second confirmation for upward messages, public reminders, critical spreadsheet edits, approval decisions, and irreversible calendar changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agisearch/skills/lark)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or structured text briefings, drafts, recommendations, and confirmation-gated action plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires host-provided Lark connector credentials via LARK_APP_ID and LARK_APP_SECRET.]

## Skill Version(s):

2.0.1 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
