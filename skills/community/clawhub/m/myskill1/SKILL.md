---
name: us-treasury-tracker
description: 获取美国 10 年期国债利率（CNBC + Treasury.gov），写入 CSV，并生成极简日志
input: 无参数，自动获取当日数据
output: testdata/us_treasury_10y.csv
---

# US 10-Year Treasury Tracker

## 功能
- 从 CNBC 获取 10 年期国债利率
- 从 Treasury.gov 获取 10 年期国债利率
- 写入 CSV 文件
- 同一天重复调用时自动覆盖当天记录
- 每次执行生成一条极简日志

## 使用方式
```
/us-treasury-tracker
```

或
```
fetch treasury
```

## 输出文件
- 数据文件：`testdata/us_treasury_10y.csv`
- 日志文件：`skills/us-treasury-tracker/logs/fetch.log`

### CSV 列名
| 列名 | 说明 |
|------|------|
| Date | 日期（YYYY-MM-DD） |
| CNBC_10Y | CNBC 数据（%） |
| Treasury_10Y | Treasury.gov 数据（%） |

## 日志内容
每次执行追加一行极简日志，格式类似：

```text
2026-03-25 20:58:12 | overwrite | success | cnbc=4.334 treasury=4.31
```

其中：
- `append`：当天首次写入
- `overwrite`：当天已有数据，执行覆盖
- `success`：两个来源都抓取成功
- `partial`：部分来源成功
- `fail`：两个来源都失败

## 依赖
- Python 3
- requests
- beautifulsoup4

## 手动运行
```bash
cd skills/us-treasury-tracker/scripts
python3 fetch_treasury.py
```
