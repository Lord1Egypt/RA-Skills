## Description:

材料成本差异分摊核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

Proprietary

## Use Case:

Finance and accounting users use this skill during month-end closing, reconciliation, or inventory checks to review material cost variance allocation tables for arithmetic, totals, duplicate rows, blanks, and missing inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker processes material cost variance allocation table data locally, which may include business-sensitive accounting information.

Mitigation: Run it only in an approved local environment and avoid supplying data you are not allowed to process on that machine.

Risk: The free version intentionally omits several additional checks and is mainly designed for Chinese-language table inputs.

Mitigation: Review the listed withheld and out-of-scope checks before relying on results, and use manual review or another approved workflow for unsupported cases.

Risk: Insufficient or unrecognized input does not produce a positive or negative finding.

Mitigation: Provide the required table headers and rows, and treat missing-input guidance as a request for more evidence rather than as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/material-cost-variance-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill definition](artifact/SKILL.md)
- [Sample input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Console text or structured JSON findings with cited source rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node.js execution; insufficient input returns missing-field guidance instead of a conclusion.]

## Skill Version(s):

1.0.56 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
