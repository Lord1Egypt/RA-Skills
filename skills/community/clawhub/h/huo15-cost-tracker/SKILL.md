---
name: huo15-cost-tracker
description: 火一五成本追踪器 - 追踪 AI API 使用量、Token 消耗和成本计算。支持 MiniMax、OpenAI 等模型。触发词：成本追踪、火一五成本追踪、火一五成本追踪器、Cost Tracker、花费了多少、token 统计。
dependencies:
  optional: ["huo15-memory-evolution"]
---

# 💰 火一五成本追踪器 (huo15-cost-tracker)

> **作者**: 火一五信息科技有限公司  
> **版本**: v1.1.0

---

## 一、简介

成本追踪器用于记录 AI API 调用统计，包括：
- Token 消耗（输入/输出）
- API 调用次数
- 成本计算
- 会话时长

### 核心功能

| 功能 | 说明 |
|------|------|
| 📊 **Token 统计** | 记录输入/输出 Token 数量 |
| 💵 **成本计算** | 基于模型定价计算 USD 成本 |
| 📈 **调用统计** | 记录 API 调用次数 |
| ⏱️ **时长追踪** | 记录会话/任务时长 |
| 📋 **报表生成** | 生成可视化成本报表 |

---

## 二、工作原理

```
API 调用 → 记录 Token → 计算成本 → 存储统计 → 生成报表
```

每次 API 调用时记录：
- 输入 Token 数量
- 输出 Token 数量
- 调用时间
- 模型名称
- 响应时长

---

## 三、使用方式

### 3.1 查看当前成本

```bash
cd ~/.openclaw/workspace/skills/huo15-cost-tracker
./scripts/report.sh
```

### 3.2 重置统计

```bash
./scripts/reset.sh
```

### 3.3 记录 API 调用

```bash
./scripts/track.sh record \
  --input-tokens 1000 \
  --output-tokens 500 \
  --model "MiniMax-M2.1" \
  --duration 1500
```

### 3.4 添加到 HEARTBEAT

在 HEARTBEAT.md 中添加定时报告：

```markdown
## 💰 成本检查（每30分钟）
./scripts/report.sh
```

---

## 四、配置说明

### 4.1 模型定价

配置文件：`config/pricing.json`

```json
{
  "MiniMax-M2.1": {
    "inputTokens": 0.01,
    "outputTokens": 0.01,
    "unit": "per 1M tokens"
  },
  "gpt-4o": {
    "inputTokens": 2.5,
    "outputTokens": 10,
    "unit": "per 1M tokens"
  }
}
```

### 4.2 报告格式

```bash
========================================
💰 成本追踪报表
========================================
会话: 2026-04-05 02:00
----------------------------------------
总 API 调用: 42 次
总 Input Tokens: 125,000
总 Output Tokens: 89,500
----------------------------------------
预估成本: $0.42 USD
----------------------------------------
模型使用分布:
  MiniMax-M2.1: 35 次 (83%)
  其他: 7 次 (17%)
----------------------------------------
最耗时调用: 3,200ms
平均响应时间: 850ms
----------------------------------------
```

---

## 五、成本阈值警告

当成本超过阈值时自动提醒：

```bash
# 设置警告阈值（默认 $1.00）
./scripts/track.sh set-threshold 1.0

# 查看当前阈值
./scripts/track.sh get-threshold
```

阈值配置在 `config/threshold.json`：

```json
{
  "thresholdUSD": 1.0,
  "alertEnabled": true,
  "alertChannel": "wecom"
}
```

---

## 六、定时报告

### 6.1 添加到 Cron

```bash
# 每小时报告
0 * * * * /Users/jobzhao/.openclaw/workspace/skills/huo15-cost-tracker/scripts/report.sh

# 每天报告（早上9点）
0 9 * * * /Users/jobzhao/.openclaw/workspace/skills/huo15-cost-tracker/scripts/daily-report.sh
```

### 6.2 每日报告功能

```bash
# 生成每日成本摘要
./scripts/daily-report.sh
```

输出：
```
📅 每日成本报告 - 2026-04-05
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
今日 API 调用: 42 次
今日 Token: 215,000
今日成本: $0.42 USD
━━━━━━━━━━━━━━━
较昨日: +15% 📈
```

---

## 七、脚本清单

| 脚本 | 功能 |
|------|------|
| `track.sh` | 记录 API 调用 |
| `report.sh` | 生成成本报表 |
| `reset.sh` | 重置统计数据 |
| `config.sh` | 配置管理 |

---

## 六、集成方式

### 6.1 集成到 API 调用层

在调用 LLM API 时自动记录：

```bash
# 调用 API 前
START_TIME=$(date +%s%3N)

# 调用 API...

# 调用 API 后
END_TIME=$(date +%s%3N)
DURATION=$((END_TIME - START_TIME))

# 记录
./scripts/track.sh record \
  --input-tokens $INPUT \
  --output-tokens $OUTPUT \
  --model "MiniMax-M2.1" \
  --duration $DURATION
```

### 6.2 集成到 Dream Agent

在 dream.sh 中添加成本追踪：

```bash
# Dream Agent 执行后
./scripts/track.sh record \
  --input-tokens $(cat /tmp/dream_input_tokens) \
  --output-tokens $(cat /tmp/dream_output_tokens) \
  --model "MiniMax-M2.1" \
  --duration $(cat /tmp/dream_duration)
```

---

## 七、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| **v1.1.0** | 2026-04-05 | 新增中文别名：火一五成本追踪，新增阈值警告，新增每日报告 |
| v1.0.1 | 2026-04-05 | 修复 shell 变量解析警告 |
| v1.0.0 | 2026-04-05 | 初始版本 |
