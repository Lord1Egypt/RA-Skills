---
name: jike-calendar-foto-query
description: 输入阳历日期，查询佛历日期、完整说明、佛教节日、斋日、星宿和吉凶等信息。 适用场景：用户询问相关数据查询、日期查询或行情查询时使用。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🪷","requires":{"bins":["python3"],"env":["JIKE_CALENDAR_FOTO_QUERY_KEY"]},"primaryEnv":"JIKE_CALENDAR_FOTO_QUERY_KEY"}}
---

# 佛历查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

## 前置配置

```bash
export JIKE_CALENDAR_FOTO_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/calendar_foto_query.py --date 2024-01-18
python3 scripts/calendar_foto_query.py --date 2024-01-18 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/calendar/foto/detail?appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取阳历日期，格式化为 `YYYY-MM-DD`。
2. 执行 `python3 scripts/calendar_foto_query.py --date <日期>`。
3. 返回佛历日期、节日、斋日、星宿和吉凶信息。

## 脚本位置

`scripts/calendar_foto_query.py`
