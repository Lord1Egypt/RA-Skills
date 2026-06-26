## Description: <br>
India Tax Helper helps resident salaried individuals in India understand tax declarations, Form 12BB, Form 16, AIS/TIS/26AS, ITR filing, FD/RD taxation, loan deductions, and capital-gains basics with conservative, calculator-backed guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aritrocoder](https://clawhub.ai/user/aritrocoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Resident salaried individuals in India use this skill to understand payroll tax declarations, filing documents, tax lifecycle deadlines, common income add-ons, deduction questions, and approximate tax treatment. Agents use it to provide concise, conservative guidance and to run deterministic local calculators when numbers matter. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat educational estimates as professional tax advice. <br>
Mitigation: Present outputs as educational estimates and direct users to verify current FY rules with official Income Tax Department sources or a qualified tax professional before acting. <br>
Risk: FY-specific rates, deadlines, forms, and filing rules can become stale. <br>
Mitigation: Ground FY-sensitive answers against current official sources during use and fail closed when a key rule or date cannot be verified. <br>
Risk: Some local tax calculations are simplified or incomplete, including surcharge and capital-gains edge cases. <br>
Mitigation: Disclose assumptions, use deterministic calculators for estimates, and avoid confident conclusions when the calculator coverage or user facts are insufficient. <br>


## Reference(s): <br>
- [Overview](references/overview.md) <br>
- [Source policy](references/source-policy.md) <br>
- [Live grounding](references/live-grounding.md) <br>
- [Forms map](references/forms-map.md) <br>
- [Lifecycle calendar](references/lifecycle-calendar.md) <br>
- [Answer patterns](references/answer-patterns.md) <br>
- [ClawHub skill listing](https://clawhub.ai/aritrocoder/india-tax-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Plain text guidance with optional shell commands for local deterministic calculators] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calculators use JSON inputs and outputs internally; user-facing responses should stay concise and disclose uncertainty.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
