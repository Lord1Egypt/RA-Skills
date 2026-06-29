---
name: marriott-hotel-booking
display_name: 万豪酒店预订
description: 搜索万豪集团旗下酒店并返回实时价格与预订链接，支持酒店详情查询和套餐优惠搜索，多旅游平台数据直连。
tags: [万豪, 喜来登, 威斯汀, 丽思卡尔顿, JW万豪, 万丽, 万枫, 瑞吉, 酒店预订, marriott]
tools:
  - name: search
    description: 搜索万豪集团旗下酒店，返回价格、星级、地址和预订链接
    parameters:
      - name: dest_name
        type: string
        description: 目的地城市/区域，如"上海""深圳""三亚"
        required: true
      - name: keyword
        type: string
        description: 关键词，如"JW""丽思卡尔顿""喜来登"
        required: false
      - name: max_price
        type: integer
        description: 最高价格/晚
        required: false
  - name: detail
    description: 查询某家万豪酒店的详细信息，包括周边交通、设施、房型等
    parameters:
      - name: shid
        type: string
        description: 酒店ID，从搜索结果获取
        required: false
      - name: hotel_name
        type: string
        description: 酒店名称（备选定位方式）
        required: false
  - name: packages
    description: 搜索万豪酒店套餐优惠（含早/连住/门票等打包产品）
    parameters:
      - name: keyword
        type: string
        description: 搜索关键词，如"上海""三亚度假"
        required: false
      - name: hotel_name
        type: string
        description: 酒店名称
        required: false
---

# 万豪酒店预订

搜索万豪集团旗下酒店（万豪/喜来登/JW/威斯汀/丽思卡尔顿/万丽/万枫/瑞吉等），返回真实价格和可预订链接，支持酒店详情和套餐优惠查询。

## 使用场景

- 用户明确要**搜索或预订万豪旗下品牌酒店**时使用
- 用户说「帮我找上海的万豪酒店」「深圳喜来登多少钱」「三亚JW万豪」等
- 不在用户仅提及品牌名但无搜索意图时触发（如「万豪的积分怎么用」不触发）

## 能做什么

- 搜索万豪旗下各品牌酒店，返回价格、星级、地址、附近地标和预订链接
- 查询某家万豪酒店的详情（周边交通/景点/设施/房型/政策）
- 搜索万豪酒店套餐优惠（含早/连住/门票等打包产品）

## 不能做什么

- 不支持非万豪旗下酒店搜索
- 不支持直接预订（提供预订链接，用户点击跳转）

## 🚫 绝对禁止

1. **禁止编造任何数据** — 酒店名称、价格、评分、星级必须100%来自脚本输出
2. **禁止添加脚本未返回的信息** — 脚本没返回评分就不能写评分
3. **禁止替换或筛选脚本结果** — AI不得二次过滤或替换脚本返回的酒店
4. **禁止美化数据** — 不得将¥1580改成¥980，不得添加虚假评分
5. **禁止省略预订链接** — 脚本返回的detailUrl必须完整展示

## 使用示例

1. 「上海有什么万豪酒店」→ search
2. 「上海800块以内的万豪」→ search + max_price
3. 「上海宝华万豪酒店怎么样」→ detail
4. 「万豪有什么优惠套餐」→ packages

## 注意事项

- 价格实时变动，以实际预订页面为准
- 数据来源为多旅游平台直连，不存储用户数据

## 数据流向

用户输入（城市/日期/关键词）→ 本技能脚本 → 代理服务 → 旅游平台API → 返回结果给用户。查询参数（城市、日期、酒店名）会发送到代理服务以获取实时数据。
