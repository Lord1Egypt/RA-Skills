## Description:

直播佣金与坑位费结算核对（免费版）逐项核对直播结算表的逐行复算、合计勾稽、重复与空缺，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and live-commerce operations teams use this skill during monthly close, reconciliation, inventory review, and payment approval to locally check commission and slot-fee settlement tables. It recalculates arithmetic relationships, checks totals, and reports missing or duplicated rows with source-row evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free-version result as complete payment approval even though several higher-level settlement checks are explicitly withheld.

Mitigation: Review checks_given and checks_withheld before relying on the result, and add separate review for contract-rate, excessive-return, excessive-commission, duplicate-settlement, and zero-slot-fee cases.

Risk: Incomplete or malformed input can prevent the checker from reaching a conclusion.

Mitigation: Run --sample or --json first, provide the settlement table with headers, and treat insufficient_input as no conclusion rather than approval.

Risk: The skill checks arithmetic and table consistency in user-provided data, not contractual interpretation, platform exports, or bank settlement matching.

Mitigation: Use contract terms, platform reports, and payment records as separate evidence for business approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/live-commerce-commission-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON settlement-check report with cited source rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided settlement material and reports checks_given and checks_withheld for the free version.]

## Skill Version(s):

1.0.50 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
