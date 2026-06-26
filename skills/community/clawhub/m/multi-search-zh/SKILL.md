---
name: multi-search-zh
description: "通过 AISA 在网页、学术、Tavily 与综合分析层做多源证据搜索，并输出置信度。触发条件：当用户需要由多个搜索来源支撑的综合结论，而不是一次单点搜索时使用。"
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
# 多源综合搜索

## 何时使用

- 通过 AISA 在网页、学术、Tavily 与综合分析层做多源证据搜索，并输出置信度。触发条件：当用户需要由多个搜索来源支撑的综合结论，而不是一次单点搜索时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 把多个搜索来源汇总成一个带置信度的综合答案。

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

- 研究 2026 年开源 coding agent 是否变强，并给出多来源依据。

## 说明

- 通过 Python 客户端的 multi-search 模式调用。
