## Description:

工程材料调拨与领用核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashiering, and project accounting teams use this skill during month-end reconciliation, account checking, and inventory review to check Chinese engineering material transfer and issue tables. It recomputes table arithmetic, checks totals, detects duplicate rows and blanks, and reports findings with source line references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free version intentionally omits several checks, so a clean result is not a full audit.

Mitigation: Review the listed checks_not_run and out-of-scope items, and use separate review for full audit coverage.

Risk: The skill is designed for a specific Chinese engineering material transfer and issue table format.

Mitigation: Use it only with matching source tables that include recognizable headers; when input is insufficient, do not treat the absence of findings as a conclusion.

Risk: Table arithmetic can balance even when physical materials or project cost allocation are wrong.

Mitigation: Reconcile results with source documents, project controls, and physical inventory counts before relying on them for business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/project-material-transfer-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable text or structured JSON report with cited findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local deterministic checks on user-provided table text and reports withheld or out-of-scope checks when applicable.]

## Skill Version(s):

1.0.54 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
