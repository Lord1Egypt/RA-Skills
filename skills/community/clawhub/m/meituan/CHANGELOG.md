# Changelog

## 2.2.0

Release theme: turn Meituan into a clean Markdown-only public decision skill with stronger install trust and sharper order-value judgment.

What changed:
- sync the local package with the published 2.x public-decision direction
- add an explicit safety contract: no login, no order lookup, no account coupons, no cart mutation, no checkout, no payment
- strengthen checkout-reality math around fee stack, threshold gap, useful add-ons, ETA, and merchant trust
- add decision modes for merchant comparison, threshold checks, deal sanity checks, risk triage, and screenshot readouts
- add confidence-and-gaps output so missing live price, address, stock, or coupon fields are visible
- add `SKILL_EN.md` and `skill-card.md` for clearer installation and review context
- update package metadata to `MIT-0`, `harrylabsj`, and public-data/no-login positioning

Suggested one-line changelog:
- Ship a Markdown-only public Meituan decision skill with stronger checkout-reality math, confidence gaps, and no account-state package surface.

## 1.2.0

Release theme: 从基础美团说明升级为“这一单该不该点”的行动型决策。

What changed:
- 重写 skill 定位，默认输出直接动作建议
- 强化门槛优惠、真实到手价、配送时效、商家风险和退款判断
- 收紧 package、Clawhub、README 文案，突出“便宜和时效哪个更值”

Suggested one-line changelog:
- Upgraded Meituan into an action-first ordering decision skill focused on whether an order is truly worth placing now.

## 1.0.0

Release theme: 美团行动型外卖决策首发版。

What ships:
- 新增 Meituan skill
- 重点判断门槛优惠、真实到手价、配送时效、商家风险、退款 practicality
- 输出收敛到“这一单该不该点”
- 补齐 README、package、Clawhub 发布文案

Suggested one-line changelog:
- Launch Meituan, an action-first ordering decision skill that tells users whether a Meituan order is truly worth placing.
