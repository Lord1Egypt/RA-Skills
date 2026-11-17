## Description:

Checks a Chinese input VAT deduction reconciliation table locally by recalculating row-level deductions, verifying totals, detecting duplicate periods and blanks, and citing source lines for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill during monthly closing or reconciliation to check Chinese input VAT certification, transfer-out, and declared deduction tables. It is useful when users need deterministic local findings with cited source rows, while separately reviewing tax eligibility and checks outside the free version.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free version omits several tax-rate, negative-value, over-deduction, certified-but-not-deducted, and negative carryover checks.

Mitigation: Review the output's checks_not_run list and verify those omitted checks separately before treating the reconciliation as complete.

Risk: The skill does not determine whether an input VAT item is legally deductible or whether it should be transferred out.

Mitigation: Use the findings as arithmetic and table-consistency checks only, and route eligibility or tax-policy decisions to qualified tax review.

Risk: When required table content or headers are missing, the skill intentionally gives no conclusion.

Mitigation: Provide the input VAT deduction reconciliation table with the required period, certified amount, certified tax, declared deduction, and transfer-out columns before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/input-vat-deduction-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON findings with executed checks, omitted checks, scope, summary, and cited line-level messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with no network use or persistence according to the security evidence; exits without a conclusion when required table content is missing.]

## Skill Version(s):

1.0.58 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
