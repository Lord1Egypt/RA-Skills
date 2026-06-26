---
name: jike-word-query
description: 汉语词语查询。支持搜索词语、词语详情、随机词语、近义词查询和反义词查询，返回词语、拼音、解释、出处、例句、故事、用法、近义词和反义词。适用场景：用户说“查一下太公钓鱼是什么意思”“一言相关词语”“伟大的近义词”“高兴的反义词”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"📝","requires":{"bins":["python3"],"env":["JIKE_WORD_QUERY_KEY"]},"primaryEnv":"JIKE_WORD_QUERY_KEY"}}
---

# 汉语词语查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

支持：**词语搜索、词语详情、随机词语、近义词查询、反义词查询**。

## 前置配置

```bash
export JIKE_WORD_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/word_query.py search --keyword 一言 --page-size 5
python3 scripts/word_query.py detail --id 75046
python3 scripts/word_query.py random
python3 scripts/word_query.py similar --word 伟大
python3 scripts/word_query.py opposite --word 高兴
python3 scripts/word_query.py similar --word 伟大 --json
```

## AI 使用步骤

1. 用户按关键词找词语时，使用 `search` 子命令。
2. 用户问词语解释、出处、用法时，优先搜索获取 ID，再用 `detail` 查询详情。
3. 用户要求随机词语时，使用 `random` 子命令。
4. 用户问近义词时，使用 `similar` 子命令。
5. 用户问反义词时，使用 `opposite` 子命令。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `id` | 词语 ID |
| `word` | 词语 |
| `pinyin` | 拼音 |
| `explanation` | 解释 |
| `source_book` | 出处书名 |
| `source_text` | 出处原文 |
| `example_text` | 例句 |
| `usage` | 用法 |
| `similar` | 近义词 |
| `opposite` | 反义词 |

## 脚本位置

`scripts/word_query.py`
