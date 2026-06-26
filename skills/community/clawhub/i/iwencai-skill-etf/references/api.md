# ETF数据查询接口文档

## 接口概述

查询ETF相关金融数据，支持自然语言问句输入，返回相关金融数据结果。

## 基本信息

| 字段 | 值 |
|------|-----|
| 接口地址 | `IWENCAI_API_URL` |
| 请求方式 | POST |
| 认证方式 | API Key |

## 认证

请求头中需携带 API Key：

```
Authorization: Bearer {IWENCAI_API_KEY}
```

## 请求参数

### Headers

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Authorization | STRING | 是 | Bearer {IWENCAI_API_KEY} |
| Content-Type | STRING | 是 | application/json |

### Body

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| query | STRING | 是 | 用户问句，例如："沪深300ETF有哪些？" |
| source | STRING | 否 | 来源，默认值：test |
| page | STRING | 否 | 分页参数，默认值：1 |
| limit | STRING | 否 | 分页参数，默认值：10 |
| is_cache | STRING | 否 | 缓存参数，默认值：1 |

### 请求示例

```json
{
  "query": "沪深300ETF有哪些？",
  "source": "test",
  "page": "1",
  "limit": "10",
  "is_cache": "1"
}
```

## 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| datas | ARRAY | 金融数据列表，接口返回的金融数据数组 |

### 响应示例

```json
{
  "datas": [
    {
      "ETF代码": "510300.SH",
      "ETF简称": "华泰柏瑞沪深300ETF",
      "涨跌幅": 1.25
    },
    {
      "ETF代码": "159919.SZ",
      "ETF简称": "嘉实沪深300ETF",
      "涨跌幅": 1.18
    },
    {
      "ETF代码": "510180.SH",
      "ETF简称": "华安上证180ETF",
      "涨跌幅": 0.95
    }
  ]
}
```

## 调用示例

```python
import os
import urllib.request
import json

url = "IWENCAI_API_URL"
headers = {
    "Authorization": f"Bearer {os.environ['IWENCAI_API_KEY']}",
    "Content-Type": "application/json"
}
payload = {
    "query": "沪深300ETF有哪些？",
    "source": "test",
    "page": "1",
    "limit": "10",
    "is_cache": "1"
}

data = json.dumps(payload).encode("utf-8")
request = urllib.request.Request(url, data=data, headers=headers, method="POST")
response = urllib.request.urlopen(request, timeout=30)
result = json.loads(response.read().decode("utf-8"))
print(result.get("datas", []))
```

## 使用说明（Agent 参考）

- 当用户询问 **ETF筛选、ETF行情、ETF规模、ETF跟踪指数** 等相关问题时，调用本接口。
- 将用户的自然语言问题直接作为 `query` 参数传入。
- 返回的 `datas` 字段为对象数组，每个对象包含ETF代码(`ETF代码`)、ETF简称(`ETF简称`)、涨跌幅(`涨跌幅`)等字段，可直接拼接后回复用户。
- `source` `page` `limit` `is_cache` 均为可选参数，使用默认值即可。
- 环境变量 `IWENCAI_API_KEY` 为鉴权密钥，需提前配置。
