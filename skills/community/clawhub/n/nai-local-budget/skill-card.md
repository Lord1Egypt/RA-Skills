## Description:

Analyze exported bank and credit card CSV files locally to track spending, categorize transactions, compare against budgets, and generate Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process personal bank or card CSV exports locally, review transaction categories, and generate budget comparison reports for private finance tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bank and card CSV exports, categorized transactions, and generated reports can contain sensitive personal finance data.

Mitigation: Process files in a private local folder, keep outputs out of synced or shared vaults unless intended, and delete intermediate JSON files when no longer needed.

Risk: Generated Markdown reports may expose sensitive details if opened in a renderer or workspace with remote-loading or sharing behavior.

Mitigation: Review generated Markdown before opening it in renderers that auto-load remote images or publishing it to shared spaces.

Risk: Rule-based category matching and LLM review can misclassify transactions or budget categories.

Mitigation: Review low- and medium-confidence transactions, especially items categorized as Other, before generating or relying on the final report.

## Reference(s):

- [Spending Categories Reference](references/categories.md)
- [CSV Format Reference](references/csv-formats.md)
- [Local Budget ClawHub Release](https://clawhub.ai/newageinvestments25-byte/skills/nai-local-budget)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with bash commands, local JSON files, and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided CSV exports; generated transaction JSON and reports are written to user-selected paths.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
