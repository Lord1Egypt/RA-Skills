---
name: meeting-minutes-assistant
description: 会议纪要助手。自动整理会议内容、提取关键讨论点、生成结构化会议纪要、识别待办事项并支持多渠道推送。当用户需要：记录会议、整理会议纪要、提取会议待办、生成会议摘要、将纪要推送到企业微信/飞书/钉钉时使用此技能。
---

# Meeting Minutes Assistant

会议纪要助手。自动整理会议记录，生成结构化纪要，提取待办事项。

## 核心能力

1. **内容整理** — 将零散会议记录组织成结构化文档
2. **摘要生成** — 提取关键讨论点和决议
3. **待办提取** — 自动识别指派的任务、截止时间、责任方
4. **多渠道推送** — 支持企业微信、飞书、钉钉推送

## 快速开始

### 整理会议记录

```bash
python3 scripts/extract_minutes.py --input ./meeting_notes.txt --output ./minutes.md
```

### 生成待办清单

```bash
python3 scripts/extract_todos.py --input ./minutes.md --format markdown
```

### 推送纪要

```bash
python3 scripts/push_minutes.py --file ./minutes.md --channel wecom
```

## 脚本说明

### scripts/extract_minutes.py

将原始会议记录整理为结构化纪要。

```bash
python3 scripts/extract_minutes.py --input <文件> --output <输出> [--format md|html]
```

### scripts/extract_todos.py

从会议纪要中提取待办事项。

```bash
python3 scripts/extract_todos.py --input <纪要文件> --format <md|json>
```

### scripts/push_minutes.py

推送会议纪要到指定渠道。

```bash
python3 scripts/push_minutes.py --file <文件> --channel <wecom|feishu|ddingtalk>
```

## 输出格式

```markdown
# 会议纪要 — [主题]

## 基本信息
- 时间：
- 参会人：
- 记录人：

## 议程
1.

## 讨论要点
-

## 决议
-

## 待办事项
| 事项 | 负责人 | 截止时间 | 状态 |
|------|--------|----------|------|
|      |        |          | 待领取 |

---
*由 meeting-minutes-assistant 生成*
```
