---
name: task-planner
---
description: |
  个人任务与行程管理助手，支持截止时间、提醒、修改、删除、重复任务、导出日历文档。
  用户可以用自然语言添加、修改、查询、完成或删除任务，无需记住ID。
  触发词：“记一下...”、“提醒我...”、“修改任务...”、“改签...”、“重复任务...”、“导出日历”、“生成本周行程表”、“我接下来要做什么”等。
author: liuxiaoying
version: 4.1.0
tags: ["task", "planner", "reminder", "schedule", "recurring", "document"]
triggers:
  - 提醒我
  - 记任务
  - 添加行程
  - 修改任务
  - 改签
  - 重复任务
  - 每天/每周/每月任务
  - 导出日历
  - 生成行程表
  - 检查提醒
requires: []
---

# Task Planner Skill (重复任务 + 导出日历文档)

## 功能说明
- 添加任务（标题、截止时间、提醒提前量、分类、优先级、额外信息）
- 添加**重复任务**：支持每日、每周、每月、每年，可指定结束条件
- 修改任务（自然语言匹配）
- 检查提醒
- 查看任务列表、按日期归纳总结
- 标记完成：如果是重复任务且未达到结束条件，自动生成下一次任务
- 删除任务
- **导出日历文档**：生成 Markdown 格式的日历表格，可打印为 PDF

## 导出日历文档

### 命令
用户可以说：
- “导出本周日历”
- “导出本月行程表”

AI 执行 `export_doc --range week/month`（默认 week），生成文件 `~/openclaw_calendar.md`。

## 微信语音输入处理

当用户通过微信语音消息与 OpenClaw 交互时，语音文件会先被转成文字，再进入本 Skill 的处理流程。

### 环境准备
- 设置环境变量 `OPENAI_API_KEY`
- 安装依赖：`pip install openai`

### 转写命令
```bash
python scripts/transcribe.py <音频文件路径>
5 * * * * /usr/bin/python3 ~/.openclaw/skills/task-planner/scripts/send_reminders.py
