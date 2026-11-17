## Description:

Middle East VAT pre-check for cross-border sellers (Amazon.ae, Noon), reviewing rates, registration obligations, platform and stock models, invoicing, filing frequency, currency, and pricing to produce a structured risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowhola](https://clawhub.ai/user/snowhola)

### License/Terms of Use:

MIT-0

## Use Case:

External cross-border sellers use this skill to screen draft UAE and Saudi VAT information and platform statements for common issues before consulting a tax professional. It provides pre-checks only and does not file returns or register businesses.

### Deployment Geography for Use:

United Arab Emirates and Saudi Arabia; the references also mention Bahrain, Oman, Kuwait, and Qatar as regional context.

## Known Risks and Mitigations:

Risk: Users may treat a preliminary VAT screening as confirmation of compliance or rely on simplified rules and deadlines without checking current applicability.

Mitigation: Treat the report as preliminary and confirm applicable rules and deadlines with a local tax professional and the relevant tax authority before acting.

Risk: Draft filings or platform statements may include unnecessary personal or account details.

Mitigation: Share only the business information needed for the pre-check and redact unnecessary personal or account details.

Risk: Registration and back-filing decisions may require local expertise, including a KSA tax representative where applicable.

Mitigation: Hand registration or back-filing questions to a local tax agent and, where applicable, a KSA tax representative; this skill does not file or register.

## Reference(s):

- [Filing deadlines](artifact/references/deadlines.md)
- [VAT rule table](artifact/references/rule-table.md)
- [ClawHub skill page](https://clawhub.ai/snowhola/skills/middle-east-vat-precheck)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Structured Markdown risk report with a risk summary, findings table, and prioritized next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pre-check only; not a compliance conclusion, official return, or registration document. Missing information and rules marked for verification are identified rather than guessed.]

## Skill Version(s):

0.1.0 (source: frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
