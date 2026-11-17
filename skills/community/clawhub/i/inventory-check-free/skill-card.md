## Description:

库存盘点表逐项核对（逐行算术、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and warehouse operations staff use this skill to reconcile inventory count tables at month-end, payroll, settlement, or stocktaking checkpoints. It checks deterministic arithmetic and table consistency while citing source rows for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes the input file or pasted table supplied by the user, which may contain operational inventory data.

Mitigation: Use only the intended inventory reconciliation material and avoid passing unrelated sensitive documents.

Risk: Incomplete or unrecognized table input can prevent a reliable reconciliation conclusion.

Mitigation: Provide a complete inventory count table with recognizable headers and review the missing-material guidance when the skill reports insufficient input.

Risk: The free release omits some advanced checks, including threshold, negative-inventory, inbound amount, and dormant-item checks.

Mitigation: Treat results as limited to the declared free checks and perform any omitted checks separately when they are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/inventory-check-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, analysis, guidance]

**Output Format:** [Markdown or JSON-formatted local reconciliation results with source row references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided inventory table input; insufficient input returns missing-material guidance instead of a conclusion.]

## Skill Version(s):

1.0.54 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
