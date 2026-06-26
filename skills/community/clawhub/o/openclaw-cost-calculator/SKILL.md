---
name: openclaw-cost-calculator
version: 1.0.0
description: |
  OpenClaw 成本计算器 - 精确计算 OpenClaw + AI 模型的完整使用成本，对比不同模型组合，优化支出。适合：个人用户、企业用户、成本优化。
metadata:
  openclaw:
    emoji: "💰"
    version: 1.0.0
    requires:
      bins: ["curl"]
---

# OpenClaw 成本计算器

**目标**：精确计算 OpenClaw 使用的完整成本，帮你选择最优模型组合，省钱 50-90%。

---

## 🎯 快速计算

### 场景 1：个人日常使用

**需求**：每天 50 轮对话，每轮 1000 tokens 输入 + 500 tokens 输出

**计算**：
```
每日输入：50 × 1000 = 50,000 tokens
每日输出：50 × 500 = 25,000 tokens
每月使用：1,500,000 输入 + 750,000 输出

GPT-4o 成本：
  输入：1.5M × $2.5/1M = $3.75
  输出：0.75M × $10/1M = $7.50
  月费用：$11.25 ≈ ¥80

DeepSeek V3 成本：
  输入：1.5M × ¥1/1M = ¥1.5
  输出：0.75M × ¥2/1M = ¥1.5
  月费用：¥3 ≈ $0.42

节省：$10.83/月（96%）
```

### 场景 2：企业客服机器人

**需求**：每天 1000 次咨询，每次 800 tokens 输入 + 400 tokens 输出

**计算**：
```
每日输入：1000 × 800 = 800,000 tokens
每日输出：1000 × 400 = 400,000 tokens
每月使用：24M 输入 + 12M 输出

Claude 3.5 Sonnet 成本：
  输入：24M × $3/1M = $72
  输出：12M × $15/1M = $180
  月费用：$252 ≈ ¥1,800

GLM-4 成本：
  输入：24M × ¥10/1M = ¥240
  输出：12M × ¥10/1M = ¥120
  月费用：¥360 ≈ $50

节省：$202/月（80%）
```

### 场景 3：内容创作

**需求**：每天写 10 篇文章，每篇 3000 tokens 输入 + 2000 tokens 输出

**计算**：
```
每日输入：10 × 3000 = 30,000 tokens
每日输出：10 × 2000 = 20,000 tokens
每月使用：900K 输入 + 600K 输出

GPT-4o 成本：
  输入：0.9M × $2.5/1M = $2.25
  输出：0.6M × $10/1M = $6.00
  月费用：$8.25 ≈ ¥60

DeepSeek V3 成本：
  输入：0.9M × ¥1/1M = ¥0.9
  输出：0.6M × ¥2/1M = ¥1.2
  月费用：¥2.1 ≈ $0.30

节省：$7.95/月（96%）
```

---

## 📊 模型价格对比（2026-03）

| 模型 | 输入价格 | 输出价格 | 优势 | 劣势 |
|------|----------|----------|------|------|
| **DeepSeek V3** | ¥1/1M | ¥2/1M | 最便宜，中文强 | 需要国内网络 |
| **GLM-4** | ¥10/1M | ¥10/1M | 国产，稳定 | 价格中等 |
| **Qwen-Max** | ¥20/1M | ¥20/1M | 阿里云生态 | 价格偏高 |
| **GPT-4o-mini** | $0.15/1M | $0.6/1M | 性价比高 | 需要 VPN |
| **Claude 3 Haiku** | $0.25/1M | $1.25/1M | 快速便宜 | 需要 VPN |
| **GPT-4o** | $2.5/1M | $10/1M | 多模态强 | 价格贵 |
| **Claude 3.5 Sonnet** | $3/1M | $15/1M | 编程最强 | 价格贵 |

**省钱建议**：
- **日常使用**：DeepSeek V3（96% 节省）
- **企业应用**：GLM-4（稳定 + 合规）
- **编程任务**：Claude 3 Haiku（便宜 + 强）
- **复杂推理**：Claude 3.5 Sonnet（贵但强）

---

## 🔧 OpenClaw 配置优化

### 配置 1：成本优先（DeepSeek）

```yaml
models:
  default: deepseek-chat
  fallback: glm-4

providers:
  deepseek:
    apiKey: "sk-xxx"
    baseUrl: "https://api.deepseek.com/v1"

  zhipu:
    apiKey: "xxx"
    model: "glm-4"
```

**预期成本**：¥2-5/月（个人使用）

### 配置 2：性能优先（Claude + DeepSeek）

```yaml
models:
  default: claude-3-5-sonnet-20241022
  reasoning: deepseek-reasoner
  fallback: glm-4

providers:
  anthropic:
    apiKey: "sk-ant-xxx"

  deepseek:
    apiKey: "sk-xxx"

  zhipu:
    apiKey: "xxx"
```

**预期成本**：$5-15/月（混合使用）

### 配置 3：企业稳定（GLM-4）

```yaml
models:
  default: glm-4
  reasoning: glm-4-plus

providers:
  zhipu:
    apiKey: "xxx"
    model: "glm-4"
```

**预期成本**：¥50-200/月（企业使用）

---

## 💰 ROI 计算器

### 个人用户

**投入**：
- OpenClaw 安装：免费（DIY）或 ¥99（服务）
- 模型成本：¥2-10/月

**回报**：
- 时间节省：2-4 小时/天 × ¥100/小时 = ¥200-400/天
- 月回报：¥6000-12000
- **ROI：600-6000 倍**

### 企业用户

**投入**：
- OpenClaw 企业版：¥299（配置服务）
- 模型成本：¥50-500/月

**回报**：
- 客服自动化：节省 1 个客服 × ¥5000/月
- 文档自动化：节省 10 小时/周 × ¥100/小时 = ¥4000/月
- 月回报：¥9000+
- **ROI：18-180 倍**

---

## 🎯 优化建议

### 建议 1：混合使用

**策略**：
- 80% 简单任务 → DeepSeek V3（最便宜）
- 15% 中等任务 → GLM-4（稳定）
- 5% 复杂任务 → Claude 3.5 Sonnet（最强）

**预期节省**：70-90%

### 建议 2：缓存优化

**策略**：
- 启用 OpenClaw 上下文缓存
- 减少重复 prompt 成本
- 缓存命中可节省 90% 输入成本

### 建议 3：批量处理

**策略**：
- 合并多个小请求为一个大请求
- 减少 API 调用次数
- 批量处理可节省 20-30%

---

## 📋 成本监控

### 配置成本追踪

在 OpenClaw 配置中启用成本追踪：

```yaml
tracking:
  enabled: true
  alerts:
    daily: 10  # 日成本超过 ¥10 提醒
    monthly: 200  # 月成本超过 ¥200 提醒
```

### 查看成本报告

```
显示本月 OpenClaw 成本报告
```

OpenClaw 会返回：
- 总成本
- 按模型分类成本
- 按日期成本趋势
- 优化建议

---

## 💰 定价参考

- **基础计算器**：免费（本 Skill）
- **成本优化咨询**：¥299（一对一分析 + 配置优化）
- **企业成本审计**：¥999（完整审计 + 优化方案 + 实施指导）

---

## 🆘 获取帮助

- **OpenClaw 文档**：https://docs.openclaw.ai
- **OpenClaw 社区**：https://discord.com/invite/clawd
- **DeepSeek 文档**：https://platform.deepseek.com/docs
- **智谱 GLM 文档**：https://open.bigmodel.cn/dev/api

---

**创建时间**：2026-03-21
**作者**：OpenClaw 中文生态
**版本**：1.0.0