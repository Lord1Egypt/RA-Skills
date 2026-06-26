---
name: jike-petrol-query
description: 国内油价实时查询。按省份查询 92号汽油、95号汽油、98号汽油和0号柴油价格，也支持不传省份返回全部地区油价。适用场景：用户说“四川今天油价多少”“查一下广东95号汽油价格”“全国油价列表”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"⛽","requires":{"bins":["python3"],"env":["JIKE_PETROL_QUERY_KEY"]},"primaryEnv":"JIKE_PETROL_QUERY_KEY"}}
---

# 国内油价实时查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

支持查询：**92号汽油、95号汽油、98号汽油、0号柴油价格**。

## 前置配置

```bash
export JIKE_PETROL_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

### 查询指定省份

```bash
python3 scripts/petrol_query.py --province 四川
```

### 查询全部地区

```bash
python3 scripts/petrol_query.py
```

### JSON 输出

```bash
python3 scripts/petrol_query.py --province 四川 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/petrol/query?province=四川&appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取省份名称。
2. 如果用户问全国油价，不传 `--province`。
3. 执行 `python3 scripts/petrol_query.py [--province <省份>]`。
4. 返回 92/95/98 号汽油和 0 号柴油价格。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `date` | 日期 |
| `time` | 更新时间 |
| `province` | 省份 |
| `petrol_92` | 92号汽油价格 |
| `petrol_95` | 95号汽油价格 |
| `petrol_98` | 98号汽油价格 |
| `diesel_0` | 0号柴油价格 |

## 脚本位置

`scripts/petrol_query.py`
