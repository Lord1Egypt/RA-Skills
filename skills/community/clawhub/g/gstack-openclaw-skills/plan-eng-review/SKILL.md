---
name: plan-eng-review
description: 工程经理视角的技术架构评审工具。锁定技术架构，评估实现方案，确保技术决策合理。
version: 1.0.0
author: Garry Tan (Original), OpenClaw Team
tags: [engineering, architecture, planning, review]
---

# Plan Engineering Review - 工程评审

> 转换自 gstack/plan-eng-review，专为 WorkBuddy/OpenClaw 优化

## 概述

从工程经理视角进行技术架构评审，锁定技术架构，评估实现方案，确保技术决策合理。

## 触发条件

当用户说以下内容时使用此技能：
- "engineering review"
- "技术评审"
- "架构审查"
- "实现方案"
- "技术决策"

## 核心评审内容

### 1. 架构设计
- 系统分层
- 模块边界
- 数据流设计
- API 设计

### 2. 技术选型
- 语言/框架选择
- 数据库选择
- 第三方服务
- 开源组件

### 3. 可扩展性
- 水平扩展能力
- 垂直扩展能力
- 性能目标

### 4. 安全性
- 认证授权
- 数据加密
- 漏洞防护

### 5. 可靠性
- 错误处理
- 容错机制
- 监控告警

### 6. 可维护性
- 代码组织
- 文档完整性
- 测试覆盖

## 评审要点

### 技术债务
- 识别潜在债务
- 权衡取舍
- 长期影响

### 风险评估
- 技术风险
- 进度风险
- 资源风险

### 替代方案
- 至少 2-3 个可选方案
- 优缺点对比
- 推荐方案

## 输出

生成工程评审报告：
- 架构图
- 技术决策记录
- 风险评估
- 实现计划

---

**注意**: 本技能是 gstack plan-eng-review 的 WorkBuddy/OpenClaw 适配版本。
