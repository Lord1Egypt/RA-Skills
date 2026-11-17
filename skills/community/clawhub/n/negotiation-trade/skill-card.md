## Description:

In-person negotiation skills and barter/trade techniques for negotiating prices, hiring contractors, disputing bills, buying or selling used goods, and trading skills or labor instead of money.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to get practical scripts, checklists, and guidance for real-world negotiation situations such as contractor bids, used-car purchases, medical bills, rent discussions, casual haggling, freelance rates, and barter arrangements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests filesystem access even though the release evidence describes it as mainly negotiation advice.

Mitigation: Remove or restrict filesystem access unless a concrete file-based feature is added.

Risk: The install command uses an unpinned external `npx` installer.

Mitigation: Use a pinned, integrity-verified installation path before deployment.

Risk: Negotiation, medical bill, consumer, contractor, landlord, and barter guidance can vary by jurisdiction and culture.

Mitigation: Adapt advice to the user's location and verify legal, tax, healthcare, and consumer-protection requirements before acting.

## Reference(s):

- [Skill page](https://clawhub.ai/howtousehumans/skills/negotiation-trade)
- [Patient Advocate Foundation](https://www.patientadvocate.org/)
- [Federal Trade Commission used car buying guide](https://consumer.ftc.gov/articles/buying-used-car)
- [IRS Publication 525](https://www.irs.gov/publications/p525)
- [Time banking networks](https://timebanking.org/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with scripts, checklists, and scenario-specific steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May adapt advice by region, culture, and negotiation scenario.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
