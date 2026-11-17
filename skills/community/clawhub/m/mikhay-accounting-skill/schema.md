# Ledger Schema

Primary format: Chinese CSV or JSON.

## Main Record Fields

Use these 9 fields. Extra fields documented below are optional, so older ledgers stay valid:

- `时间`: `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`.
- `收支类型`: `支出`, `收入`, `还款`, `转账`, `退款`, `报销`, `投资`.
- `金额`: signed number. `0` is valid, for example a fully refunded or fully reimbursed item that is kept as one row.
- `类别`: top category.
- `子类`: second-level category.
- `账户`: one account enum.
- `备注`: short description.
- `tags`: optional tag text or list.
- `note`: optional extra note.

Existing records may miss `tags` or `note`; treat them as empty.

## JSON Shape

Preferred monthly file:

```json
{
  "schema_version": "0.3.0",
  "month": "2026-06",
  "records": []
}
```

Files written by the scripts include `schema_version` `0.3.0`. A missing `schema_version`, `0.2.0`, and `0.3.0` all validate with no version warning. Any other value warns and still loads. New fields below are optional, so an unedited 0.2.0 book stays valid and its totals stay the same.

A JSON list is also accepted and treated as records.

Preferred storage path: `data/ledger/YYYY/YYYY-MM.json`.

## Config Files

Two optional side files make the skill fit a real user. Both are read by every script that needs them, next to the ledger or in the working directory, or through `--accounts PATH` / `--categories PATH`:

- `data/accounts.json`: accounts, account `别名`, `账户类型`, `纳入`, and `信用卡`. Shape and rules are in `accounts.md`.
- `data/categories.json`: custom categories, category aliases, and subcategory aliases. Shape and rules are in `categories.md`.
- `data/settings.json`: `base_currency` (default `CNY`) and `invest_out_subcategory` (default `赎回`).
- `data/import_rules.json`: import keyword table, fallback pair, and source-account map. Shape is in `import_rules.md`.
- Alias history windows are part of `data/accounts.json` alias entries. There is no separate `data/aliases.json`.

`replace_defaults: true` in either file drops the starter list. Files may be UTF-8 with or without a BOM. Unknown accounts and unknown categories are warnings by default; `validate_ledger.py --strict` turns them into errors.

## Type Rules

- `支出`: 真实消费。
- `收入`: 真实收入。退款不是收入。
- `还款`: 还负债；不混入普通支出统计。
- `转账`: 账户间移动；不计入收入或支出。
- `退款`: 冲回一笔支出。首选做法是直接把原支出改小：全额退款改成 `0`，部分退款改成剩余金额，超过原支出的部分改成一条 `收入` 的差额。只有原记录无法改动时，才另写 `收支类型=退款`，可选 `refund_of` 指向原支出的 `id`。报表同时给出毛额和净额，退款不计入收入。
- `报销`: 报销到账。首选做法同样是直接改原支出：全额报销改成 `0`，部分报销改成剩余金额，多出来的部分改成 `收入` 的差额；这样一件事只有一条记录。需要保留原始金额时再另写 `报销` 行，金额为正，不计入收入，可选 `reimburse_of` 指向原 `支出` 的 `id`，指到原支出时金额冲回那个类别。
- `投资`: 现金和投资账户之间的移动。不进花销，不进收入。成对记录和转账一样，同一个 `pairid`，一正一负；只记得一边时写 `target_account=`。赎回方向相反。报表单列「投资净投入 = 投入 − 赎回」。

## Amount Sign Rules

