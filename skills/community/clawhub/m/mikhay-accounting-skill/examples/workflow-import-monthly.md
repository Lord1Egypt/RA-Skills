# 工作流：导入账单、校验、出月报

范围是 2026-06 这一份账单。数字来自脚本，不是手算。

## 输入

`raw/2026/2026-06/bill.csv`：

```csv
时间,收支类型,金额,类别,子类,账户,备注
2026-06-01 08:30,支出,15,食品餐饮,早餐,微信钱包,豆浆
2026-06-02 12:10,支出,42,食品餐饮,午餐,花呗,盖饭
2026-06-03 09:00,退款,10,食品餐饮,午餐,花呗,退回盖饭
2026-06-04 18:00,转账,200,转账,个人转账,建设银行,转入支付宝
2026-06-05 10:00,收入,8000,收入,工资,建设银行,工资
```

若 `data/ledger/2026/2026-06.json` 已经存在，脚本会拒绝写入并整批退出，不会先写别的月份。先备份 `data/`。用户明确要替换时才加 `--overwrite`，该标志会整文件替换分片。

## 命令

```bash
python scripts/import_ledger.py raw/2026/2026-06/bill.csv --shard month --year-dirs --output data/ledger
python scripts/validate_ledger.py data/ledger/2026/2026-06.json
python scripts/summarize_ledger.py data/ledger/2026/2026-06.json
```

导入会把支出改成负数，退款保持正数。这条转账没有 `pairid`，也没有 `target_account`，所以校验能通过，但会警告。

## 输出

导入：

```text
wrote data/ledger/2026/2026-06.json records=5 shard=2026-06 warnings=1
```

校验：

```text
OK: data/ledger/2026/2026-06.json
records: 5
asset_snapshots: 0
credit_accounts: 0
installment_plans: 0
repayment_reminders: 0
warnings: 1
- record[4]: 转账 has neither pairid nor target_account
```

月报：

```text
# 记账统计: 2026-06.json
扫描文件: 1
分片(month): 2026-06

- 记录数: 5
- 收入: 8000.00
- 支出: 57.00
- 花销毛额: 57.00
- 退款: 10.00
- 花销净额: 47.00
- 还款: 0.00
- 转账: 200.00
- 内部转账: 200.00
- 结余(不含还款): 7953.00
- 现金流结余: 7953.00

## 双口径
- 花销口径: 毛额 57.00, 退款 10.00, 净额 47.00
- 内部转账口径: 200.00

## 花销按类别
- 食品餐饮: 47.00 (100.00%)
```

## 回复

2026-06 花销净额 47.00（毛额 57.00，退款 10.00），收入 8000.00。转账 200 没有配对账户，内部转账口径暂按单边 200.00 计，不计入花销。下一步是补上支付宝 `+200` 的另一条腿，或写上 `target_account=支付宝`，然后重新校验。
