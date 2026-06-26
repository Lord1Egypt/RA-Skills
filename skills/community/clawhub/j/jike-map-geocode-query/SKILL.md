---
name: jike-map-geocode-query
description: 经纬度位置查询。输入经度、纬度和坐标系，查询完整地址、国家、省、市、区、乡镇和街道。适用场景：用户说“这个经纬度在哪里”“114.30394,34.79646 对应什么地址”“把 GPS 坐标反查成地址”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"📍","requires":{"bins":["python3"],"env":["JIKE_MAP_GEOCODE_QUERY_KEY"]},"primaryEnv":"JIKE_MAP_GEOCODE_QUERY_KEY"}}
---

# 经纬度位置查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

输入经纬度，查询：**完整地址、国家、省、市、区、乡镇、街道**。

## 前置配置

```bash
export JIKE_MAP_GEOCODE_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/map_geocode_query.py --lng 114.30394 --lat 34.79646
python3 scripts/map_geocode_query.py --lng 114.30394 --lat 34.79646 --coordinate-system gps --json
```

支持坐标系：

```text
gps、baidu、gaode、mapbar
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/map/geocode/query?lng=114.30394&lat=34.79646&coordinate_system=gps&appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取经度、纬度。
2. 判断坐标系；用户未说明时默认 `gps`。
3. 执行 `python3 scripts/map_geocode_query.py --lng <经度> --lat <纬度> --coordinate-system <坐标系>`。
4. 返回完整地址和行政区划层级。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `formatted_address` | 完整地址 |
| `country` | 国家 |
| `province` | 省 |
| `city` | 市 |
| `district` | 区 |
| `township` | 乡镇 |
| `street` | 街道 |

## 脚本位置

`scripts/map_geocode_query.py`
