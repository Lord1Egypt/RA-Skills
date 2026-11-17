## Description:

工资代发与银行回单核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，并仅执行免费版声明的检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and treasury users use this skill during monthly payroll closing, reconciliation, and audit preparation to check payroll disbursement tables against deterministic table-level consistency rules. It reports cited findings and missing input rather than making conclusions when the material is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free version intentionally omits several reconciliation checks, including bank receipt amount versus disbursement amount comparison.

Mitigation: Use the output as a limited table-level check and do not rely on it as a complete financial control.

Risk: Payroll tables may contain sensitive personal and compensation data.

Mitigation: Install and run only in an environment approved for payroll data; server security evidence reports no hidden network, persistence, credential, or destructive behavior.

Risk: Incomplete or unrecognized input can otherwise lead users to overread the absence of findings.

Mitigation: The skill returns insufficient-input guidance and does not output a no-issue conclusion when required material is missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/payroll-payment-bank-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable console text or structured JSON with cited reconciliation findings, scope notes, and insufficient-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard-library code; the free version reports its executed and withheld checks.]

## Skill Version(s):

1.0.52 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
