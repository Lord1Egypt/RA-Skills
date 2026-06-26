---
name: jike-character-query
description: 新华字典。支持拼音列表、部首列表、按拼音查汉字、按部首查汉字、汉字详情查询，返回汉字、拼音、部首、笔画、结构、繁体、异体字、同义词、反义词和形近字。适用场景：用户说“查一下好字怎么读”“口部有哪些汉字”“yī 这个拼音有哪些字”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🔤","requires":{"bins":["python3"],"env":["JIKE_CHARACTER_QUERY_KEY"]},"primaryEnv":"JIKE_CHARACTER_QUERY_KEY"}}
---

# 新华字典 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

支持：**拼音列表、部首列表、拼音查汉字、部首查汉字、汉字详情**。

## 前置配置

```bash
export JIKE_CHARACTER_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/character_query.py pinyin-list --limit 20
python3 scripts/character_query.py radicals-list --limit 20
python3 scripts/character_query.py pinyin --pinyin yī --limit 20
python3 scripts/character_query.py radicals --radicals 口 --limit 20
python3 scripts/character_query.py detail --char 好
python3 scripts/character_query.py detail --char 好 --json
```

## AI 使用步骤

1. 用户问拼音或部首列表时，使用 `pinyin-list` 或 `radicals-list`。
2. 用户按拼音查字时，使用 `pinyin`，注意接口需要带声调拼音，如 `yī`。
3. 用户按部首查字时，使用 `radicals`。
4. 用户问某个汉字详情时，使用 `detail`。
5. 返回拼音、部首、笔画、结构、繁体、同义词、反义词等信息。

## 脚本位置

`scripts/character_query.py`
