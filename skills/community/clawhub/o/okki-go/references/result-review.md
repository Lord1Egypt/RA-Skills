# Result Review

Read this for `L1_RESULT_REVIEW`: the user asks which displayed companies to contact, unlock, prioritize, avoid, or analyze.

## Preconditions

- A visible company batch exists, or the latest saved batch can be resolved.
- The user is asking about the displayed rows, not asking for a new search method.

If no batch exists and the user asks how to search, switch to `references/search-strategy.md`.

## Rules

- Reuse the current batch; do not run a new search by default.
- Do not browse the web unless the user explicitly asks for external research.
- Do not ask Product Context Lite questions in L1.
- Do not unlock companies. Recommendations never authorize paid actions.
- Keep the answer compact and in the user's language.

## Output Shape

Analysis groups are recommendations over the displayed batch. They must not replace, filter, renumber, or restate the script-owned result table as if they were the full result set.

Use this same overlay wording when L0 already showed the full table; do not require a separate user request before giving brief priority guidance after discovery.

Group rows into:

- priority unlock: strongest buyer-side fit and enough profile signals to justify a small paid validation batch.
- observe: plausible but incomplete fit, unclear role, or weaker profile signals.
- not recommended: supplier/peer/manufacturer role, unrelated profile, poor geography fit, or no buyer-side relationship.

Then add:

- one risk or uncertainty
- one next action
- paid confirmation boundary if the recommendation mentions unlock

Example:

```text
我会优先看 #2、#5、#8。

优先解锁:
- #2 ... 理由 ...

观察:
- #3 ... 风险 ...

暂不建议:
- #6 ... 原因 ...

如果要验证联系人，可以先解锁 #2、#5、#8。解锁每家公司通常消耗 1 积分，是否继续？
```

## Buyer-Side Fit

Prefer companies that plausibly buy, resell, install, integrate, maintain, retrofit, specify, or use the seller's offer.

Treat suppliers or peer manufacturers as observe/not recommended unless result fields show a customer-side role such as distributor, integrator, service provider, project buyer, reseller, installer, or operator.
