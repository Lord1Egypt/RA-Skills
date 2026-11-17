## Description:

Calculates principal, in-term interest, overdue interest, penalties, compounding, repayment allocation, and statutory rate caps for Chinese private lending matters, then helps generate a structured interest calculation sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolalam](https://clawhub.ai/user/coolalam)

### License/Terms of Use:

MIT-0

## Use Case:

Legal and financial users handling Chinese private lending matters use this skill to collect loan facts, run local calculations, and explain legally protected interest, repayment allocation, assumptions, and risk warnings.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may treat the generated calculation sheet as legal advice or a final court-ready conclusion.

Mitigation: Present the output as a calculation aid and require qualified legal review before reliance or submission.

Risk: Incorrect loan dates, missing repayment records, or stale LPR data can change the protected interest cap and final totals.

Mitigation: Verify case facts, repayment inputs, cutoff dates, and the applicable LPR source before using the numbers.

Risk: Pre-2015 loans, compounding, professional lender issues, and local court practice may require judgment beyond mechanical calculation.

Mitigation: Flag these scenarios for manual review and document all assumptions in the final calculation explanation.

## Reference(s):

- [Legal Basis](references/legal_basis.md)
- [Calculation Rules](references/calculation_rules.md)
- [LPR Data](references/lpr_data.md)
- [Bank of China LPR Reference](https://www.boc.cn/fimarkets/lilv/fd32/201310/t20131031_2591219.html)
- [ClawHub Skill Page](https://clawhub.ai/coolalam/skills/private-lending-interest-calculator)
- [Publisher Profile](https://clawhub.ai/user/coolalam)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text calculation report with tabular sections and optional bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs assumptions and risk warnings alongside calculated principal, interest, penalties, fees, repayment allocation, and legal cap checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
