## Description:

发票领用存台账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and cashier teams use this skill during monthly close, reconciliation, or inventory checks to review invoice usage and stock ledgers. It performs the free deterministic checks for row arithmetic, totals, duplicate periods, missing fields, and cited findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free-version output as a complete tax or invoice compliance review.

Mitigation: Use it as a local ledger arithmetic and consistency check; the output lists checks not run and out-of-scope compliance judgments.

Risk: Invoice usage and stock ledgers can contain sensitive operational data.

Mitigation: Run the checker locally on a trusted machine and review inputs before execution; the security evidence reports no hidden network, persistence, credential, or destructive behavior.

Risk: Incomplete or malformed table input can produce no conclusion.

Mitigation: Provide ledger text with the required headers and review the tool's missing-input guidance; it does not report no issues when materials are insufficient.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenqg618/skills/invoice-usage-stock-check-free)
- [Publisher Profile](https://clawhub.ai/user/chenqg618)
- [Skill Instructions](artifact/SKILL.md)
- [Sample Input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable CLI text or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes executed checks, checks not run, line-cited findings, summary counts, insufficient-input guidance, and local execution indicators.]

## Skill Version(s):

1.0.56 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
