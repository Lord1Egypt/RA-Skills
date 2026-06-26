---
name: openclaw-china-search-tips
description: |
  OpenClaw 国内联网搜索整合技能，整合多种免代理免费搜索API，帮你在国内不用翻墙也能稳定联网搜索。
  - 支持 volcengine-search / tavily-search / search-api / multi-search-engine 四种搜索渠道
  - 总结国内使用技巧，绕开代理问题
  - 自动 fallback，一个渠道失败自动切下一个
author: 你的名字 (based on 海绵宝宝 & 派大星 整理)
license: MIT
metadata:
  openclaw:
    category: search
    tags: ["china", "search", "no-proxy", "tips"]
---

# OpenClaw 国内联网搜索整合技巧

在中国大陆使用 OpenClaw 时，常常碰到网络问题、代理问题，没法正常联网搜索。这个技能整合了多种可用的免费搜索API，帮你**不用翻墙也能稳定搜索**。

## 整合渠道

| 渠道 | 免费额度 | 要求 | 特点 |
|------|----------|------|------|
| volcengine-search | 500次/月 | 火山方舟套餐 | 官方支持，中文准，带AI总结 |
| tavily-search | 1000次/月 | GitHub登录 | AI原生搜索，结构化结果 |
| search-api | 1000次/月 | GitHub登录 | Google搜索结果，稳定 |
| multi-search-engine | 不限 | 免APIKey | 直接爬搜索引擎，当兜底 |

## 使用技巧

### 1. GitHub登录技巧
在中国大陆直接打开 GitHub 很卡，可以用这个办法：
```
1. 先打开 GitHub 中文社区 (https://www.githubs.cn/)
2. 在中文社区登录你的GitHub账号
3. 登录完直接打开 GitHub 官网，登录状态已经带过去了
4. 再去 tavily/searchapi 官网选择 GitHub 登录，一次性成功
```

### 2. 搜索失败自动 fallback
代码已经封装好，一个渠道失败自动切下一个，不用你手动操作。

### 3. 不用命令行代理
只要你浏览器能上网，就能拿到 API Key，技能调用搜索API直接走域名，不需要命令行开代理。

## 安装要求
1. 你需要手动申请各个渠道的 API Key（都是免费有额度）
2. 配置环境变量即可使用

## 环境变量配置

```bash
export VOLC_SEARCH_API_KEY="..."   # 火山引擎搜索
export TAVILY_API_KEY="..."       # Tavily 搜索
export SEARCHAPI_API_KEY="..."    # SearchAPI 搜索
```

## 使用示例

```python
from china_search import search

# 自动搜索，自动 fallback
results = search("你的问题")
for r in results:
    print(r.title, r.url)
```

## 总结

核心经验：**碰到问题不要一根筋走到黑**，国内网络环境特殊，多准备几个渠道，一个不行就试下一个，总能搞定。

## 作者

整理：海绵宝宝 & 派大星 (OpenClaw 比奇堡团队)

