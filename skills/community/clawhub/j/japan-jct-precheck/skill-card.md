## Description:

Checks draft Japan consumption-tax filings for common rate, registration, invoice, sales-location, filing-frequency, and record-retention issues, and produces a structured risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowhola](https://clawhub.ai/user/snowhola)

### License/Terms of Use:

MIT-0

## Use Case:

External cross-border sellers use this skill to review draft Japan JCT data and platform statements for common issues and prepare questions for a tax professional. It provides a preliminary pre-check only; it does not file returns or determine compliance.

### Deployment Geography for Use:

Japan

## Known Risks and Mitigations:

Risk: The skill gives an incorrect annual filing deadline for sole proprietors.

Mitigation: Confirm applicable deadlines with the National Tax Agency or a qualified tax professional before relying on the report.

Risk: Draft tax data and platform statements may contain sensitive financial or personal information.

Mitigation: Share only information needed for the pre-check and redact unrelated personal details.

## Reference(s):

- [Japan JCT rule table](artifact/references/rule-table.md)
- [Japan JCT filing deadlines](artifact/references/deadlines.md)
- [National Tax Agency consumption tax guidance](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6601.htm)
- [ClawHub release page](https://clawhub.ai/snowhola/skills/japan-jct-precheck)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Structured Markdown risk report with item-by-item findings and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preliminary guidance based on supplied information; identifies missing details as cannot determine and does not generate or file official returns or registration documents.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
