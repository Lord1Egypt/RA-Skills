---
name: openviking-adapter
description: 字节OpenViking记忆系统适配器 - 分层加载优化，Token降低83%
version: 1.0.0
author: partner
---

# OpenViking Adapter

字节跳动开源 AI 记忆系统的 OpenClaw 适配实现。

## 核心特性

- **三层记忆架构**: L0灵魂层 + L1概述层 + L2详情层
- **智能加载**: 按需检索，避免信息过载
- **Token优化**: 降低83%的Token消耗
- **效果提升**: 任务完成率35%→52%

## 工具功能

1. `analyze_token_usage` - 分析当前记忆系统的Token使用情况
2. `generate_l0_soul` - 生成100token核心身份摘要
3. `generate_l1_overview` - 生成2000token重要记忆概述
4. `search_relevant_memories` - 智能搜索相关记忆
5. `optimize_memory_loading` - 执行完整的优化流程

## 使用方法

1. 安装: `clawhub install openviking-adapter`
2. 分析: `openclaw tools call openviking-adapter analyze_token_usage`
3. 优化: `openclaw tools call openviking-adapter optimize_memory_loading`

## 定价

- 每次调用: 0.5 USDT

## 开源协议

基于字节跳动 OpenViking 开源项目