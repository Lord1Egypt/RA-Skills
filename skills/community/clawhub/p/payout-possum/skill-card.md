## Description: <br>
Comprehensive money-recovery specialist for finding money, benefits, refunds, settlements, unclaimed property, pensions, bankruptcy funds, escrow balances, and other amounts owed to a person. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chadnewbry](https://clawhub.ai/user/chadnewbry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to run a structured sweep for possible unclaimed property, refunds, settlements, benefits, retirement funds, bankruptcy funds, and other amounts owed. It helps organize official-source searches, missing inputs, confidence labels, and next actions, with optional read-only Gmail evidence review when the user approves inbox coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may involve sensitive personal financial history, addresses, employers, account relationships, and optional email evidence. <br>
Mitigation: Share only the minimum details needed for each search category, avoid full SSNs or full account numbers unless an official verified claims process requires them, and keep optional Gmail review targeted and read-only. <br>
Risk: Third-party or discovery sites can produce weak leads, misleading eligibility signals, or pressure users toward fee-based recovery services. <br>
Mitigation: Prefer official government, court, agency, administrator, or institution sources first, treat third-party sites only as leads, and flag upfront fees or unnecessary document requests before the user acts. <br>


## Reference(s): <br>
- [Payout Possum Source Map](references/source-map.md) <br>
- [Payout Possum Source Directory](references/source-directory.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/chadnewbry/payout-possum) <br>
- [NAUPA Unclaimed Property Directory](https://unclaimed.org/) <br>
- [USA.gov Unclaimed Money Hub](https://www.usa.gov/unclaimed-money) <br>
- [U.S. Courts Bankruptcy Unclaimed Funds](https://www.uscourts.gov/court-programs/bankruptcy/unclaimed-funds-bankruptcy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text with a lightweight tracker table and next-action lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses official sources first, labels evidence confidence, and keeps Gmail review read-only unless the user requests otherwise.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
