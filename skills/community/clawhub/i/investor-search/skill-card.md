## Description:

Researches investors in a chosen market, checks each claim against sources, and delivers a cited Excel workbook with an honest account of coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chainleo](https://clawhub.ai/user/chainleo)

### License/Terms of Use:

MIT-0

## Use Case:

Fundraising teams, deal sourcers, and investor researchers use this skill to identify and verify family offices, venture capital firms, private equity firms, and angels in a market or enrich an existing prospect list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finished investor workbooks can reach everyone in a shared channel without fresh confirmation.

Mitigation: Use a private delivery channel or confirm that all channel members should receive the workbook before running the skill.

Risk: Retained research files and imported workbooks or ledgers can influence future runs.

Mitigation: Use an appropriately restricted workspace and import only workbooks or ledgers from trusted sources.

## Reference(s):

- [ClawHub investor-search release](https://clawhub.ai/chainleo/skills/investor-search)
- [Environment and retained files](references/environment.md)
- [Investor lists and classifications](references/lists.md)
- [Research and stopping-rule rationale](references/why.md)

## Skill Output:

**Output Type(s):** [Files, Analysis]

**Output Format:** [Cited Excel investor workbook (.xlsx) and a text summary of coverage; working CSV files and a ledger are retained for later runs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source links accompany investor claims; unresolved and rejected candidates are tracked separately.]

## Skill Version(s):

1.2.3 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
