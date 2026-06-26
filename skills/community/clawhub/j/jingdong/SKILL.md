---
name: jingdong
description: "Redirect: jingdong has been merged into jd-shopping. Use jd-shopping for JD.com search, review checks, price comparison, SKU selection, and safe cart preparation. Safe boundary: no login, no order submission, no payment."
---
# Jingdong Redirect

`jingdong` has been merged into the maintained `jd-shopping` skill.

Use `jd-shopping` for JD.com search, self-operated store checks, review analysis, price comparison, SKU selection, and cart preparation. Keep using this legacy skill only when the user explicitly asks for the old `jingdong` slug; immediately route them to install or use `jd-shopping`.

## Redirect Target

- Target skill: `jd-shopping`
- Reason: avoid two independent JD shopping products competing for the same user intent.
- User promise: product name or JD link -> self-operated/flagship checks, visible price, review risks, SKU advice, and cart-ready summary.
- Safety boundary: the agent never logs in for the user and never clicks checkout, final order submission, payment, bank, wallet, or payment-provider controls.

## Trigger Keywords

京东 / Jingdong / JD / JD.com / 京东自营 / 京东比价 / 查京东评价 / 京东购物

## Handoff Text

```text
这个旧入口已经合并到 `jd-shopping`。请安装或调用 `jd-shopping`，它覆盖京东搜索、查自营、看评论、比价、选规格和购物车准备；登录、结算、确认订单和支付仍由你手动完成。
```


## P1 Safety Boundaries

- Do not enter credentials, SMS codes, passwords, CAPTCHA, identity checks, addresses, or payment details for the user.
- Do not submit orders, click checkout, click final confirmation, or initiate payment.
- Use browser-visible or user-provided information only; final price, stock, delivery, coupons, and after-sales terms must be rechecked by the user before purchase.
