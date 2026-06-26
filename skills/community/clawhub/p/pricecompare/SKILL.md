---
name: 购物省钱宝 - 京东/淘宝/拼多多优惠查询
description: 购物省钱宝，淘宝京东拼多多优惠券查询、商品比价、链接转链省钱助手。支持解析电商分享口令，多平台价格对比，找优惠券更省钱。Shop smarter: parse share codes, search products, convert links with coupons, compare prices across JD/Taobao/PDD.
version: 1.5.1
---

# PriceCompare · 购物省钱宝

> 京东/淘宝/拼多多优惠券查询、商品比价、口令解析、链接转链。Cross-platform price comparison, coupon discovery, and deal conversion for JD.com, Taobao, and Pinduoduo.

> 调用入口: `handle_message(message, keyword=None)` — message 用于路由判断，keyword 用于搜索/比价。API: `POST http://op.squirrel2.cn/api/v1/{endpoint}`。数据仅用于本次查询，发送至 op.squirrel2.cn 处理。

## 功能

### 1. 链接转链 `convert_link`
将商品链接转换为优惠链接。
```
触发条件: 用户发送了电商商品链接
调用签名: convert_link(url: str, platform: str|None = None) -> str
API:      POST /api/v1/convert  body: {"url": "...", "platform": "jd|taobao|pinduoduo"}

platform 可选，服务端自动识别域名:
  JD: item.jd.com, u.jd.com, 3.cn
  TB: item.taobao.com, detail.tmall.com, m.tb.cn, e.tb.cn
  PDD: mobile.yangkeduo.com, p.pinduoduo.com
```

### 2. 口令解析 `parse_share_content`
解析用户粘贴的电商分享内容（口令、短链接等）。服务端自动判断是否含有效口令。
```
触发条件: 用户发送了疑似分享口令的文本（非纯 URL）
调用签名: parse_share_content(content: str) -> str
API:      POST /api/v1/parse_share  body: {"content": "<用户原话>"}

注意: 服务端自动识别口令格式，无需客户端做正则检测。
      解析失败时返回错误信息，调用方应 fallback 到商品搜索。
```

### 3. 商品搜索 `search_goods`
按关键词搜索商品。不指定 platform 时自动走三平台比价。
```
触发条件: 用户想搜索/找某类商品
调用签名: search_goods(keyword: str, platform: str|None = None, page_size: int = 10) -> str
API:      POST /api/v1/search  body: {"platform": "jd|taobao|pinduoduo", "keyword": "...", "page_size": 10}

platform 为 None: 自动调用 compare_prices 三平台比价
page_size 最小值: 10（拼多多限制）
```

### 4. 多平台比价 `compare_prices`
同一关键词在京东/淘宝/拼多多三平台同时搜索，返回最低价。
```
触发条件: 用户想对比价格、找最便宜的平台
调用签名: compare_prices(keyword: str) -> str
API:      POST /api/v1/compare  body: {"keyword": "..."}
```

## Agent 调用指引

### 调用方式
```
handle_message(user_raw_message, keyword=extracted_product_name)
```

- **message**: 用户原始输入，用于路由判断（检测 URL）
- **keyword**: agent 从用户消息中提取的商品关键词，用于搜索/比价。不提供时回退到 message

### 路由决策

| 优先级 | 条件 | 调用 |
|:---:|------|------|
| 1 | message 含电商商品 URL | `convert_link(url)` |
| 2 | 其他文本 | 先 `parse_share_content(message)`，失败则 `search_goods(keyword or message)` |

### Agent 行为规范

1. 从用户消息中提取商品关键词传给 `keyword` 参数（如"帮我查一下iPhone 16的价格" → keyword="iPhone 16"）
2. 用户指定平台时传 `platform` 参数（jd/taobao/pinduoduo）
3. 展示链接时优先用超链接格式，如前端不支持则输出原始 URL
4. 函数返回的格式化内容直接呈现，无需重新组织

## 平台代码

| 中文 | 代码 | 主要域名 |
|------|:---:|------|
| 京东 | `jd` | item.jd.com, u.jd.com, 3.cn |
| 淘宝/天猫 | `taobao` | item.taobao.com, detail.tmall.com, m.tb.cn |
| 拼多多 | `pinduoduo` | mobile.yangkeduo.com, p.pinduoduo.com |

## 响应字段

| 字段 | 类型 | 含义 |
|------|------|------|
| title | string | 商品名称 |
| price | number | 券后价（元） |
| originalPrice | number | 原价（元） |
| couponInfo | string | 优惠券描述，如"满99减30" |
| couponAmount | number | 优惠券面值（元） |
| shopName | string | 店铺名称 |
| monthSales | string | 月销量 |
| link | string | 优惠购买链接 |
| platform | string | 平台代码 |

## 参数速查

| 参数 | 值 |
|------|-----|
| 推广链接有效期 | JD 15天 / TB 15天 / PDD 7天 |
| 口令有效期 | JD 7-15天 / TB 15-30天 |
| 搜索最小页大小 | 10 |

## 错误处理

- 口令过期/无效 → 告知用户重新获取
- 商品下架 → 告知不可购买，建议搜索同类
- 无搜索结果 → 建议放宽关键词
- parse_share 失败 → 自动 fallback 到商品搜索
- API 异常 → 提示服务暂时不可用
