---
name: myknowledge
version: "1.4.89"
events:
  - message:received
description: |
  MyKnowledge 自动检测 Hook（操作后告知用户）。
  当用户发送消息时，自动分析任务复杂度，
  对复杂任务自动创建知识库和记录需求，操作完成后告知用户。
---

# MyKnowledge Hook

## 功能

自动检测用户消息中的复杂任务，触发知识库创建和需求记录（操作后告知用户）。

## 触发条件

- 事件：`message:received`
- 角色：`user`
- 复杂度：检测到 3 个及以上关键词（避免日常对话误触发）

## 关键词列表

- 分析、统计、挖掘
- 开发、设计、调研
- 整理、清洗、项目

## 行为

1. 分析消息内容
2. 判断是否为复杂任务
3. 如果是，调用 MyKnowledge Skill 创建记录
4. 操作完成后告知用户（非无感知）
