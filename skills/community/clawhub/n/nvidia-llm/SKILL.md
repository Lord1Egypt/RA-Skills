---
name: nvidia-llm
slug: nvidia-llm
version: 1.1.0
description: "英伟达 NIM 大模型智能路由 Skill — 50+ 模型自动路由+降级, 订阅VIP+微信支付+邀请奖励"
author: 用户
license: MIT
tags:
  - ai
  - llm
  - nvidia
  - nemotron
  - deepseek
  - qwen
  - mistral
  - router
  - circuit-breaker
  - auto-failover
categories:
  - ai-ml
  - developer-tools
topics:
  - nvidia
  - llm
  - api
  - routing
  - subscription
---

# nvidia-llm — 英伟达大模型智能路由 Skill

> 作者: 用户 | 版本: 1.1.0

一行代码调用 50+ 英伟达 NIM 前沿大模型，内置智能路由 + 自动降级 + 熔断器 + 订阅 VIP。

## 核心特性

- **智能路由** — 自动选择效果/速度最优的可用模型
- **自动降级** — 限流(429)/超时/服务不可用时自动切换备用模型
- **熔断器** — 连续失败自动熔断，探测恢复后自动启用
- **延迟追踪** — 实时统计各模型 P50/P95 延迟，优先使用最快的
- **并发请求** — 同时向多个模型发请求，取最快响应（Hedge 模式）
- **场景感知** — 编码/推理/创意/快速 自动匹配最优模型组
- **订阅系统** — 免费体验 + VIP 订阅 + 微信支付 + 邀请奖励

## 快速开始

```python
from nvidia_llm import chat, stream, AutoRouter

# 一行调用
print(chat("你好"))

# 编码场景
print(chat("写爬虫", scene="code"))

# 流式输出
for text in stream("讲个故事", scene="creative"):
    print(text, end="", flush=True)

# 智能路由器
router = AutoRouter(scene="code")
result = router.chat("写快速排序")
print(f"模型: {result['model_alias']}, 延迟: {result['latency']:.2f}s")
```

## CLI

```bash
nvidia-llm chat "你好"
nvidia-llm chat "写爬虫" --scene code
nvidia-llm stream "讲故事" --scene creative
nvidia-llm subscribe          # 微信扫码订阅
nvidia-llm invite DONGJIE8888 # 使用邀请码
nvidia-llm me                 # 会员状态
nvidia-llm status             # 模型健康
```

## 会员体系

| 等级 | 价格 | 限制 |
|------|------|------|
| 免费 | ¥0 | 5次/天 |
| 月卡 | ¥19/月 | 无限 |
| 年卡 | ¥99/年 | 无限 |
| 终身 | ¥299 | 永久无限 |
| 邀请VIP | 免费 | 邀请1人得30天 |

## 11 个场景

default / code / fast / reasoning / creative / chinese / multimodal / translate / finance / medical / edge

## 安装

```bash
pip install nvidia-llm
```

## 环境变量

```bash
export NVIDIA_API_KEY="your-key"
```
