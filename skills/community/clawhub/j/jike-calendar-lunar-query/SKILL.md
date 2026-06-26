---
name: jike-calendar-lunar-query
description: 老黄历查询。输入阳历日期和时间，查询农历日期、黄历宜忌、黄黑道、吉神凶煞、生肖、星座、节气、喜神福神财神方位等信息。适用场景：用户说“查一下 2024-02-02 的老黄历”“今天宜忌是什么”“某天适合结婚搬家吗”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"📅","requires":{"bins":["python3"],"env":["JIKE_CALENDAR_LUNAR_QUERY_KEY"]},"primaryEnv":"JIKE_CALENDAR_LUNAR_QUERY_KEY"}}
---

# 老黄历查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

输入阳历日期和时间，查询：**农历日期、黄历宜忌、黄黑道、吉神凶煞、生肖、星座、节气、喜神/福神/财神方位**。

## 前置配置

```bash
export JIKE_CALENDAR_LUNAR_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/calendar_lunar_query.py --date 2024-02-02
python3 scripts/calendar_lunar_query.py --date 2024-02-02 --time 10:30:00
python3 scripts/calendar_lunar_query.py --date 2024-02-02 --time 10:30:00 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/calendar/lunar/detail?date=2024-02-02&time=10:30:00&appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取阳历日期，格式化为 `YYYY-MM-DD`。
2. 如果用户提供时间，格式化为 `HH:MM:SS`；未提供时默认 `00:00:00`。
3. 执行 `python3 scripts/calendar_lunar_query.py --date <日期> [--time <时间>]`。
4. 返回农历、宜忌、黄黑道、节气、神位和节日信息。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `solar_date` | 公历日期时间 |
| `solar_full_string` | 公历完整描述 |
| `lunar_string` | 农历日期 |
| `lunar_full_string` | 农历完整描述 |
| `lunar_day_yi` | 当日宜 |
| `lunar_day_ji` | 当日忌 |
| `lunar_day_tian_shen_type` | 黄道/黑道 |
| `lunar_day_tian_shen_luck` | 吉凶 |
| `lunar_day_position_xi` | 喜神方位 |
| `lunar_day_position_fu` | 福神方位 |
| `lunar_day_position_cai` | 财神方位 |

## 脚本位置

`scripts/calendar_lunar_query.py`
