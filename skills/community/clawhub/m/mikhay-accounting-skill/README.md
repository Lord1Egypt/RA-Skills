[English](README.md) · [中文](README.zh-CN.md)

# Mikhay Accounting Skill

Skill version `0.4.2` (see `SKILL.md` frontmatter). Ledger `schema_version` is still `0.3.0`, because the record format stayed compatible. An unedited `0.2.0` book still validates, and its totals stay the same.

Install: `npx skills add MikhayEeer/mikhay-accounting-skill`

Homepage: https://github.com/MikhayEeer/mikhay-accounting-skill

License: MIT, copyright MikhayEeer. Full text in [LICENSE](LICENSE).

Chinese personal ledger workflow for CSV, JSON, and XLSX files. Agent instructions stay in Chinese in `SKILL.md`. Common mistakes: `references/faq.md`. Recovery: `references/troubleshooting.md`.

Display name: `Accounting|记账 - 资产管理/信用卡/预购清单/年月统计`.

## Privacy

This skill is for Chinese personal ledgers. Records, asset snapshots, and wishlists stay in local files under `data/`, `raw/`, and `exports/`. The scripts do not upload the ledger.

## AI native 记账和传统记账的区别

This is not another bookkeeping app. The books stay in local files, and the agent follows the scripts instead of a screen full of forms.

1. **The only entrance is the conversation.** Text, a voice transcript, and screenshots all go to the agent you already use. Reading a screenshot depends on whether that model has vision (VL). This skill does not do OCR and does not add a separate screenshot-import entry. After the model reads the image, the agent files each row with the categories in `categories.md`.
2. **Accounts and categories are the user's data.** The skill ships starter lists, but the agent should write the real accounts (with `别名`) to `data/accounts.json` and the real categories to `data/categories.json`. "微信", "建行", and "花呗" resolve to the canonical account names. An unknown account or category only warns; `validate_ledger.py --strict` makes it an error. When unsure, put `待确认` in the note and ask once, then persist the answer in the config file.
3. **Validation is the safety net.** After every write, run `validate_ledger.py` and `lint_ledger.py` on the shards you touched. Copy totals from the script output. The model does not add the numbers. The skill cannot install a hook. If those commands did not run, do not say the row was recorded.
4. **A budget is a question asked before the purchase.** There is no envelope spreadsheet. When you say you want to buy something, the agent checks the wishlist bucket, credit exposure, and the cooling-off period (`analyze_wishlist.py`).
5. **Reminders and market values are scheduled tasks you set yourself.** The skill only stores the dates: repayment days, renewal days, the end of a cooling-off period, and a missing fixed expense. It does not poll prices and it does not run a timer. A periodic reminder or a fresh market snapshot belongs on a scheduled task of the host agent, so this skill does not spend tokens in a loop.
6. **Local plain text.** JSON and CSV live under `data/`. Back up with git or a drive you choose. There is no cloud sync.
7. **Left out on purpose:** charts and dashboards, manual entry forms, in-app OCR, bank connections and automatic sync, price tracking and returns, full split transactions, shared ledgers, an envelope-budget screen, ads, and product recommendations.

Rows already stored as `收入/报销` stay valid and still count as income. `scripts/migrate_0_3.py` only prints a preview and refuses `--apply`. Whether to rewrite those rows is your decision. Tell the agent that; do not rewrite them on your own.

Money that is waiting to be reimbursed still counts as actual spending. When the cash arrives, edit the original row instead of adding a second one: a fully reimbursed item becomes `金额=0`, a partial one keeps the remaining amount, and an over-reimbursement turns the row into `收入` for the difference. Mark `报销状态=已报销` when useful. Only when the original row cannot be edited should you add a separate `报销` row with `reimburse_of`. The same rule covers refunds and AA: one event, one row, and `0` is a valid amount. There is no "expected actual spending" line.

Investment accounts are part of net worth. A market value exists only when you ask for a snapshot. Floating profit is printed from that snapshot and is not a forecast.

## Import and export

