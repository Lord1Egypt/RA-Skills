## Description:

A Chinese-language payroll pre-release checker that runs locally on pasted salary-sheet text to flag net-pay arithmetic errors, incorrect total rows, duplicate people, and blank or placeholder values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

HR, payroll, finance, and accounting users use this skill before payroll release to check whether a provided salary sheet has arithmetic, total-row, duplicate-person, blank, or placeholder issues within the free version's stated scope. It reports findings with source line references and does not decide what an employee should be paid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payroll data can contain sensitive personal and compensation information.

Mitigation: Use the skill only with payroll data intended for local processing and avoid sharing input files beyond the local Node.js workflow.

Risk: The free version checks only the stated arithmetic, total-row, duplicate-person, blank, and placeholder conditions.

Mitigation: Treat a clean result as limited to those checks; separately review tax, labor-policy, benefit-base, bank-disbursement, and out-of-scope compensation questions.

Risk: Chinese-language trigger wording is broad and may activate during general payroll discussions.

Mitigation: Confirm the user is asking to check a payroll sheet before running scripts or processing payroll material.

Risk: Unrecognized or incomplete table headers can make the material insufficient for reliable checking.

Mitigation: Require a salary sheet that includes headers and the needed columns, especially name and net-pay fields; do not treat insufficient input as a clean payroll result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/payroll-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON containing payroll-check findings, summary status, executed and withheld checks, source-line evidence, and remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs through local Node.js scripts on user-provided salary-sheet text; exits with distinct status codes for success, missing input, insufficient material, parse/read failures, and unexpected errors.]

## Skill Version(s):

1.0.53 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
