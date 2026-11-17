## Description:

Patent Fee Monitor helps agents query patent-fee deadlines, monitor patent legal status, manage patent, trademark, and software copyright ledgers, calculate remaining payment days, import IP assets in batches, and generate reminders for small businesses, inventors, and startup IP management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and IP operations teams use this skill to monitor patent annuity deadlines, estimate fee status, maintain lightweight IP asset ledgers, and generate reminder artifacts. It is suited to non-specialist small-business IPR users, individual inventors, and startup teams that need structured patent, trademark, and software copyright tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent portfolio details, filing strategy, owner names, notes, and reminder dates may be sensitive and can be stored locally by the skill.

Mitigation: Use the skill only with IP asset data that is approved for local storage in the skill directory, and review ledger contents before sharing the workspace or exports.

Risk: Patent lookups may send patent identifiers to public patent services.

Mitigation: Avoid automatic lookups for confidential portfolios and rely on manually supplied ledger dates when lookup disclosure is not acceptable.

Risk: CSV and iCalendar exports may carry sensitive data and the security guidance notes caution until export escaping is fixed.

Mitigation: Open generated CSV and .ics files only in trusted tools, inspect exported content before distribution, and avoid importing unreviewed exports into production calendars or spreadsheets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/golngod/skills/patent-fee-monitor)
- [Google Patents](https://patents.google.com)
- [USPTO ODP API](https://api.uspto.gov)
- [EPO Open Patent Services](https://ops.epo.org)
- [WIPO PATENTSCOPE](https://patentscope.wipo.int)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration]

**Output Format:** [Markdown-style text reports, CSV ledger exports, iCalendar reminder files, JSON-like dictionaries, and user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local CSV and .ics files and may update the local IP asset ledger JSON.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
