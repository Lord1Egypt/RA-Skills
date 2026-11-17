## Description:

检测样品流转与留样台账逐项核对 6 项（数量勾稽、留样期限、交接单一致性、重复登记、合计行复核、字段与状态校验），每条结论都引用原文行号与原文内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External laboratory sample managers, QA teams, and internal auditors use this skill to check copied lab sample handover and retention ledgers before monthly inventory reviews, CMA/CNAS assessments, spot checks, and internal audits. It performs six local in-table checks and returns source-line evidence for each conclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill prints source-line evidence from submitted ledgers, which may expose sensitive sample, client, or audit data in terminal output.

Mitigation: Run it only in an environment where terminal output is appropriate for that data, and avoid submitting rows that should not be displayed.

Risk: The free release intentionally omits several checks from the full version and does not determine sample compliance, testing validity, required retention duration, or facility controls.

Mitigation: Use the results as ledger consistency checks only, and keep human review for compliance judgments and out-of-scope controls.

Risk: Input materials with missing required columns produce an insufficient-input result rather than a positive or negative conclusion.

Mitigation: Provide a copied ledger with the required table headers and rerun the skill before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/lab-sample-retention-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill documentation](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, json, analysis, guidance]

**Output Format:** [Plain text or JSON findings with source-line evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally from a Node.js command and reports insufficient input instead of fabricating conclusions.]

## Skill Version(s):

1.0.3 (source: server release metadata; SKILL.md frontmatter says 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
