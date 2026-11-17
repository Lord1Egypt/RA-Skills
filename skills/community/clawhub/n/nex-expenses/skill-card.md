## Description:

Nex Expenses helps agents track business expenses, scan receipts with local Tesseract OCR, categorize Belgian tax deductions, summarize VAT, and export accounting records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

External freelancers, sole traders, and small businesses in Belgium use this skill to capture receipts and expenses, calculate deductible amounts and VAT summaries, and prepare CSV or JSON exports for an accountant.

### Deployment Geography for Use:

Belgium

## Known Risks and Mitigations:

Risk: Receipt images, OCR text, expense records, and exports can contain sensitive accounting or personal data stored under ~/.nex-expenses.

Mitigation: Protect the local data directory, limit access to the machine account, and periodically delete receipts or exports that no longer need to be retained.

Risk: Belgian tax categories, deduction percentages, and VAT summaries may not fit every business circumstance.

Mitigation: Review generated categories and quarterly summaries with an accountant before using them for filings.

Risk: CSV exports can expose sensitive data and may need sanitization before being opened in spreadsheet tools or shared externally.

Mitigation: Inspect and sanitize CSV exports before sharing them or opening them in spreadsheet software.

Risk: The setup flow installs Python dependencies and creates local CLI files.

Mitigation: Review setup.sh and dependency installation behavior before running it in a production or sensitive environment.

## Reference(s):

- [Nex AI homepage](https://nex-ai.be)
- [Tesseract OCR installation reference](https://github.com/UB-Mannheim/tesseract/wiki)
- [ClawHub skill page](https://clawhub.ai/nexaiguy/skills/nex-expenses)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Plain text guidance with shell commands; generated exports may be CSV or JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally and stores the SQLite database, receipt images, configuration, and exports under ~/.nex-expenses by default.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, README changelog 2026-04-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
