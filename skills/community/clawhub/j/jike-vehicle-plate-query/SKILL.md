---
name: jike-vehicle-plate-query
description: 车牌号码归属地。输入车牌号码或至少前两位车牌前缀，查询车牌前缀、省份简称、省份和城市。适用场景：用户说“陕C 是哪里的车牌”“查一下陕C88888 归属地”“这个车牌属于哪个城市”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🚗","requires":{"bins":["python3"],"env":["JIKE_VEHICLE_PLATE_QUERY_KEY"]},"primaryEnv":"JIKE_VEHICLE_PLATE_QUERY_KEY"}}
---

# 车牌号码归属地 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

输入车牌号码或车牌前缀，查询：**车牌前缀、省份简称、省份、城市**。

## 前置配置

```bash
export JIKE_VEHICLE_PLATE_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/vehicle_plate_query.py 陕C88888
python3 scripts/vehicle_plate_query.py 陕C
python3 scripts/vehicle_plate_query.py 陕C88888 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/vehicle/plate/query?plate_number=陕C88888&appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取车牌号或前两位车牌前缀。
2. 如果用户只给省份简称但没有字母，提醒补充至少前两位。
3. 执行 `python3 scripts/vehicle_plate_query.py <车牌号>`。
4. 返回省份、城市和车牌前缀。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `plate_prefix` | 车牌前缀 |
| `province_abbr` | 省份简称 |
| `province` | 省份 |
| `city` | 城市 |

## 脚本位置

`scripts/vehicle_plate_query.py`
