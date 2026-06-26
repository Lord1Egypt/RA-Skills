---
name: hna-666-flight-checker
description: 查询海南航空 666Plus 权益可往返航班，自动遍历指定目的地
triggers:
  - 海航 666
  - 海南航空 plus
  - 海航权益
  - 海航航班查询
  - 666权益
version: 1.0.0
author: wd
tags: [海航, 航班查询, 权益卡, 自动化]
timeout: 600
# async: true          # 启用异步模式
---

# 海航 666Plus 权益往返航班查询助手

## 技能描述
自动查询从北京出发，使用 666Plus 权益卡，在指定日期范围内可往返的航班目的地。

## 触发条件
当用户提到以下内容时激活：
- 查询海航 666 权益航班
- 海航 plus 会员可出行目的地
- 北京出发 666 权益往返
- 海航权益卡航班查询

## 输入参数
| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| out_date | string | 是 | 去程日期，格式 YYYY-MM-DD | 2026-04-01 |
| ret_date | string | 是 | 返程日期，格式 YYYY-MM-DD | 2026-04-06 |

## 执行流程

### 1. 参数解析
从用户输入中提取日期，自动转换为 YYYYMMDD 格式

### 2. 执行查询
调用 Python 脚本：
```bash
cd /home/wd/.openclaw/skills/hna-666-flight-checker/scripts
~/.local/pipx/venvs/playwright/bin/python main.py --out {out_date_compact} --ret {ret_date_compact} --headless --debug
