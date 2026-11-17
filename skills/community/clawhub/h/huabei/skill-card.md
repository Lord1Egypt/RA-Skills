## Description:

Huabei helps agents explain Ant Credit Pay usage, estimate real annualized installment costs with a local IRR calculator, and discuss interest-free periods, repayment planning, credit-report impact, and account controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to reason about Huabei installment costs, repayment choices, credit-report considerations, and account-limit or closure paths. It is most useful when a user provides installment amount, term, and fee information that can be checked with the included IRR calculator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may make financial decisions from static guidance when actual Huabei fees, credit-report treatment, or account options differ by account or change over time.

Mitigation: Confirm current fees, credit-report treatment, and account controls in Alipay before making repayment, installment, or closure decisions.

Risk: The calculator is intended for ordinary positive installment inputs and may not cover unusual or edge-case financing scenarios.

Mitigation: Use ordinary positive inputs and seek authoritative financial review for unusual fee structures or high-stakes borrowing decisions.

Risk: The skill is primarily Chinese-language, which can reduce usability or increase misunderstanding for readers who do not read Chinese fluently.

Mitigation: Provide bilingual clarification or translation when supporting non-Chinese readers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/huabei)
- [Publisher profile](https://clawhub.ai/user/zhangifonly)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands]

**Output Format:** [Markdown with inline shell commands and numeric calculator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local zero-dependency Python IRR calculator when installment inputs are provided.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
