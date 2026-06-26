---
name: jike-surname-query
description: 百家姓查询。输入姓氏，查询姓氏起源、名人、迁徙分布等信息。 适用场景：用户询问相关传统文化、生活常识或配对资料时使用。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"📜","requires":{"bins":["python3"],"env":["JIKE_SURNAME_QUERY_KEY"]},"primaryEnv":"JIKE_SURNAME_QUERY_KEY"}}
---

# 百家姓查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

## 前置配置

```bash
export JIKE_SURNAME_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/surname_query.py --name 赵
python3 scripts/surname_query.py --name 欧阳 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/surname/query?name=赵&appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取查询参数。
2. 执行 `python3 scripts/surname_query.py` 并传入对应参数。
3. 默认返回中文文本；需要结构化处理时追加 `--json`。
4. 如果用户没有提供可选参数，可不传该参数，由接口按默认逻辑处理。

## 脚本位置

`scripts/surname_query.py`
