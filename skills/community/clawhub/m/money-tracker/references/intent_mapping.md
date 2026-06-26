# money_tracker Intent Mapping

This reference maps common user requests to the current skill behavior.
It is a routing summary, not a replacement for `SKILL.md` or `commands.md`.

## Core Mapping

| User request example | Skill route | Primary command | Main result |
| --- | --- | --- | --- |
| `记账 我喝奶茶用了10元` | Add one expense entry | `record` | Saves one transaction, usually with today's date, inferred amount, inferred type, and either a matched or fallback category/account |
| `用支付宝记一笔午饭 25 元` | Add one expense entry with wallet | `record --account 支付宝` | Saves one transaction under the matched wallet currency |
| `这个月工资到账 5000` | Add one income entry | `record --type income` | Saves one income transaction |
| `把分类设置为日常、学习、电器` | Replace active categories | `set-categories --replace ...` | Replaces the active category set |
| `添加分类 旅行` | Add one or more categories | `set-categories ...` | Adds or re-enables categories without replacing the whole set |
| `显示分类` | List categories | `list-categories` | Returns active categories, or all categories with `--all` |
| `列出所有账户` | List wallet accounts | `list-accounts` | Returns active wallets such as `支付宝:CNY` or `银行卡:USD` |
| `添加账户 Wise:USD` | Add one wallet account | `set-accounts Wise:USD` | Adds or re-enables the wallet |
| `把 Wise:USD 改成 TravelCard:EUR` | Rename or change wallet currency | `update-account --name Wise:USD --new-name TravelCard --currency EUR` | Updates the wallet definition and rewrites linked entry and recurring snapshots |
| `删除账户 银行卡:EUR` | Deactivate one wallet | `delete-account --name 银行卡:EUR` | Deactivates the wallet without rewriting history |
| `显示所有账户余额` | Show current holdings by wallet and currency | `account-balances` | Returns per-wallet balances plus `totals_by_currency` |
| `我现在还有多少美元` | Show current holdings for one currency | `account-balances --currency USD` | Returns active USD wallet balances and grouped USD totals |
| `今天花了多少` | Day total report | `day-report --date YYYY-MM-DD` | Returns expense, income, net, breakdowns, and top category/account for that date |
| `这周花了多少` | ISO week report | `week-report --week YYYY-Www` or `week-report --date YYYY-MM-DD` | Returns weekly totals and breakdowns |
| `这个月花了多少` | Month report | `month-report --month YYYY-MM` | Returns monthly totals and breakdowns |
| `今年收入主要来自哪里` | Year report or analysis | `year-report --year YYYY` | Returns yearly totals, income/expense breakdowns, and top categories/accounts |
| `列出 2026-03-15 的账单` | Day detail query | `list-transactions --date 2026-03-15` | Returns entry list for that date |
| `列出这周的账单` | Week detail query | `list-transactions --week YYYY-Www` | Returns entry list for that ISO week |
| `列出这个月的账单` | Month detail query | `list-transactions --month YYYY-MM` | Returns entry list for that month |
| `列出 2026 年的账单` | Year detail query | `list-transactions --year 2026` | Returns entry list for that year |
| `展示出最新的10个账单` | Recent entry query | `recent-transactions --limit 10` | Returns the most recent entries across all dates |
| `显示最近的一笔账` | Latest entry query | `latest-entry` | Returns the single latest saved transaction |
| `修改一笔账 1 金额为12元，分类为学习` | Update one saved entry | `update-entry --id 1 ...` | Updates only the specified fields |
| `删除一笔账 3` | Delete one saved entry | `delete-entry --id 3` | Deletes the selected entry |
| `删除最近的一笔账` | Delete latest entry | `delete-latest-entry` | Deletes the newest saved entry |
| `添加周期性支出 每月 1 号交房租 3000 用银行卡` | Add recurring schedule | `add-recurring --frequency monthly --next-date ...` | Saves a recurring schedule entry |
| `列出所有周期性账单` | List recurring schedules | `list-recurring` or `list-recurring --all` | Returns active schedules, or all schedules with inactive ones included |
| `修改周期性账单 1 下次日期为 2026-05-01` | Update one recurring schedule | `update-recurring --id 1 --next-date 2026-05-01` | Updates the recurring schedule |
| `停用周期性账单 2` | Deactivate one recurring schedule | `update-recurring --id 2 --deactivate` or `delete-recurring --id 2` | Marks the schedule inactive |
| `重新启用周期性账单 2` | Reactivate one recurring schedule | `update-recurring --id 2 --activate` | Marks the schedule active again |

## Important Routing Rules

| Situation | Current behavior |
| --- | --- |
| User asks about current holdings such as `我现在还有多少美元` | Use `account-balances`, not a day/week/month/year report |
| User asks about a relative period such as `今天`, `这周`, `这个月`, or `今年` | Resolve it to an explicit date, ISO week, month, or year before calling the script |
| User omits the wallet account while recording | The skill may save the entry under `未指定账户` if it cannot safely match an active wallet |
| User omits the category while recording | The skill may save the entry under `未分类` if it cannot safely match an active category |
| User names an inactive or unknown wallet with strict validation | `--strict-account` should fail instead of silently guessing |
| User names an inactive or unknown category with strict validation | `--strict-category` should fail instead of silently guessing |
| One report period contains multiple currencies | Day/week/month/year report totals are raw stored amounts and do not apply FX conversion |
| User wants recurring schedules to become normal entries automatically | Not implemented; recurring items are schedules only |

## Useful Examples

| User says | Typical command shape |
| --- | --- |
| `记账 我喝奶茶用了10元` | `python "{baseDir}/scripts/bookkeeping.py" record --amount 10 --description 奶茶 ...` |
| `显示所有账户余额` | `python "{baseDir}/scripts/bookkeeping.py" account-balances` |
| `我现在还有多少美元` | `python "{baseDir}/scripts/bookkeeping.py" account-balances --currency USD` |
| `这周花了多少` | `python "{baseDir}/scripts/bookkeeping.py" week-report --week YYYY-Www` |
| `列出 2026-03-15 的账单` | `python "{baseDir}/scripts/bookkeeping.py" list-transactions --date 2026-03-15` |
| `展示出最新的10个账单` | `python "{baseDir}/scripts/bookkeeping.py" recent-transactions --limit 10` |
| `添加周期性支出 每月 1 号交房租 3000 用银行卡` | `python "{baseDir}/scripts/bookkeeping.py" add-recurring --frequency monthly --next-date 2026-04-01 ...` |
