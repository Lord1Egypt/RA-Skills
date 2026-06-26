# 钱迹 CSV Schema

## Encoding

- **Character encoding**: UTF-8 with BOM (`EF BB BF` at byte 0)
- **Line ending**: `\n` (LF)
- **Trailing newline**: The file does NOT end with a trailing newline. The last data row ends at EOF with no `\n` after it.
- **Quoting**: RFC 4180 — fields containing commas, double quotes, or newlines are wrapped in double quotes. Embedded double quotes are escaped as `""`.

## Columns (18 fields)

| # | Column Name | Type | Required | Default | Notes |
|---|---|---|---|---|---|
| 1 | ID | string | Yes | Generated | `qj` + 13-digit ms timestamp + 6-digit random |
| 2 | 时间 | datetime | Yes | Now | Format: `YYYY-MM-DD HH:MM:SS` |
| 3 | 分类 | string | Yes | — | Primary category |
| 4 | 二级分类 | string | No | empty | Subcategory |
| 5 | 类型 | string | Yes | 支出 | One of: 支出, 收入, 转账, 退款 |
| 6 | 金额 | decimal | Yes | — | Always one decimal place (e.g. `14.0`, `3.96`) |
| 7 | 币种 | string | Yes | CNY | Always `CNY` |
| 8 | 账户1 | string | Yes | 工资卡 | Primary account |
| 9 | 账户2 | string | No | empty | Only for 转账 type |
| 10 | 备注 | string | No | empty | User's original input text |
| 11 | 已报销 | string | No | empty | |
| 12 | 手续费 | string | No | empty | |
| 13 | 优惠券 | string | No | empty | |
| 14 | 记账者 | string | Yes | 小明 | Customizable — set your own name |
| 15 | 账单标记 | string | No | empty | `不计收支` for balance adjustments only |
| 16 | 标签 | string | No | empty | |
| 17 | 账单图片 | string | No | empty | |
| 18 | 关联账单 | string | No | empty | |

## ID Generation Algorithm

```
ID = "qj" + MILLISECOND_TIMESTAMP + RANDOM_6_DIGITS
```

- `MILLISECOND_TIMESTAMP`: 13-digit Unix epoch in milliseconds (e.g. `1770045906717`)
- `RANDOM_6_DIGITS`: random integer in range `100000..199999`

Example: `qj1770045906717197829`

Total length: 2 + 13 + 6 = 21 characters.

When generating multiple entries at once, use the current timestamp for the first entry, then increment by 1 millisecond for each subsequent entry. Each entry gets its own random suffix.

## Amount Format

- Always display with at least one decimal place: `14.0`, `3.96`, `206.0`
- Python: `f"{amount:.1f}"` when the amount is a round number; otherwise preserve the original precision up to 2 decimals.
- In practice, use `f"{amount:.2f}".rstrip('0')` then ensure at least one decimal digit remains. Simplest: always format with one decimal if it's a whole number, or two decimals otherwise.

## Appending a Row

When appending a new row to the CSV:

1. The file currently does NOT end with `\n`, so prepend `\n` before the new row.
2. The new row itself should NOT have a trailing `\n`.
3. Use Python's `csv.writer` with `lineterminator='\n'` to generate the row string, then strip any trailing newline before appending.
