---
name: issue-request-manager
description: 管理Issue Request的整个生命周期，从创建、跟踪到回复。支持多平台集成（GitHub, GitLab, Jira等），实时状态跟踪，自动化通知系统。
version: 1.0.0
author: clawdbot
tags:
  - project-management
  - issue-tracking
  - automation
---

# Issue Request Manager Skill

## 功能概述
本技能用于管理Issue Request的整个生命周期：从创建、跟踪到回复，提供完整的项目管理和问题跟踪解决方案。

## 核心功能
1. Issue Request创建与分类
2. Issue Request状态跟踪与监控
3. Issue Request回复与沟通
4. 通知与提醒机制

## 使用场景
- 项目管理
- 客户支持系统
- 开发缺陷跟踪
- 任务分配与跟进

## 技术特点
- 支持多平台集成（GitHub, GitLab, Jira等）
- 实时状态跟踪
- 自动化通知系统
- 可扩展的插件架构

## 快速开始
1. 创建新Issue Request：`create issue "描述"`
2. 跟踪Issue状态：`track issue #123`
3. 回复Issue：`reply to issue #123 "回复内容"`

## 命令参考
- `create issue "<标题>"` - 创建新问题
- `track issue #<编号>` - 跟踪指定问题
- `reply to issue #<编号> "<回复内容>"` - 回复问题
- `assign issue #<编号> to <用户>` - 分配问题给用户
- `set priority #<编号> to <级别>` - 设置问题优先级
- `close issue #<编号>` - 关闭问题