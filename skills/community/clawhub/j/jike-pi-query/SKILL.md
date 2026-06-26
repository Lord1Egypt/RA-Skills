---
name: jike-pi-query
description: 支持查找圆周率指定位置开始的数字，也支持查找指定数字在圆周率中的位置。 适用场景：用户询问相关数据查询、日期查询或行情查询时使用。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"π","requires":{"bins":["python3"],"env":["JIKE_PI_QUERY_KEY"]},"primaryEnv":"JIKE_PI_QUERY_KEY"}}
---

# 圆周率查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

## 前置配置

```bash
export JIKE_PI_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/pi_query.py find-number --start-location 1 --length 20
python3 scripts/pi_query.py find-location --find-number 14159
python3 scripts/pi_query.py find-location --find-number 14159 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/pi/find_number?appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 用户要查圆周率指定位置数字时，使用 `find-number`。
2. 用户要查某串数字在圆周率中出现位置时，使用 `find-location`。
3. 返回数字串、位置、左右上下文和周边数字。

## 脚本位置

`scripts/pi_query.py`
