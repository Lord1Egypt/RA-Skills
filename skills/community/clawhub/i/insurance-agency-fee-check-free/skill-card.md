## Description:

保险代理手续费与佣金结算核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations users use this skill during monthly settlement or reconciliation to check insurance agency commission settlement tables for line arithmetic, total reconciliation, duplicate rows, blanks, and negative amounts or rates. It reports findings with source-line evidence and states when the supplied material is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes insurance commission settlement data through a local Node script.

Mitigation: Install and run it only in an environment where local execution on that data is acceptable, and prefer JSON output when complete machine-readable results are needed.

Risk: The free release explicitly omits several checks, including agreement-rate mismatch and some duplicate-settlement checks.

Mitigation: Review the reported checks_not_run list before relying on results, and do not treat a clean free-version result as coverage of omitted checks.

Risk: The skill checks table arithmetic and reconciliation, but does not decide regulatory, contract, invoicing, banking, or accounting treatment.

Mitigation: Use the findings as reconciliation evidence and confirm contract, compliance, tax, cash-receipt, and accounting questions with the responsible source documents or reviewer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/insurance-agency-fee-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [CLI text or JSON containing executed checks, findings, summary, omitted checks, and scope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-supplied table text; insufficient input returns missing material and advice instead of a conclusion.]

## Skill Version(s):

1.0.48 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