**Re-import can delete data.** `scripts/import_ledger.py` refuses to overwrite an existing ledger file unless you pass `--overwrite`. If any target path already exists, the whole batch aborts and nothing is written. The script checks `Path.exists()` before it writes. `--overwrite` replaces each target file; records that are not in the new bill are dropped from that file. Back up `data/` before you use the flag. The gate is enforced by the script, not only by asking first.

Import CSV or XLSX into standard JSON:

```bash
python scripts/import_ledger.py raw/bill.csv --output data/imported.json
```

Split by month:

```bash
python scripts/import_ledger.py raw/bill.csv --split-by-month --year-dirs --output data/ledger
```

Replace existing shards only after a backup:

```bash
python scripts/import_ledger.py raw/bill.csv --shard month --year-dirs --output data/ledger --overwrite
```

Export standard JSON to CSV:

```bash
python scripts/export_ledger.py data/ledger/2026/2026-06.json --output exports/2026/2026-06.csv
```

Preferred real ledger shards: `data/ledger/YYYY/YYYY-MM.json`. Day shards: `data/ledger/YYYY/YYYY-MM/YYYY-MM-DD.json`.

```bash
python scripts/import_ledger.py raw/bill.csv --shard day --year-dirs --output data/ledger
python scripts/import_ledger.py raw/bill.csv --shard month --year-dirs --output data/ledger
```

Shard keys use the file name (`os.path.basename`). The month key of `data/ledger/2026/2026-06.json` is `2026-06`. Do not slice the full path; that produces the wrong key `r/202`.

Validate:

```bash
python scripts/validate_ledger.py data/ledger/2026/2026-06.json
python scripts/validate_ledger.py data/ledger
```

## Spending and internal transfers

Totals come from scripts. Do not add them by hand. The scripts scan every shard you pass in.

```bash
python scripts/summarize_ledger.py data/ledger
python scripts/summarize_ledger.py data/ledger --buckets examples/buckets.sample.json
python scripts/summarize_tags.py data/ledger
```

Two bases:

- **花销 (spending):** gross expense minus refunds. A refund (`收支类型=退款` or `refund_of`) is not income and is not a new purchase. Reports show both gross and net.
- **内部转账 (internal transfers):** `转账` between accounts. A `pairid` pair is counted once. Transfers are not spending.

Tag namespaces are free-form: any letter-first `prefix:suffix` is valid (`trip:`, `event:`, `project:`, `pet:`). `summarize_tags.py` prints gross, net, per-day totals, and the category share on the same line.

Optional fields: `currency` (default is the configured base currency, `CNY`), `original_amount`, `fx_rate`, `cny_amount`. Headline totals use the base-currency `金额`; foreign-currency rows are also summed per currency in an original-amount section. New JSON files include `schema_version`. Older books that omit these fields still load.

## Net worth and credit cards

```bash
python scripts/summarize_assets.py data/assets/2026/2026-06.assets.json --cc-method A
python scripts/summarize_assets.py data/assets/2026/2026-06.assets.json --forecast --as-of 2026-06-15
python scripts/project_assets.py data/assets/assets.json data/ledger/2026/2026-06.json
```

Accounts are `included` or `excluded` (备查). Net worth is printed as 计入净资产 and 备查账户. Starter 备查 examples: Apple Card, 公积金, 助学贷款, 加密货币; change them in `data/accounts.json`.

## Accounts, categories, and aliases

Accounts and categories are configuration, not code. Every script reads these files next to the ledger or in the working directory, and every command also accepts `--accounts PATH` / `--categories PATH`.

```json
{
  "accounts": [
    {"账户": "招商银行", "别名": ["招行", "CMB"], "账户类型": "资产"},
    {"账户": "花呗", "别名": ["支付宝花呗"], "账户类型": "负债", "信用卡": true}
  ]
}
```

```json
{
  "categories": {"宠物": ["猫粮", "疫苗"]},
  "subcategory_aliases": {"猫食": "猫粮"}
}
```

`replace_defaults: true` drops the starter list, so the file is the complete definition. Validation only warns on values that are outside the configured catalogs; add `--strict` when a hard gate is wanted. Add `投资账户: true` to an account to make investment direction explicit. Alias history windows live in the same file as `{"名称", "起", "止"}` entries; there is no separate `aliases.json`.

`data/settings.json` changes the base currency and the redemption marker:

