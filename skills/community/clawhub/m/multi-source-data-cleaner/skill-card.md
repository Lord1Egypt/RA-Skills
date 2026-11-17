## Description:

Cleans multi-source tabular data by parsing spreadsheets, CSV/TSV, JSON, and pasted text, identifying fields, deduplicating and normalizing records, merging sources, and producing cleaned files or quality reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiji0802](https://clawhub.ai/user/qiji0802)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and developers use this skill to turn messy operational data into cleaned datasets, joined multi-source tables, and data-quality reports for CRM, ecommerce, finance, operations, and customer-support workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports under-disclosed paths that can send spreadsheet data and credentials to external services.

Mitigation: Avoid AI mode, automatic report publishing, and Feishu export for sensitive customer, banking, ID, HR, or regulated records unless external transfer is approved.

Risk: Provider and license credentials may be used by optional AI, token validation, or export paths.

Mitigation: Use separate provider and license credentials, prefer an explicit local-only tier setting, and rotate credentials if unintended external calls occur.

Risk: Exported spreadsheets created from untrusted inputs may preserve values that spreadsheet software interprets as formulas.

Mitigation: Treat generated spreadsheets from untrusted data as potentially formula-injection unsafe and review cells before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiji0802/skills/multi-source-data-cleaner)
- [MiniMax platform](https://platform.minimax.chat/)
- [DeepSeek platform](https://platform.deepseek.com/)

## Skill Output:

**Output Type(s):** [Files, Markdown, Text, Configuration]

**Output Format:** [Excel or CSV files, Markdown quality reports, Feishu Bitable or document links, and Python dictionary results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by tier and configuration; optional AI classification and Feishu export require credentials.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact docs list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
