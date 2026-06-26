---
name: perplexity-research-zh
description: "通过 AISA 调用 Perplexity Sonar 模型生成带引用的深度研究答案。触发条件：当用户需要综合研究、对比分析或长篇引用答案，而不是原始链接列表时使用。"
author: aisa
version: "1.0.0"
license: Apache-2.0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  env:
    - AISA_API_KEY
  bins:
    - python3
metadata:
  openclaw:
    primaryEnv: AISA_API_KEY
    requires:
      env:
        - AISA_API_KEY
      bins:
        - python3
---
# Perplexity 深度研究

## 何时使用

- 通过 AISA 调用 Perplexity Sonar 模型生成带引用的深度研究答案。触发条件：当用户需要综合研究、对比分析或长篇引用答案，而不是原始链接列表时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 使用可配置的 Sonar 模型深度生成带引用的研究答案。

## 快速开始

```bash
export AISA_API_KEY="your-key"
```

## 运行方式

首选运行路径是仓库内置的 Python 客户端：

```bash
python3 scripts/search_client.py
```

## 示例请求

- 研究全球 AI 监管趋势，并返回带引用的总结。

## 说明

- 当综合结论比原始结果列表更重要时优先使用。
