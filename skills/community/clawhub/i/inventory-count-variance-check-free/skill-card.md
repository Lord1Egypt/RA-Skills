## Description:

存货盘点表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing, retail, and logistics inventory accountants and warehouse staff use this skill before inventory count adjustments to recalculate detail rows and totals, detect duplicate or incomplete rows, and cite source rows for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic or completeness findings as accounting advice, audit evidence, ERP/WMS reconciliation, or a complete variance-control review.

Mitigation: Use the output as a local arithmetic and completeness aid only, and have qualified finance, audit, or operations staff review accounting treatment and source-system reconciliation.

Risk: The free version omits higher-level checks such as blank variance reasons, major variance thresholds, negative count quantities, and unclear variance explanations.

Mitigation: Review the omitted checks before relying on the results, and perform separate controls or use a fuller review process when those conditions matter.

Risk: Results depend on pasted table quality and recognizable headers.

Mitigation: Provide complete inventory count tables with headers and source rows; rerun after correcting missing columns, blank cells, placeholders, or parsing issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/inventory-count-variance-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with local CLI commands and evidence-cited findings; optional JSON output from the bundled checker.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows, include P0/P1 severity labels, and list checks that were not run in the free version.]

## Skill Version(s):

1.0.18 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
