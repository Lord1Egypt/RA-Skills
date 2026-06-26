---
name: jike-calendar-holiday-query
description: 支持查询某天是否放假或调休、某月假期、某年假期，返回假期名称、是否上班和调休目标日期。 适用场景：用户询问相关数据查询、日期查询或行情查询时使用。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🗓️","requires":{"bins":["python3"],"env":["JIKE_CALENDAR_HOLIDAY_QUERY_KEY"]},"primaryEnv":"JIKE_CALENDAR_HOLIDAY_QUERY_KEY"}}
---

# 节假日查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

## 前置配置

```bash
export JIKE_CALENDAR_HOLIDAY_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/calendar_holiday_query.py day --day 2021-06-14
python3 scripts/calendar_holiday_query.py month --month 2021-06
python3 scripts/calendar_holiday_query.py year --year 2021
python3 scripts/calendar_holiday_query.py day --day 2021-06-14 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/calendar/holiday/day?appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 用户问某天是否放假或调休时，使用 `day`。
2. 用户问某月或某年假期安排时，使用 `month` 或 `year`。
3. 返回日期、假期名称、放假/调休状态和调休目标日期。

## 脚本位置

`scripts/calendar_holiday_query.py`
