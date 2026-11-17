---
name: pdd-selection
slug: pdd-selection-new
displayName: 拼多多精选
version: 1.0.0
display_name: 拼多多精选
description: 拼多多商品搜索、详情查询和频道好货浏览三合一工具，支持百亿补贴/秒杀/销量榜等频道，返回优惠价格、优惠券和购买链接。夏日拼多多好物，精选高性价比商品
tags:
  - 拼多多搜索
  - 拼多多购物
  - 商品搜索
  - 优惠券
  - 便宜好货
tools:
  - name: search_goods
    description: 拼多多商品搜索，关键词搜索拼多多商品，支持筛选和排序
    env:
      - name: PROXY_URL
        description: 代理服务器地址（自动配置，无需手动设置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: keyword
        type: string
        description: 搜索关键词
        required: true
      - name: sort_type
        type: string
        description: 排序方式，可选：综合排序、价格升序、价格降序、销量排序、优惠券面额
        required: false
      - name: has_coupon
        type: boolean
        description: 仅显示有券商品
        required: false
      - name: price_min
        type: number
        description: 最低价格
        required: false
      - name: price_max
        type: number
        description: 最高价格
        required: false
      - name: page
        type: integer
        description: 页码，默认1
        required: false
      - name: page_size
        type: integer
        description: 每页数量，默认20
        required: false
  - name: get_goods_detail
    description: 拼多多商品详情，通过goods_sign获取商品完整信息
    parameters:
      - name: goods_sign
        type: string
        description: 商品签名ID
        required: true
  - name: explore_deals
    description: 拼多多逛好价，按频道浏览拼多多精选好货，涵盖百亿补贴、秒杀、销量榜等频道
    parameters:
      - name: channel
        type: string
        description: 频道名称，默认销量榜
        required: false
      - name: limit
        type: integer
        description: 返回数量，默认20
        required: false
---

# 拼多多精选
> 搜商品、看详情、逛频道，拼多多购物三合一

## 📌 简介
拼多多商品搜索、详情查询和频道好货浏览三合一工具。3项能力覆盖拼多多购物全流程：关键词搜索找商品、商品详情看完整信息、频道浏览逛百亿补贴/秒杀/销量榜等精选好货。

## ✨ 核心亮点
- ✅ **三合一**：搜索+详情+频道浏览，一个技能搞定拼多多购物全流程
- ✅ **智能搜索**：关键词搜索支持多种排序（综合/价格/销量/优惠券面额）
- ✅ **频道好货**：百亿补贴、秒杀、销量榜等频道精选好货，不用自己找
- ✅ **优惠券筛选**：仅看有券商品，领券下单更省钱
- ✅ **商品详情**：通过goods_sign获取完整信息，含价格、优惠券和购买链接

## 🚀 快速入门
| 你这样说 | 技能做什么 |
|---------|----------|
| "拼多多搜一下无线耳机" | 关键词搜索，返回匹配商品列表 |
| "拼多多百亿补贴有什么好货" | 频道浏览，返回百亿补贴精选 |
| "这个商品详情帮我看看" | 通过goods_sign获取完整商品详情 |

## 🔧 核心能力
1. **商品搜索**：关键词搜索拼多多商品，支持综合/价格/销量/优惠券多种排序
2. **价格筛选**：设置最低/最高价格，锁定预算
3. **优惠券筛选**：has_coupon=true仅显示有券商品
4. **商品详情**：通过goods_sign获取商品完整信息（价格、优惠券、购买链接）
5. **频道浏览**：按频道浏览精选好货（百亿补贴/秒杀/销量榜等）
6. **翻页浏览**：支持分页，每页默认20条

## ✅ 能做什么
- 关键词搜索拼多多商品
- 按价格/优惠券/销量筛选和排序
- 查看商品详情（含优惠券和购买链接）
- 按频道浏览精选好货

## ❌ 不能做什么
- 不能下单购买，只提供商品信息和购买链接
- 不能查询订单状态或物流信息
- 不能跨平台比价（需使用购物比价助手）

## 💡 使用提示
- 数据通过云端代理服务器安全转发至拼多多开放平台API获取商品数据，代理服务不存储用户个人信息和查询数据
1. sort_type选销量排序找爆款，选优惠券面额找大额券
2. has_coupon=true只看有券商品，找优惠更精准
3. explore_deals的channel选百亿补贴，价格通常最低
4. 先搜商品拿到goods_sign，再用get_goods_detail看详情
5. 拼多多的百亿补贴频道是平台补贴，价格优势明显

## 🔗 搭配使用
- [拼多多百亿补贴](https://clawhub.ai/cn-shopping/pdd-baiyi-proxy)：专业版百亿补贴浏览，568件精选+品类导览
- [拼多多实时热销榜](https://clawhub.ai/cn-shopping/pdd-hot-rank)：707件热销爆款，看大家都在买什么
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)：拼多多价 vs 京东淘宝，跨平台确认最低
