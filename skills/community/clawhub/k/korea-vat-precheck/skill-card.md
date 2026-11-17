## Description:

Reviews Korean VAT draft filing data and marketplace statements for common cross-border seller issues and produces a structured pre-check risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowhola](https://clawhub.ai/user/snowhola)

### License/Terms of Use:

MIT-0

## Use Case:

Cross-border sellers use this skill to review Korean VAT information and platform statements for common filing, import, registration, and receipt issues. It provides a preliminary risk report only; it does not determine compliance, file returns, or register a business.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: The filing-calendar guidance may contain incorrect timing information.

Mitigation: Confirm applicable deadlines with official NTS filing guidance and a Korean tax advisor before acting.

Risk: Sales materials may contain customer identifiers, PCCC values, or credentials that are not needed for a pre-check.

Mitigation: Use redacted sales summaries and omit customer identifiers, actual PCCC values, and credentials.

Risk: A favorable pre-check could be mistaken for a compliance determination or filing service.

Mitigation: Treat the report as preliminary only; have a Korean tax advisor review it and handle filing or registration.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/snowhola/skills/korea-vat-precheck)
- [Korea VAT rule table](artifact/references/rule-table.md)
- [Korea VAT deadlines](artifact/references/deadlines.md)
- [Official NTS filing guidance](https://www.nts.go.kr/english/cm/cntnts/cntntsView.do?cntntsId=238886&mi=40008)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Structured Markdown risk summary, findings table, and prioritized next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pre-check only; does not generate official returns or registration documents.]

## Skill Version(s):

0.1.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
