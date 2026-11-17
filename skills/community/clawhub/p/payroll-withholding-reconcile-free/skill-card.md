## Description:

工资表与个税社保申报对照表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文；本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, payroll, HR, and bookkeeping users use this skill during monthly closing or reconciliation to compare payroll withholding against individual income tax and social-insurance filing data. It checks row-level arithmetic, totals, duplicate people, blank fields, and missing filing-side values, and it avoids drawing conclusions when required input is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payroll input can contain sensitive personal and compensation data.

Mitigation: Run the included Node.js script locally, review the ClawHub security summary before installation, and avoid sharing input files outside the trusted environment.

Risk: The free version omits several payroll and filing checks, so a clean result is not a full payroll, tax, or social-insurance compliance audit.

Mitigation: Use the report only for the documented free reconciliation checks and separately review omitted checks, tax calculations, social-insurance rules, and special payroll cases.

Risk: The skill's user-facing output is Chinese-language and may not fit every payroll workflow.

Mitigation: Confirm that Chinese-language command output and report fields are acceptable for the intended users before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/payroll-withholding-reconcile-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Chinese-language terminal text or JSON reconciliation report, with local Node.js commands for running the sample or user input.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report lists executed free checks, checks not run in the free version, findings with source line references, summary counts, local execution status, and missing-input guidance when input is insufficient.]

## Skill Version(s):

1.0.53 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