- `支出`: 负数。
- `收入`: 正数。
- `还款`: 正数。
- `转账`: 旧的单边记录用正数。`pairid` 的两条腿一正一负。
- `退款`: 正数，表示钱退回来。
- `报销`: 正数，表示报销款回到原账户。
- `投资`: 成对记录一正一负。单边投入在现金账户用负数，单边赎回在现金账户用正数。
- `金额` 允许为 `0`，也允许 `支出` 为 `0` 后保持原类别。全额退款、全额报销或 AA 后净额为 0，都直接改原记录：金额改成 `0`，需要时把 `报销状态` 写成 `已报销`，不要新增第二条。
- 净额超过原支出时（例如 500 元机票报销 520 元），把这一条改成 `收支类型=收入`、`金额=20`，备注保留来源。退款、报销和 AA 同理，一件事只留一条记录。
- 统计展示时，`支出`、`还款`、`转账` 使用正数合计。实际花销 = 支出毛额 − 退款 − 已报销。待报销的钱仍算在实际花销里，到账并以任一种方式冲减之后才扣减。不另报「预计实际花销」。旧的 `收入/报销` 不改写，仍然算收入，校验只给警告。

## Accounts

Accounts are user data, not a closed enum. `data/accounts.json` defines the real accounts, their `别名`, `账户类型`, `纳入`, and `信用卡` flag. The starter list (建设银行, 工商银行, 招商银行, 微信钱包, 支付宝, 美团, 白条, 花呗, 美团月付, 抖音月付, plus 备查 examples Apple Card, 公积金, 助学贷款, 加密货币) only exists so a fresh install works out of the box. See `accounts.md` for the config shape and alias rules.

Unknown accounts warn by default. A custom account can be declared in `data/accounts.json`, in `account_policy`, or on a snapshot with `账户类型`.
## Optional Asset Snapshot

For account balance snapshots:

```json
{
  "asset_snapshots": [
    {"时间": "2026-06-30", "账户": "建设银行", "账户类型": "资产", "金额": 1000, "currency": "CNY", "note": ""},
    {"时间": "2026-06-30", "账户": "花呗", "账户类型": "负债", "金额": -500, "currency": "CNY", "note": ""}
  ]
}
```

Rules:

- `资产`账户余额通常为正数。
- `负债`账户余额通常为负数，统计时按绝对值计入总负债。
- 直接修改资产快照时，默认先询问是否创建差额记账项，不自动补 item。

## Optional Credit Accounts

For credit account debt and limits:

```json
{
  "credit_accounts": [
    {"账户": "花呗", "欠款": 500, "额度": 5000, "可用额度": 4500, "账单日": 1, "还款日": 10, "状态": "active", "note": ""}
  ]
}
```

`账户` must be a liability account.

`credit_policy.mode` is `debt_only` (default) or `with_limit`. A `credit_accounts` row may set `mode` to override the file. `debt_only` reports debt and the repayment day, and does not print empty limits. `with_limit` warns when `额度` is missing, and when `可用额度` differs from `额度 − 欠款` by more than 1.

Forecast does not invent a silent bill day or repayment day. A missing `账单日` is reported as assumed day 1, and a missing `还款日` as assumed day 10.

## Optional Installment Plans

For installment strategy:

```json
{
  "installment_plans": [
    {"id": "inst-001", "账户": "花呗", "本金": 1200, "总期数": 12, "已还期数": 3, "每期金额": 100, "下一还款日": "2026-07-10", "状态": "active", "note": ""}
  ]
}
```

## Optional Repayment Reminder

For reminders, use a separate JSON file if needed:

```json
{
  "repayment_reminders": [
    {"时间": "2026-07-10", "账户": "白条", "金额": 500, "状态": "待还", "installment_id": "", "note": ""}
  ]
}
```

## Asset Sync Rule

- `支出`: 资产账户减少；信贷账户负债增加。
- `收入`: 资产账户增加。
- `还款`: 付款账户减少；目标负债账户减少。目标账户写在 `note` 或 `备注`，如 `target_account=花呗`。
- `转账`: 来源账户减少；目标账户增加。目标账户同样用 `target_account=...`。
- `退款`: 原账户余额回升；信用卡欠款下降。退款不记成收入。
- `报销`: 原账户余额回升；不记成收入。到账时新增一条 `报销`，`reimburse_of` 指向原支出，并把原支出的 `报销状态` 改为 `已报销`。在那之前，`待报销` 仍算实际花销。
- `投资`: 和成对转账一样移动余额。投资账户用 `account_policy` 声明为资产且 `纳入=included`，计入净资产。市值只来自用户主动写入的 `asset_snapshots`，不查行情，也不做定时更新。有快照时才打印「浮动盈亏 = 快照市值 − 累计净投入」。

