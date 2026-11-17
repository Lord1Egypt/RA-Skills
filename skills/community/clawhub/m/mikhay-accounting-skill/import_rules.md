# Import Rules

Use `scripts/import_ledger.py` to convert third-party CSV/XLSX bills into the standard JSON ledger.

## Supported Inputs

- Standard Mikhay CSV: `时间, 收支类型, 金额, 类别, 子类, 账户, 备注, tags, note`
- Common CSV/XLSX exports from payment or bank tools, when columns can be mapped by name.

## Common Column Aliases

- 时间: `时间`, `交易时间`, `交易创建时间`, `付款时间`, `日期`, `交易日期`
- 收支类型: `收支类型`, `收/支`, `收支`, `类型`, `交易类型`
- 金额: `金额`, `金额(元)`, `金额（元）`, `交易金额`, `收入金额`, `支出金额`
- 类别: `类别`, `分类`, `一级分类`
- 子类: `子类`, `二级分类`
- 账户: `账户`, `支付方式`, `付款方式`, `收/付款方式`
- 备注: `备注`, `商品`, `商品说明`, `交易对方`, `商户`, `摘要`, `说明`

## Keyword Rules Config

`data/import_rules.json` (optional; `--import-rules PATH`) replaces the built-in keyword table:

```json
{
  "category_keywords": [
    {"类别": "宠物", "子类": "猫粮", "关键词": ["猫粮", "猫砂"]}
  ],
  "fallback": {"类别": "宠物", "子类": "其他"},
  "source_accounts": {"alipay": "支付宝", "wechat": "微信钱包"}
}
```

- `category_keywords` replaces the starter table. Set `append_defaults: true` to keep the starter rules as well.
- `fallback` is used when no rule matches. Both values must exist in `data/categories.json`; otherwise the first configured category is used.
- `source_accounts` maps a bill source token to a configured account. A token with no configured account falls back to the first included asset account.
- Classification never emits a category that is not in the configured catalog; it falls through to the fallback pair instead.

## Import Policy

- Preserve existing valid `类别/子类`.
- Normalize known aliases from `data/categories.json` and the built-in legacy aliases (see `categories.md`).
- Resolve `账户` through `data/accounts.json` aliases before the substring fallback, so 微信, 建行, 招行, and 花呗 land on the configured account names. Accounts and categories that are not configured still import; the validator only warns about them.
- If no confident category is found, use `购物消费/日用百货` and append `待确认分类` to `note`.
- Use signed amount rules from `schema.md`: `支出` is negative; `收入`, `还款`, `退款` are positive. Legacy single-sided `转账` is positive. `pairid` legs are opposite signs.
- A source value of `退款` becomes `收支类型=退款`, not income.
- Keep `currency`, `original_amount`, `fx_rate`, `cny_amount`, `pairid`, `refund_of`, and `target_account` when the source has them. Default currency is `CNY`.
- Do not overwrite existing ledger files. If any target path already exists, `import_ledger.py` aborts the whole batch and writes nothing unless `--overwrite` is set. Back up `data/` first. `--overwrite` replaces each target file and drops records that are not in the new bill. The script enforces this with a `Path.exists()` check before writing.

## Commands

Single JSON:

```bash
python scripts/import_ledger.py raw/bill.csv --output data/imported.json
```

Split by month:

```bash
python scripts/import_ledger.py raw/bill.csv --split-by-month --year-dirs --output data/ledger
python scripts/import_ledger.py raw/bill.csv --shard day --year-dirs --output data/ledger
```
