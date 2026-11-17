## Description:

Three-phase money crisis protocol: immediate triage when you can't pay bills, surviving on drastically reduced income, and building financial resilience once stable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to prioritize urgent bills, contact creditors, find assistance programs, survive reduced income, and rebuild an emergency fund after a financial shock.

### Deployment Geography for Use:

Global, with US-centric crisis resources that require localization for non-US users.

## Known Risks and Mitigations:

Risk: The skill can involve sensitive financial details in persistent state and reminder workflows.

Mitigation: Enable persistence and reminders only with clear consent, per-user isolation, deletion controls, and protection for financial data.

Risk: The skill's assistance programs, phone numbers, and legal implications are US-centric.

Mitigation: Ask for the user's country or region before jurisdiction-specific guidance, substitute local equivalents, cite sources, and tell the user what was localized.

Risk: Financial-crisis guidance may be harmful if treated as individualized legal, tax, or financial advice.

Mitigation: Frame outputs as planning support, prioritize immediate safety and essential needs, and refer users to qualified local assistance, legal aid, or nonprofit credit counseling when appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/money-crisis-ladder)
- [USDA SNAP](https://www.fns.usda.gov/snap)
- [LIHEAP](https://www.acf.hhs.gov/ocs/programs/liheap)
- [Emergency Rental Assistance](https://home.treasury.gov/policy-issues/coronavirus/assistance-for-state-local-and-tribal-governments/emergency-rental-assistance-program)
- [211 helpline](https://www.211.org/)
- [Benefits.gov](https://www.benefits.gov/)
- [Federal Poverty Guidelines](https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines)
- [Federal Student Aid income-driven repayment](https://studentaid.gov/manage-loans/repayment/plans/income-driven)
- [CFPB housing help](https://www.consumerfinance.gov/housing/)
- [FDIC](https://www.fdic.gov)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with scripts, checklists, state fields, and reminder trigger definitions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request calendar and filesystem capabilities for reminders and persistent crisis-planning state.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
