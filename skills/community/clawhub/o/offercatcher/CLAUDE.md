# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

OfferCatcher 是一个招聘邮件提醒同步工具，配合 OpenClaw 使用。通过 Apple Mail 扫描邮件，OpenClaw LLM 解析内容，Apple Reminders 创建提醒。

## 架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  scan-only  │ --> │ OpenClaw    │ --> │ apply-events│
│  获取邮件   │     │ LLM 解析    │     │ 创建提醒    │
└─────────────┘     └─────────────┘     └─────────────┘
```

**不使用正则匹配**：邮件解析由 OpenClaw LLM 完成，能适应各种格式的邮件。

## 常用命令

### 扫描邮件
```bash
python3 scripts/recruiting_sync.py --scan-only
```
返回原始邮件 JSON，供 OpenClaw LLM 解析。

### 应用 LLM 解析结果
```bash
python3 scripts/recruiting_sync.py --apply-events /tmp/events.json --dry-run
python3 scripts/recruiting_sync.py --apply-events /tmp/events.json
```

### 手工记录事件
```bash
python3 scripts/manual_event.py --title "重要事件" --due "2026-04-01 10:00" --notes "入口：https://example.com"
```

### 运行测试
```bash
python3 -m unittest discover tests/ -v
```

## 事件 JSON 格式

`apply-events` 接受的 JSON 格式：

```json
{
  "events": [
    {
      "id": "唯一标识",
      "company": "公司名称",
      "event_type": "interview | written_exam | assessment | authorization | deadline",
      "title": "提醒标题",
      "timing": {"start": "YYYY-MM-DD HH:MM", "end": "..."} 或 {"deadline": "..."},
      "role": "岗位名称",
      "link": "入口链接",
      "message_id": "原始邮件ID",
      "subject": "邮件主题",
      "sender": "发件人"
    }
  ]
}
```

## 核心文件

| 文件 | 作用 |
|------|------|
| `scripts/recruiting_sync.py` | 主脚本：scan-only / apply-events |
| `scripts/apple_reminders_bridge.py` | Apple Reminders 桥接 |
| `scripts/manual_event.py` | 手工记录事件 |
| `scripts/list_mail_sources.py` | 列出 Apple Mail 账户 |

## 配置文件

`~/.openclaw/offercatcher.yaml`：

```yaml
mail_account: 谷歌    # Apple Mail 账号名
days: 2               # 扫描天数
max_results: 60       # 最大邮件数
```

## 编码规范

- Python 3.11+，dataclass 定义数据结构
- 中文注释和输出
- 遵循 PEP 8