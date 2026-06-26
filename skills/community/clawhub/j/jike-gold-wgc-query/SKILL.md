---
name: jike-gold-wgc-query
description: 查询世界黄金协会最新金价和历史金价，支持按日期、重量单位和币种筛选。 适用场景：用户询问相关数据查询、日期查询或行情查询时使用。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🌍","requires":{"bins":["python3"],"env":["JIKE_GOLD_WGC_QUERY_KEY"]},"primaryEnv":"JIKE_GOLD_WGC_QUERY_KEY"}}
---

# 国际实时金价 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

## 前置配置

```bash
export JIKE_GOLD_WGC_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/gold_wgc_query.py latest
python3 scripts/gold_wgc_query.py history --date 2025-04-28 --weight-unit grams,oz --currency cny,usd
python3 scripts/gold_wgc_query.py latest --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/gold/wgc/latest?appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 用户问最新国际金价时，使用 `latest`。
2. 用户问历史金价时，使用 `history`，可传日期、重量单位和币种。
3. 返回价格时间、更新时间、重量单位、币种和价格，并提示不构成投资建议。

## 脚本位置

`scripts/gold_wgc_query.py`
