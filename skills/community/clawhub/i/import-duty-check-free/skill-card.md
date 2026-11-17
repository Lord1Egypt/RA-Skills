## Description:

进口税费计算表逐项核对（逐行算术复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。触发词包括 进口税费核对、关税算错、增值税不对、完税价格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Importers, freight forwarders, customs staff, and finance teams use this skill before payment to re-check import duty, consumption tax, value-added tax, totals, duplicate product rows, and blank fields in copied worksheet text or JSON input. It reports findings with source line numbers and does not provide customs, tariff-classification, or tax advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake deterministic worksheet checks for customs or tax advice.

Mitigation: Treat results as arithmetic and consistency checks only; have qualified customs or tax reviewers confirm tax codes, rates, declared value, and filing decisions.

Risk: Incomplete or unrecognized input can lead to missing checks or no conclusion.

Mitigation: Provide copied worksheet text or JSON with recognizable headers and review any insufficient-input message before relying on the output.

Risk: The free version does not execute every possible anomaly check.

Mitigation: Review the listed withheld and out-of-scope checks, especially tax-rate range, nonpositive dutiable value, negative tax, and overall tax-burden anomaly checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/import-duty-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON containing findings, summaries, executed checks, withheld checks, and insufficient-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; the runner returns nonzero exit codes for missing input, insufficient material, unreadable input, and unexpected errors.]

## Skill Version(s):

1.0.36 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
