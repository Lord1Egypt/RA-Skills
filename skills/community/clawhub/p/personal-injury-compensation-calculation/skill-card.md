## Description:

Calculates China-focused personal injury compensation amounts and structured compensation breakdowns using the bundled Python calculator and local legal and statistical references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolalam](https://clawhub.ai/user/coolalam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and legal practitioners use this skill to calculate injury or death compensation items under China-focused personal injury compensation rules and to produce structured compensation details.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Outputs are legal and financial estimates that may be wrong if statistics, dates, court location, or evidence assumptions are outdated or incomplete.

Mitigation: Verify current official province or city statistics, case facts, and legal assumptions before relying on results, and consult a qualified lawyer for case-specific advice.

Risk: User-provided statistics_overrides can materially change compensation amounts.

Mitigation: Review each override against an authoritative government or court source and keep the source and year with the case record.

Risk: Markdown, JSON, or XLSX report generation can write sensitive case information to chosen file paths.

Mitigation: Choose output paths deliberately, avoid shared directories for confidential cases, and inspect generated files before distribution.

## Reference(s):

- [人身损害赔偿计算公式大全](references/formulas.md)
- [全国各省历年职工平均工资数据（人身损害赔偿用）](references/provincial_avg_wage.md)
- [全国城镇居民人均可支配收入（人身损害赔偿用）](references/disposable_income.md)
- [人身损害赔偿核心法条库](references/law_articles.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown, JSON, and optional XLSX report files with supporting shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires case facts and local statistical inputs; missing statistics should be supplied through reviewed overrides before recalculation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
