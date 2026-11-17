## Description:

Multi-Source Cleaner parses messy spreadsheet, CSV, TSV, JSON, and pasted text inputs, identifies common business fields, cleans and merges records, and exports cleaned datasets with quality reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yk-global-01](https://clawhub.ai/user/yk-global-01)

### License/Terms of Use:

MIT-0

## Use Case:

Business operations, ecommerce, finance, CRM, and support teams use this skill to normalize, deduplicate, fill, classify, and merge multi-source tabular data before sharing or analysis. Agents can call it through Python functions or CLI commands to produce cleaned files and optional quality reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive records or API keys may be transferred to external AI, license-verification, or Feishu services when optional features are enabled.

Mitigation: Use local-only cleaning paths for sensitive datasets, disable AI classification and Feishu export unless users explicitly approve those transfers, and keep provider credentials separate.

Risk: The artifact documentation contains unclear disclosure about external transfers.

Mitigation: Review the security summary before installation and communicate which optional features contact external services before processing personal, financial, customer, banking, or identity data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yk-global-01/skills/multi-source-cleaner)
- [MiniMax platform](https://platform.minimax.chat/)
- [DeepSeek platform](https://platform.deepseek.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; generated runtime artifacts can include XLSX, CSV, Markdown reports, dictionaries, and Feishu document or Bitable links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on tier and selected options; AI-assisted classification and Feishu export require explicit credentials and supported integrations.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
