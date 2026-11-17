## Description:

课时核销表逐项核对（逐行算术、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations staff use this skill during monthly close, reconciliation, or inventory checks to verify lesson-hour tables. It checks included arithmetic, totals, duplicate learners, blanks, and placeholders, with findings tied back to source line numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean result could be misunderstood as complete reconciliation because the free version intentionally omits several documented checks.

Mitigation: Review the listed omitted checks before relying on results, and use an expanded review process when those checks matter.

Risk: Financial or operational decisions could be wrong if the input table is incomplete, lacks recognizable headers, or is misformatted.

Mitigation: Provide the lesson-hour table with headers and review each line-referenced finding against the source material before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/lesson-hour-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis, Guidance]

**Output Format:** [Human-readable text or structured JSON with findings, summaries, omitted checks, and source line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite original input lines; insufficient input returns missing requirements instead of a pass/fail conclusion.]

## Skill Version(s):

1.0.28 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
