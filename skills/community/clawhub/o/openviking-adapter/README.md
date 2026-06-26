# OpenViking 适配器

字节跳动开源 AI 记忆系统的 OpenClaw 适配实现。

## 核心功能

- **L0 灵魂层**: 100 token 核心身份摘要
- **L1 概述层**: 2000 token 重要记忆概述
- **L2 详情层**: 按需加载的完整记忆

## 效果

- 任务完成率: 35% → 52%
- Token 消耗降低: 83%

## 使用方法

### 1. 分析当前 Token 使用
```bash
openclaw tools call openviking-adapter analyze_token_usage
```

### 2. 生成三层记忆架构
```bash
openclaw tools call openviking-adapter optimize_memory_loading
```

### 3. 按需搜索记忆
```bash
openclaw tools call openviking-adapter search_relevant_memories '{"query": "binance 套利"}'
```

## 文件结构

优化后会生成:
```
~/.openclaw/workspace/memory_viking/
├── L0_soul.md          # 100 token 灵魂摘要
├── L1_overview.md      # 2000 token 记忆概述
└── L2_details/         # 原始详细记忆 (按需加载)
```

## 定价

- 每次调用: 0.5 USDT
- 支付方式: SkillPay (Crypto)

## 来源

基于字节跳动 OpenViking 开源记忆系统:
https://github.com/bytedance/OpenViking