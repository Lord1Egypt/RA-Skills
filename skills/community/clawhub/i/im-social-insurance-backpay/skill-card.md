## Description:

内蒙古养老保险补缴计算工具用于估算内蒙古地区养老保险补缴本金、按月复利计算的利息、滞纳金和不同缴费档次的汇总金额。

This skill is ready for commercial/non-commercial use.

## Publisher:

[binbin](https://clawhub.ai/user/binbin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to estimate Inner Mongolia pension insurance backpay over a selected month range, compare 60% through 300% payment tiers, and generate personal, employer, interest, late-fee, and total amount breakdowns. Results are advisory and should be checked against official social-security authority calculations before financial decisions.

### Deployment Geography for Use:

China (Inner Mongolia)

## Known Risks and Mitigations:

Risk: Calculated backpay amounts may differ from official social-security authority results because wage, rate, late-fee, exemption, and eligibility rules can vary or change.

Mitigation: Treat results as estimates and verify financial decisions with the local social-security authority or employer records.

Risk: Weak input validation or invalid month ranges, rates, or custom monthly bases can produce misleading output or execution errors.

Mitigation: Use valid supported month ranges and positive finite rates or monthly bases before relying on output.

Risk: Late-fee responsibility and reduction policies may depend on local rules, hardship status, or whether an employer caused the missed payment.

Mitigation: Confirm late-fee responsibility and any available reduction policy with the relevant authority before payment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/binbin/skills/im-social-insurance-backpay)
- [内蒙古历年社会平均工资](references/social_avg_wages.md)
- [养老保险个人账户记账利率](references/interest_rates.md)
- [养老保险补缴政策规则](references/policy_rules.md)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell and Python examples plus JSON calculation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local calculator output with RMB amounts rounded to two decimals and summaries for principal, interest, late fees, totals with late fees, and totals without late fees.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
