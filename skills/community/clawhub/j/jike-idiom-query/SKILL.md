---
name: jike-idiom-query
description: 成语词典。支持搜索成语、成语详情、随机成语和成语接龙，返回成语、拼音、解释、出处、例句、故事、用法、近义词和反义词。适用场景：用户说“一丘之貉是什么意思”“搜一心相关成语”“来几个随机成语”“比翼双飞怎么接龙”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"📖","requires":{"bins":["python3"],"env":["JIKE_IDIOM_QUERY_KEY"]},"primaryEnv":"JIKE_IDIOM_QUERY_KEY"}}
---

# 成语词典 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

支持：**成语搜索、成语详情、随机成语、成语接龙**。

## 前置配置

```bash
export JIKE_IDIOM_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/idiom_query.py search --keyword 一心 --page-size 5
python3 scripts/idiom_query.py detail --id 320
python3 scripts/idiom_query.py random
python3 scripts/idiom_query.py last-word --keyword 比翼双飞 --size 5
python3 scripts/idiom_query.py search --keyword 一心 --json
```

## AI 使用步骤

1. 用户按关键词找成语时，使用 `search` 子命令。
2. 用户问成语解释、出处、用法时，优先搜索获取 ID，再用 `detail` 查询详情。
3. 用户要求随机成语时，使用 `random` 子命令。
4. 用户玩成语接龙时，使用 `last-word` 子命令。
5. 返回成语、拼音、解释、出处、近义词、反义词和接龙结果。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `id` | 成语 ID |
| `word` | 成语 |
| `pinyin` | 拼音 |
| `explanation` | 解释 |
| `source_book` | 出处书名 |
| `source_text` | 出处原文 |
| `example_text` | 例句 |
| `usage` | 用法 |
| `similar` | 近义词 |
| `opposite` | 反义词 |

## 脚本位置

`scripts/idiom_query.py`
