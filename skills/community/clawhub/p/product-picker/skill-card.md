## Description:

Product Picker is a workflow for comparing home-product candidates with weighted signals from Xiaohongshu, JD.com, and Taobao, then producing a ranked product-fit report for Shangpin Home Collection scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunni123](https://clawhub.ai/user/yunni123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business analysts use this skill to evaluate whether candidate products fit a furniture and home-customization scenario. It combines social engagement, ecommerce conversion, and strategic fit into a ranked recommendation with decision thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated product-analysis reports are saved locally and sent as Feishu attachments.

Mitigation: Use the skill only when Feishu is approved for the product, customer, and strategy data included in the report.

Risk: Product ranking depends on collected marketplace and social-platform data plus qualitative fit scoring.

Mitigation: Review source data, cleaned records, scoring assumptions, and final recommendations before making business decisions.

## Reference(s):

- [Report template](references/report_template.md)
- [ClawHub skill page](https://clawhub.ai/yunni123/skills/product-picker)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown report with tabular scoring details, summary text, a JSON-style Feishu file-send action, and optional PPT handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow saves generated reports locally, sends the Markdown report as a Feishu attachment, keeps an Excel result file as a local supplemental artifact, and asks for confirmation before optional PPT generation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
