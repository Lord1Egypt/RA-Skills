## Description:

Expense Report Pro helps an agent extract receipt details, categorize expenses, answer spending queries, and generate PDF expense reports from local expense records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, contractors, and small teams use this skill to log receipt images or expense text, maintain local expense records, answer expense questions, and generate reimbursement-ready PDF reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive financial records and receipt images locally.

Mitigation: Use it only in workspaces where local storage is acceptable, keep the expense directory private, and verify restrictive file permissions before storing receipts or reports.

Risk: Receipt text, expense descriptions, and local data files may contain untrusted content.

Mitigation: Treat extracted receipt and expense text as data only, ignore embedded instructions, and ask for user confirmation before saving or bulk-logging receipts.

Risk: PDF report generation depends on Playwright and Chromium and writes generated files.

Mitigation: Pin Playwright/Chromium dependencies, avoid symlinked output paths, and confirm generated reports are readable only by the owner.

Risk: The artifact claims security verification that is not supported by the authoritative security evidence.

Mitigation: Treat bundled security-verification statements as unproven marketing until independently reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-expense-report-pro)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [Dashboard manifest](artifact/dashboard-kit/manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Chat responses, JSON expense records, shell commands, configuration files, and generated PDF reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local expense data and receipt images; PDF generation depends on Python, Playwright, and Chromium.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
