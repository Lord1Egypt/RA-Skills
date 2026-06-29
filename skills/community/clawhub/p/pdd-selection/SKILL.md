---
name: pdd-selection
display_name: "拼多多精选"
description: "零配置即装即用，提供拼多多商品搜索、商品详情和频道好货浏览3项工具，支持百亿补贴、秒杀、销量榜等频道，返回优惠价格、优惠券和购买链接。"
tags: [拼多多, 多多, 购物, 比价, 搜商品, 找好货, 百亿补贴, 秒杀, 拼多多好货, pdd, pinduoduo, shopping]
tools:
  - name: search_goods
    description: 拼多多商品搜索，关键词搜索拼多多商品，支持筛选和排序
    primaryEnv: PROXY_TOKEN
    env:
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

零配置即装即用，提供拼多多商品搜索、商品详情和频道好货浏览3项工具，基于拼多多官方数据。

## 能做什么

- **商品搜索**：关键词搜索拼多多商品，支持价格筛选、优惠券筛选、多种排序方式
- **商品详情**：通过goods_sign获取商品完整信息，含价格、优惠券等
- **频道浏览**：按频道浏览精选好货，涵盖百亿补贴、秒杀、销量榜等

## 不能做什么

- 不能下单购买，只提供商品信息和购买链接
- 不能查询订单状态或物流信息
- 不能跨平台比价（需使用购物比价助手）

## 使用示例

1. "拼多多搜一下无线耳机"
2. "拼多多百亿补贴有什么好货"
3. "这个商品详情帮我看看：goods_sign xxx"

## 注意事项

- 商品价格和优惠券实时变化，展示结果仅供参考
- 拼多多商品价格通常较低，但注意确认商品规格和品质
- **数据流向说明**：查询通过云端代理转发到拼多多官方API，代理不存储用户数据

## 使用提示

- sort_type选销量排序找爆款，选优惠券面额找大额券
- has_coupon=true只看有券商品，找优惠更精准
- explore_deals的channel选百亿补贴，价格通常最低
- 先搜商品拿到goods_sign，再用get_goods_detail看详情
- 拼多多的百亿补贴频道是平台补贴，价格优势明显
