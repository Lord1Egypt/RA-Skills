## Description:

工资审核助手 helps payroll, HR COE, and finance reviewers generate payroll audit checklists, cross-validation summaries, and Markdown or HTML audit reports for domestic and overseas payroll reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Payroll reviewers, HR COE teams, and finance auditors use this skill to prepare monthly payroll audit materials, compare payroll-related CSV sources, identify mismatches or missing approvals, and generate review reports before payroll release.

### Deployment Geography for Use:

Global, with documented domestic and overseas payroll review modes; local payroll, tax, and labor requirements need human validation.

## Known Risks and Mitigations:

Risk: The skill presents payroll auditing as fully automated, which can overstate its reliability for payroll, tax, and compliance decisions.

Mitigation: Use it as a checklist and report assistant; require a qualified human reviewer to confirm data sources, calculations, approvals, and final payroll decisions.

Risk: The artifact describes sending payroll reports to Feishu, which can expose sensitive compensation data if the destination or contents are wrong.

Mitigation: Send reports externally only after a human confirms the destination, recipient permissions, and exact data included.

Risk: Generated HTML reports from untrusted payroll inputs may be unsafe to open or share until output escaping is fixed.

Mitigation: Sanitize or escape payroll input values before HTML generation, keep generated files local, and avoid opening or sharing reports made from untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/payroll-audit)
- [Core payroll audit checks](artifact/rules/core-checks.md)
- [Regional payroll audit rules](artifact/rules/regional-rules.md)
- [Required audit materials list](artifact/rules/materials-list.md)
- [Audit report template](artifact/templates/audit-report.md)
- [Cross-validation script](artifact/scripts/cross_validate.py)
- [HTML report generator](artifact/scripts/generate_html_report.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON or Markdown cross-validation results, HTML reports, shell command examples, and checklist guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local audit files under /tmp and can describe Feishu delivery; sensitive payroll data should be reviewed before sharing.]

## Skill Version(s):

4.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
