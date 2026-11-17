## Description:

Decode KOL and creator performance by netting refunds, screening suspicious traffic, and estimating true ROI for renewal or renegotiation decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, affiliate, and ecommerce teams use this skill to convert creator order, payout, refund, and traffic exports into renewal recommendations and breakeven economics. It is intended for KOL or influencer programs with attributable orders, discount codes, links, or UTM data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste sensitive order, refund, affiliate, Shopify, or GA4 exports while using the skill.

Mitigation: Remove unnecessary customer identifiers and share only the columns needed for creator ROI, refund, payout, and attribution analysis.

Risk: Traffic-quality checks are heuristics and cannot prove fraud or misconduct without platform evidence.

Mitigation: Frame suspicious traffic findings as verification leads, then confirm with source-platform data before taking external action.

Risk: Incorrect attribution, refund-window, margin, or commission assumptions can change renewal recommendations.

Mitigation: State the attribution rule, reporting window, refund treatment, cost model, and ROI formula before interpreting the renewal ledger.

## Reference(s):

- [KOL attribution, refunds, and traffic quality playbook](artifact/references/kol_attribution_playbook.md)
- [ClawHub skill page](https://clawhub.ai/rijoyai/skills/kol-roi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with tables, bullets, and renewal economics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed five-column creator renewal ledger and may include templates or export checklists when source data is missing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
