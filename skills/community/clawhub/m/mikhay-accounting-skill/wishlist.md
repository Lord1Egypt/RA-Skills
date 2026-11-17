# Wishlist

Use this module for things the user wants to buy but has not bought yet.

## Storage

Preferred path:

```text
data/wishlist/YYYY/wishlist.json
```

## Shape

```json
{
  "items": [
    {
      "名称": "机械键盘",
      "预计金额": 399,
      "类型": "数码",
      "优先级": "P2",
      "目标日期": "2026-07-15",
      "可延期": true,
      "使用频率": "每日",
      "替代方案": "继续使用现有键盘",
      "状态": "想买",
      "note": ""
    }
  ]
}
```

## Rules

- Wishlist items are plans, not ledger records.
- Do not create a `records` item before the purchase actually happens.
- Analyze pressure with recent ledger surplus, net assets, debt, and repayment reminders.
- After purchase, create a normal `支出` record and set wishlist `状态` to `已购买`.
- For uncertain value judgments, output `观望` instead of forcing a buy/no-buy answer.
- `加入日期` defaults to the earliest date already in the file. Lint-style analysis warns until it is filled in.
- `冷静天数` defaults to 7. `P0` defaults to 0. Until that many days have passed, the suggestion is `观望（冷静期剩 N 天）`.
- `预计金额` is the estimate. `目标价` is the price the user is willing to pay. When the target is below the estimate, the reason includes `等降价`.
- `放弃原因` is required when `状态` is `放弃`. `record_id` should point at the `支出` when `状态` is `已购买`. Status values stay `想买`, `观望`, `计划购买`, `已购买`, and `放弃`.
- Top-level `budget_buckets` name a spending cap, for example `双十一`. Used amount is the sum of `支出` rows referenced by `record_id` on purchased items in that bucket. An active wish that costs more than the remainder is `不建议`.

## Command

```bash
python scripts/analyze_wishlist.py data/wishlist/2026/wishlist.json --ledger data/ledger/2026/2026-06.json --assets data/assets/2026/2026-06.assets.json
python scripts/analyze_wishlist.py data/wishlist/2026/wishlist.json --due --as-of 2026-10-19
```

`--due` prints wishes whose cooling-off period has ended, for a scheduled task the user sets up. The skill does not run that task itself.

Useful output:

- 是否建议购买
- 经济压力
- 建议优先级
- 建议购买时间
- 主要原因
