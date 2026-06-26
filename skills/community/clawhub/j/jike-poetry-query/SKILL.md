---
name: jike-poetry-query
description: 唐诗宋词元曲查询。支持古诗词列表、详情、诗人查询、诗人详情、随机诗词、词牌信息、朝代列表、类别列表和体裁列表。适用场景：用户说“查相思这首诗”“杜甫简介”“随机来一首宋词”“水调歌头词牌是什么”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🏮","requires":{"bins":["python3"],"env":["JIKE_POETRY_QUERY_KEY"]},"primaryEnv":"JIKE_POETRY_QUERY_KEY"}}
---

# 唐诗宋词元曲查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

支持：**诗词搜索、诗词详情、诗人查询、诗人详情、随机诗词、词牌、朝代、类别、体裁**。

## 前置配置

```bash
export JIKE_POETRY_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/poetry_query.py search --name 相思 --page-size 5
python3 scripts/poetry_query.py detail --poetry-id 4
python3 scripts/poetry_query.py author --name 杜甫
python3 scripts/poetry_query.py author-detail --name 杜甫
python3 scripts/poetry_query.py random
python3 scripts/poetry_query.py cipai --name 水调歌头
python3 scripts/poetry_query.py dynasty
python3 scripts/poetry_query.py type
python3 scripts/poetry_query.py format
python3 scripts/poetry_query.py detail --poetry-id 4 --json
```

## AI 使用步骤

1. 用户按题名、作者、朝代、类别、体裁找诗词时，使用 `search`。
2. 用户问某首诗完整内容、译文、注释、赏析时，使用 `detail`。
3. 用户问诗人列表或诗人介绍时，使用 `author` 或 `author-detail`。
4. 用户要随机诗词、词牌、朝代/类别/体裁列表时，使用对应子命令。

## 脚本位置

`scripts/poetry_query.py`
