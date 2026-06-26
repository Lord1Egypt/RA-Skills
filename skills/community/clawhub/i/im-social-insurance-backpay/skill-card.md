## Description: <br>
用于估算内蒙古地区养老保险补缴本金、按月复利利息、滞纳金，并对比不同缴费档次。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binbin](https://clawhub.ai/user/binbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents can use this skill to estimate Inner Mongolia pension insurance backpay for a selected date range, payment tier, target payment date, or custom monthly base. It produces principal, interest, late-fee, and with-or-without-late-fee summaries for review before official filing. <br>

### Deployment Geography for Use: <br>
China (Inner Mongolia policy context) <br>

## Known Risks and Mitigations: <br>
Risk: Wage, interest-rate, or policy assumptions may be outdated or differ from official local calculations. <br>
Mitigation: Verify inputs and results with official social-security sources or the local social-security office before relying on monetary estimates. <br>
Risk: Backpay eligibility, late-fee reductions, and payment responsibility can vary by individual situation and local policy. <br>
Mitigation: Use the calculation as an estimate and confirm eligibility, reductions, and responsibility with the local social-security office. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/binbin/im-social-insurance-backpay) <br>
- [内蒙古历年社会平均工资](references/social_avg_wages.md) <br>
- [养老保险个人账户记账利率](references/interest_rates.md) <br>
- [养老保险补缴政策规则](references/policy_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [JSON calculation summaries and console tables, with optional Markdown guidance from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local estimate calculations only; monetary results should be verified with official social-security sources before reliance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