```json
{"base_currency": "CNY", "invest_out_subcategory": "赎回"}
```

Rows without `currency` use the base currency, and foreign-currency rows get their own original-amount totals. `data/import_rules.json` replaces the import keyword table, fallback pair, and source-account map; see `import_rules.md`.

Credit-card balances default to method A: latest snapshot plus records after that snapshot. Method B replays the card ledger from zero and ignores the snapshot. The report names the method.

`--forecast` prints each card's projected statement, repayment, and due date, plus the current-month cash flow. It does not guess a payday; record salary rows if you want an income line.

## Assets

Query total assets, liabilities, net worth, installments, and repayment reminders:

```bash
python scripts/summarize_assets.py data/assets/2026/2026-06.assets.json
```

New ledger records affect asset totals. Editing an asset snapshot directly should report the difference and ask before writing an adjustment. `project_assets.py --write` writes the inferred view only when you pass that flag.

## Wishlist

Pressure, suggestions, and priority for planned purchases:

```bash
python scripts/analyze_wishlist.py data/wishlist/2026/wishlist.json --ledger data/ledger/2026/2026-06.json --assets data/assets/2026/2026-06.assets.json
```

A wishlist item is not a ledger record. Write an `支出` only after the purchase happens.

## Maintainer packaging and publish

`tools/publish.py` publishes committed `HEAD` to ClawHub, SkillHub.cn, and ModelScope. It reads tokens from one file per platform under `~/.secrets/publishing/` (or environment variables) and never writes them into the repository or per-tool config files.

```bash
python tools/publish.py --dry-run
python tools/publish.py --platform clawhub
python tools/publish.py --platform skillhub
python tools/publish.py --platform modelscope
```

`tools/package_skill.py` is maintainer-only. It is not an end-user ledger command. ClawHub publish ignores `tools/` via `.clawhubignore`, and the archive itself omits `tools/` and `package_skill.py`.

```bash
python tools/package_skill.py
```

Output:

```text
dist/mikhay-accounting-skill.tar.gz
dist/mikhay-accounting-skill.zip
```

The archive includes the skill, reference docs, import rules, `scripts/`, fictional examples, both READMEs, and `LICENSE`. It does not include `VERSION`, `tests/`, `.github/`, `tools/`, `data/`, `raw/`, `exports/`, `.claude/`, or `.codex/`. `MANIFEST.json` uses the same version as `SKILL.md`. `.clawhubignore` also leaves out `tests/` and `.github/`, so a registry publish does not pack them either.

## Using the skill compared with not using it

This comparison used a local sample that is not in the repository: one local check, a monthly total, and a category top list (Claude Code, GLM-5.2). The times and token counts below are that session's order of magnitude, not the example files in this repo.

| | Without the skill (LLM only) | With the skill (scripts + short instructions) |
|---|---|---|
| Input tokens | Schema, categories, and rules pasted or recalled, about 2–4k tokens of rules plus about 15k of records | Read `SKILL.md`, then open schema, categories, or references only when needed |
| Reasoning tokens | Classify, sum, and alias each row; long output, easy to get wrong, about 8–15k output tokens | Almost no arithmetic; two Bash commands |
| Output tokens | Hand-written report, about 1–2k | Script result, about 300–500 tokens |
| Latency | One turn of 30s to over 1min, longer with correction rounds | Two Bash calls, about 3–8s |
| Accuracy | Sums and alias normalization often drift; a few hundred rows rarely match on the first try | Deterministic; matches the reconciliation file |
| Total tokens | About 25–35k | About 3–5k |

## Conclusion

- Tokens: the skill used about 5–8× fewer, mostly because the rules and the row-by-row arithmetic stay out of the prompt.
- Speed: about 5–10× faster, from two or three correction rounds down to one pass.
- Quality: the largest gap. Hand sums and alias normalization can miss by hundreds of yuan. The scripts are deterministic.

For ongoing bookkeeping (new records, monthly reports, exceptions), install the skill and follow: read the schema, run validate, run summarize, and report only the totals and warnings the scripts print. Tag totals, category shares, and net worth come from a full shard scan. Do not add them by hand.

Tests:

```bash
python -m pytest -q
```
