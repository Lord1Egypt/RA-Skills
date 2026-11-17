## Description:

应付职工薪酬台账逐项核对，每条结论都带原文依据，不需要付款，也不需要注册。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and payroll operations users use this skill during monthly close, reconciliation, or inventory checks to review payroll payable ledgers for arithmetic consistency, totals, duplicate periods, and blank or placeholder fields. It is intended for locally supplied ledger text and does not decide payroll, tax, or social insurance calculation policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes payroll amounts supplied by the user, and incorrect input formatting or incomplete ledgers can affect the usefulness of the result.

Mitigation: Review the output against the original ledger, and use the missing-input guidance when the skill reports insufficient material.

Risk: The free version explicitly omits several checks documented by the artifact, so a clean result is not a full payroll payable audit.

Mitigation: Treat the result as coverage for the listed free checks only and perform separate review for omitted or out-of-scope checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/payroll-payable-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown instructions and CLI text or JSON findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided payroll payable ledger text; insufficient input returns missing-field guidance instead of a conclusion.]

## Skill Version(s):

1.0.53 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
