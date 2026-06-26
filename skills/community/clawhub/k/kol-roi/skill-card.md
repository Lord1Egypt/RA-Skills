## Description: <br>
Decode KOL and creator "black box" performance by stripping refunds, suspicious traffic, and vanity clicks to estimate each creator's true profit contribution and produce a renewal-style P&L view. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rijoyai](https://clawhub.ai/user/rijoyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, ecommerce, and affiliate operations teams use this skill to compare creators by net-of-refund revenue, true ROI, traffic quality, and renewal economics. It is intended for decisions about renewing, renegotiating, pausing, or extending KOL and creator campaigns with linked order or payout data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creator ROI can be misleading when refunds, chargebacks, attribution rules, or cost assumptions are incomplete. <br>
Mitigation: State the attribution rule, refund treatment, ROI formula, currency, tax treatment, and missing-data assumptions before making renewal recommendations. <br>
Risk: Traffic-quality heuristics can suggest suspicious behavior without proving fraud. <br>
Mitigation: Describe quality signals as heuristics, note what cannot be proven without platform data, and recommend verification steps such as code rotation, payout caps, or delayed commission. <br>


## Reference(s): <br>
- [KOL attribution, refunds, and traffic quality playbook](references/kol_attribution_playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown with a creator renewal ledger table, adjustment notes, renewal economics, and data checklist when inputs are missing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires attributed orders, refund or chargeback data, and creator cost assumptions for complete ROI recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
