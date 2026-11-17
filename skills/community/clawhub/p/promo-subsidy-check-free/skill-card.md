## Description:

促销补贴核销表逐项核对（应结补贴与差异复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。触发词包括 促销补贴核对、补贴核销、活动补贴没结到、应结补贴。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Retail and e-commerce operators use this skill after promotions to reconcile subsidy settlement tables, recalculate payable subsidy and differences, check totals, and detect duplicate or blank rows. It is intended for user-supplied tabular materials and returns line-referenced findings when enough evidence is present.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial output can imply that activity cap validation was applied, but the free engine does not implement cap validation.

Mitigation: Independently verify capped payable amounts before collection, approval, or accounting decisions.

Risk: The checker only covers the free-tier checks and may omit policy, tax, pricing, negative-value, or threshold issues.

Mitigation: Review the listed withheld and out-of-scope checks before relying on a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/promo-subsidy-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON findings with summary fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input returns missing fields instead of a conclusion.]

## Skill Version(s):

1.0.31 (source: server evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
