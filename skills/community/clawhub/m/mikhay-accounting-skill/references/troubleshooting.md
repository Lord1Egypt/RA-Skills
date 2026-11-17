# 排错和恢复

校验和汇总脚本只读。导入和 `project_assets.py --write` 会写文件。出错时先停写。

回复必须包含三件事：错误类别、原因（字段、路径或脚本原文）、下一步。不要只回「已记录」「有问题」或「失败」。

脚本把硬错误打成 `INVALID:`，把可继续的问题打成 `warnings:`。警告也要告诉用户，不能当成没发生。

## 缺字段

现象：`record[n]: missing 类别`、`missing 子类`、`missing 账户`、`missing 备注`，快照则是 `missing 金额`。账户或类别为空时还会连带 `invalid 账户 ''`。

回复：列出缺的字段，保持这条不入库。向用户要缺的值。不要填空字符串，也不要默默选一个账户。

恢复：补全后再跑 `scripts/validate_ledger.py`。通过后再写入对应分片。

## 格式错误

现象：时间无法解析、`金额 must be a decimal number`、`currency must be a 3-letter code`、CSV 报 `duplicate column` 或列数不符。`金额=0` 是合法记录。正数支出、超过两位小数、裸标签、未知账户或未知类别通常是警告而不是 `INVALID`。

回复：指出文件、记录序号和错误值，并给出符合 `schema.md` 的改法。例如支出 `-35.00`、时间 `2026-06-01 12:10`。

恢复：只改指出的字段。日期超过上限（默认今天加 366 天）时先确认是不是写错年份，不要直接改系统日期。

## 校验失败

现象：进程退出码为 1，首行 `INVALID:`。常见原文：

- `pairid … expected 2 legs, found 1`
- `amounts are not equal` / `legs must have opposite directions`
- `金额 … != original_amount * fx_rate`
- `duplicate of record[n]` / `duplicate id`
- `退款 cannot use 类别 收入`

回复：原样引用第一条，必要时再引用其余几条。说明它违反哪条数据规则。不要在 `INVALID` 之后继续报花销或净资产。

恢复：按 `faq.md` 改记录，然后对同一路径重新校验。目录里的成对转账或 `refund_of` 要一次传入整个目录，单文件里找不到另一条时，`refund_of` 只警告「does not match a record id in this file」。

## 未知账户或类别（警告）

现象：`OK:` 后面有 `账户 … 不在账户表` 或 `类别 … 不在类别表`，退出码仍是 0。加 `--strict` 才会变成 `INVALID`。

回复：说明这只是配置缺失。把账户写进 `data/accounts.json`（`账户`、`别名`、`账户类型`），把类别写进 `data/categories.json`，再跑一次校验。

恢复：两个文件都可以用 `--accounts PATH` / `--categories PATH` 指定；不指定时脚本找账本旁边或工作目录下的 `data/`。配置文件允许带 BOM。

## 找不到文件

现象：路径不存在时，`validate_ledger.py` 会抛出 `FileNotFoundError`，而不是一行 `INVALID`。目录存在但没有账本文件时，标准错误是 `no ledger files found`。

回复：说清哪个路径不存在，以及脚本没有读到任何记录。不要把整段回溯当作唯一答复，也不要假装已经记完。

恢复：和用户确认路径。没有 `data/` 时，按 `storage.md` 创建空的 `data/ledger/`、`data/assets/`、`data/wishlist/`、`raw/`、`exports/`。只写入用户这次给出的记录。没有观察快照的账户会记在「未建立基线账户」，不要补一条假余额。

## 文件损坏

现象：`invalid JSON: Expecting property name …` 或类似解析错误。根因是文件损坏。空的 `schema_version`、`0.2.0` 和 `0.3.0` 都是接受的版本，不会因此报警。

回复：说明文件损坏，引用 `invalid JSON` 原文和行号。明确说先不要汇总。

恢复：不要覆盖坏文件。把它改名留档，例如 `2026-06.json.broken`。从 `raw/` 里的原始账单重新导入到新路径，或请用户拿出上一份完好分片。新文件必须先校验通过。要替换正式路径时先备份，再显式加上 `--overwrite`。没有该标志时，`import_ledger.py` 整批退出，不写文件。

`schema_version` 缺失或仍是 `0.2.0`、JSON 又能解析时，按旧账本继续汇总。不要为了版本号去改历史文件。

## 重试

可以重跑的只读命令：`validate_ledger.py`、`lint_ledger.py`、`summarize_ledger.py`、`summarize_tags.py`、`summarize_assets.py`、`summarize_items.py`、`analyze_wishlist.py`、`migrate_0_3.py`（不要加 `--apply`）、不带 `--write` 的 `project_assets.py`。输入没变时，结果应相同。

不要盲目重跑的写命令：

- `import_ledger.py` 会整文件写入目标路径，但默认拒绝覆盖。同一分片再导一次、且没有 `--overwrite` 时，整批退出，已有文件保持不变。见 `faq.md` 第 7 条。
- `project_assets.py --write` 会把推算结果写进资产文件。用户没点头之前不要加 `--write`。

重试规则：

1. 先改掉导致 `INVALID` 的输入，再重跑校验。
2. 同一条错误原样出现第二次就停，把原因和下一步交给用户，不要连跑。
3. 校验没通过时不要重试汇总来「碰碰运气」。
4. 脚本没有超时重试。本地文件读失败按「找不到文件」或「文件损坏」处理，不要换一套参数空转。

## 回复模板

```text
类别：校验失败
原因：data/ledger/2026/2026-06.json 的 pairid p4 只有 1 条，脚本要求 2 条。
下一步：补上支付宝那条 +200 的转账，或去掉 pairid 并写上 target_account。改完我会重新校验，通过后再报花销。
```
