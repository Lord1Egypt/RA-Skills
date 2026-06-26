---
name: jike-tenwhy-query
description: 十万个为什么。支持按问题关键词搜索，也支持随机返回问题和答案。 适用场景：用户要求搜索、随机推荐或解释相关中文内容时使用。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"❓","requires":{"bins":["python3"],"env":["JIKE_TENWHY_QUERY_KEY"]},"primaryEnv":"JIKE_TENWHY_QUERY_KEY"}}
---

# 十万个为什么 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

支持：**关键词查询、随机返回**。

## 前置配置

```bash
export JIKE_TENWHY_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/tenwhy_query.py query --keyword 示例关键词
python3 scripts/tenwhy_query.py random
python3 scripts/tenwhy_query.py query --keyword 示例关键词 --json
```

## AI 使用步骤

1. 用户提供关键词时，使用 `query` 子命令。
2. 用户要求随机推荐时，使用 `random` 子命令。
3. 默认返回表格文本；需要结构化数据时追加 `--json`。

## 脚本位置

`scripts/tenwhy_query.py`
