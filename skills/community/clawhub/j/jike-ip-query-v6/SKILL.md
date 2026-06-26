---
name: jike-ip-query-v6
description: IPv6地址查询。输入 IPv6 地址，实时查询国家、省份、城市、地区、运营商和 long_ip 数值。适用场景：用户说“查一下 240e:1f:1::1 是哪里的 IPv6”“这个 IPv6 属于哪个运营商”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python3"],"env":["JIKE_IP_QUERY_V6_KEY"]},"primaryEnv":"JIKE_IP_QUERY_V6_KEY"}}
---

# IPv6地址查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

输入 IPv6 地址，查询：**国家、省份、城市、地区、运营商、Long 数值**。

## 前置配置

```bash
export JIKE_IP_QUERY_V6_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/ip_query_v6.py 240e:1f:1::1
python3 scripts/ip_query_v6.py 240e:1f:1::1 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/ip/query/v6?ip=240e:1f:1::1&appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取 IPv6 地址。
2. 校验格式，IPv4 不调用本 Skill。
3. 执行 `python3 scripts/ip_query_v6.py <IPv6地址>`。
4. 返回国家、省份、城市、地区、运营商等信息。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `ip` | IPv6 地址 |
| `long_ip` | Long 数值 |
| `country` | 国家 |
| `province` | 省份 |
| `city` | 城市 |
| `area` | 地区 |
| `isp` | 运营商 |

## 脚本位置

`scripts/ip_query_v6.py`
