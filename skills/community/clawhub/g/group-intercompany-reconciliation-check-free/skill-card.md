## Description:

集团内部往来对账与抵消核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill during monthly closing, reconciliation, or inventory control to check group intercompany reconciliation and elimination tables for row-level arithmetic, totals, duplicates, missing fields, and cited findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes reconciliation-table data on the local machine.

Mitigation: Install and run it only in an environment approved for the user's reconciliation data; evidence indicates no network access, credential handling, registration, payment, or hidden persistence.

Risk: The free edition omits several disclosed business-substance checks, including tolerance overages, opposite-direction unresolved balances, over-elimination, unmatched internal transactions, and similar-name detection.

Mitigation: Treat results as local table-arithmetic and completeness checks, and separately review the omitted checks before relying on the reconciliation.

Risk: Insufficient or malformed input can prevent the checker from producing a conclusion.

Mitigation: Provide the complete table with headers and required fields; when data is insufficient, the tool should report missing material instead of claiming no issues were found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/group-intercompany-reconciliation-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Shell commands, Guidance]

**Output Format:** [Console text or JSON with reconciliation findings, cited source rows, executed checks, omitted checks, and input-status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; free edition reports the checks it executes and the checks it omits.]

## Skill Version(s):

1.0.53 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