## Tags

Tags are namespaced, and the namespace is yours. Any letter-first `prefix:suffix` is valid, for example `trip:demo`, `event:demo`, `person:demo`, `nature:need`, `project:move`, or `pet:vaccine`. A record may carry more than one tag; each tag receives the full amount. Older bare tags such as `旅行` still load, with a warning.

`scripts/summarize_tags.py` is the only way to total tags. It reads every shard it is given.

## Refunds And Transfer Pairs

Optional record fields:

- `id`: stable id inside the validated file set.
- `refund_of`: id of the original `支出`.
- `reimburse_of`: id of the original `支出`. Only on `报销`.
- `报销状态`: on an `支出`, one of `待报销`, `已报销`, `不报销`. Missing means `不报销`.
- `预计报销`: amount still expected back. Missing means the whole expense. Used only to list 待报销, not to reduce 实际花销.
- `pairid`: shared id of the two transfer or investment legs.
- `target_account`: other account. `note` may still say `target_account=花呗`.

`scripts/migrate_0_3.py` only prints a preview of legacy `收入/报销` rows and investment keyword candidates. It does not accept `--apply`. Do not rewrite historical rows unless the user asks.

Optional `item_id` links a ledger row to a subscription or holding in `data/items/items.json`. It is not a tag, and it does not add a tag namespace.

## Subscriptions And Holdings

`data/items/items.json` is a side file (`schema_version` `0.3.0`):

```json
{
  "schema_version": "0.3.0",
  "subscriptions": [
    {"id": "sub-001", "名称": "某AI会员", "金额": 140, "currency": "CNY", "周期": "月", "续费日": "2026-11-03", "自动续费": true, "扣款账户": "招商银行", "可报销": true, "状态": "active", "note": ""}
  ],
  "holdings": [
    {"id": "item-001", "名称": "相机", "购入价": 5000, "购入日期": "2026-03-01", "估计残值": 3200, "估值日期": "2026-10-01", "可增值": false, "record_id": "", "状态": "持有", "note": ""}
  ]
}
```

- `周期`: `月`, `季`, `年`, `周`.
- Subscription `状态`: `active` or `已取消`. Holding `状态`: `持有`, `已卖出`, or `已送出`.
- `scripts/summarize_items.py` prints the monthly subscription equivalent, renewals due within 30 days, auto-renewed reimbursable subscriptions with no matching `报销`, holding purchase total, residual total, and cost per day.
- None of those totals are added to 总资产, 净资产, or 备查净值. `summarize_assets.py` prints one `备查物品` residual line at the end and does not add it.
- When a belonging is sold, write `收入/其他` for the proceeds and set the holding `状态` to `已卖出`. Do not treat the residual as cash until that happens.

A `pairid` group must contain exactly two `转账` rows, with equal absolute amounts, opposite signs, and different accounts. Validate a directory when the legs live in different shards.

## Currency

Base currency is `CNY` by default and is set with `data/settings.json` (`base_currency`). Rows without `currency` use the base currency. Optional columns:

- `currency`: 3-letter code, default is the base currency.
- `original_amount`: signed amount in `currency`.
- `fx_rate`: multiplier into the base currency. Base-currency rows use `1`.
- `cny_amount`: signed base-currency amount (legacy field name). It must match `金额`.

`金额` stays the signed base-currency amount used by every headline total. For a non-base row, `金额` must equal `original_amount * fx_rate` within 0.01. `summarize_ledger.py` also prints a per-currency section with original amounts.

## Account Inclusion

Accounts are `included` or `excluded` (备查). Excluded balances stay visible and stay out of headline net worth. Starter excluded accounts are `Apple Card`, `公积金`, `助学贷款`, and `加密货币`; change them in `data/accounts.json`, with `account_policy`, or with a snapshot field `纳入`.

```json
{
  "account_policy": [
    {"账户": "公积金", "账户类型": "资产", "纳入": "excluded"}
  ]
}
```

`纳入` accepts `included` or `excluded`. `备查: true` also means excluded.
