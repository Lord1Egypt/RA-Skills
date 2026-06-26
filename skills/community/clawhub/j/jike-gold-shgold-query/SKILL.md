---
name: jike-gold-shgold-query
description: 按日期查询上海黄金交易所历史行情，返回品种、开盘价、最高价、最低价、收盘价、涨跌幅和成交量等信息。 适用场景：用户询问相关数据查询、日期查询或行情查询时使用。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🥇","requires":{"bins":["python3"],"env":["JIKE_GOLD_SHGOLD_QUERY_KEY"]},"primaryEnv":"JIKE_GOLD_SHGOLD_QUERY_KEY"}}
---

# 上海黄金交易所行情 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

## 前置配置

```bash
export JIKE_GOLD_SHGOLD_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/gold_shgold_query.py --date 2024-05-20
python3 scripts/gold_shgold_query.py --date 2024-05-20 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/gold/shgold/history?appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取日期，格式化为 `YYYY-MM-DD`。
2. 执行 `python3 scripts/gold_shgold_query.py --date <日期>`。
3. 返回上海黄金交易所各品种行情，并提示不构成投资建议。

## 脚本位置

`scripts/gold_shgold_query.py`
