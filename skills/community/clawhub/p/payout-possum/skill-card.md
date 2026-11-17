## Description:

Comprehensive money-recovery specialist for finding money, benefits, refunds, settlements, unclaimed property, pensions, bankruptcy funds, escrow balances, and other amounts owed to a person.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chadnewbry](https://clawhub.ai/user/chadnewbry)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to run a structured sweep for overlooked money, benefits, refunds, settlements, unclaimed property, pensions, bankruptcy funds, escrow balances, and related claims. It helps organize official-source searches, inbox evidence checks when approved, and a tracker of possible matches, missing inputs, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Money-recovery searches can involve sensitive personal history such as names, prior addresses, employers, banks, insurers, and claim notices.

Mitigation: Share only the minimum details needed for each search and avoid providing full account numbers or unnecessary identifiers.

Risk: Inbox coverage can expose private Gmail messages during settlement, refund, pension, benefits, escrow, or restitution searches.

Mitigation: Approve Gmail access only when inbox coverage is wanted, keep the work read-only by default, and treat email as supporting evidence rather than the source of record.

Risk: Running the bundled local installer can replace existing local payout-possum skill customizations.

Mitigation: Back up any existing local payout-possum customization before running the installer.

## Reference(s):

- [Payout Possum Source Directory](references/source-directory.md)
- [Payout Possum Source Map](references/source-map.md)
- [NAUPA directory](https://unclaimed.org/)
- [USA.gov unclaimed money hub](https://www.usa.gov/unclaimed-money)
- [U.S. Courts bankruptcy unclaimed funds](https://www.uscourts.gov/court-programs/bankruptcy/unclaimed-funds-bankruptcy)
- [FTC consumer refunds](https://www.ftc.gov/terms/consumer-refunds)
- [CFPB payments to harmed consumers](https://www.consumerfinance.gov/enforcement/payments-harmed-consumers/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with plain-text tracker tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source-by-source status labels, confidence labels, missing-input notes, and next actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
