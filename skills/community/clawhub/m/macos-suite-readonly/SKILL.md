---
name: macos-suite-readonly
description: "macOS 只读查询：Mail 未读、Calendar 日程、Notes 搜索、Stocks 行情（输出 JSON）。"
metadata: "{\"openclaw\":{\"os\":[\"darwin\"],\"requires\":{\"bins\":[\"python3\",\"osascript\"]}}}"
---

# macos-suite-readonly

面向 ClawHub 的“只读”macOS 查询技能：读取邮件未读、日程、备忘录搜索、股票行情。所有命令输出单个 JSON，适合 agent 解析。

## ⚠️ 权限

- 首次调用可能弹出系统权限提示（自动化/隐私）。
- 若系统拒绝自动化权限，命令会返回 `ok=false` 或 `warning`。

## 使用方式

```bash
python3 {baseDir}/scripts/main.py <command> key=value key=value ...
```

## Commands

### Mail

```bash
python3 {baseDir}/scripts/main.py mail.unread_count
python3 {baseDir}/scripts/main.py mail.unread_list limit=20
```

### Calendar

```bash
python3 {baseDir}/scripts/main.py calendar.today limit=50
python3 {baseDir}/scripts/main.py calendar.list start="2026-03-03 00:00:00" end="2026-03-03 23:59:59" limit=50
```

### Notes

```bash
python3 {baseDir}/scripts/main.py notes.folders
python3 {baseDir}/scripts/main.py notes.search query="购物" limit=10 folder="Notes"
```

### Stocks

```bash
python3 {baseDir}/scripts/main.py stocks.quote symbol=AAPL
python3 {baseDir}/scripts/main.py stocks.quote symbol=600519
python3 {baseDir}/scripts/main.py stocks.batch symbols="AAPL,600519,00700"
```

