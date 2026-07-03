---
name: hotel-smart-pro
display_name: "酒店智能搜索"
description: 5项酒店搜索工具覆盖万豪品牌查询、酒店详情、套餐推荐、周边餐饮，基于飞猪与高德数据直连，零配置即装即用。暑期酒店预订智能筛选，快速匹配理想住所
version: 1.1.2
tags: [酒店搜索, 万豪酒店, 酒店推荐, 周边餐饮, 酒店套餐]
tools:
  - name: search_hotels
    description: 搜索国内酒店，返回实时价格和预订链接
    primaryEnv: FLIGGY_PROXY_URL
    env:
      - name: FLIGGY_PROXY_URL
        description: 飞猪代理URL（自动配置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置）
        required: false
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"三亚亚龙湾亲子酒店"
        required: true
  - name: search_marriott_hotels
    description: 搜索万豪集团旗下品牌酒店
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"上海万豪酒店"
        required: true
  - name: get_marriott_hotel_info
    description: 获取万豪酒店详细信息
    parameters:
      - name: params
        type: string
        description: 酒店名称或关键词
        required: true
  - name: search_marriott_packages
    description: 搜索万豪酒店套餐产品
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"三亚万豪含早套餐"
        required: true
  - name: search_food
    description: 搜索酒店周边餐饮美食
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"西湖附近美食"
        required: true
---

# 酒店智能搜索 — 万豪全系+国内酒店+周边美食，5个工具一站搞定

> 覆盖国内酒店搜索、万豪品牌搜索/详情/套餐、周边餐饮推荐，飞猪+高德双数据源，自然语言直达结果。

🔥 **核心亮点：**
- **万豪全系覆盖** — 万豪/喜来登/JW/威斯汀/丽思卡尔顿等品牌一站搜索
- **酒店+套餐** — 不仅搜酒店，还能直接查含早/含SPA等套餐优惠
- **周边餐饮** — 基于高德地图数据，搜酒店同时找附近美食
- **自然语言** — 直接说"三亚亚龙湾亲子酒店"即可
- **零配置** — 免申请Key，装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "三亚亚龙湾亲子酒店"
2. "上海JW万豪有什么含早套餐"
3. "西湖附近有什么好吃的"

## 核心能力

1. **国内酒店搜索** — 按城市/区域/品牌/关键词搜索，返回实时价格和预订链接
2. **万豪品牌搜索** — 覆盖万豪/喜来登/JW/威斯汀/丽思卡尔顿/W等全部品牌
3. **万豪酒店详情** — 获取设施、房型、政策、周边交通等完整信息
4. **万豪套餐搜索** — 搜索含餐/含SPA/含景点等组合优惠套餐
5. **周边餐饮搜索** — 基于高德地图搜索酒店/景点附近餐厅美食
6. **预订链接** — 每条结果附带预订链接，可直接跳转下单

## 能做什么

- 搜索国内各城市酒店，返回价格、评分、设施和预订链接
- 搜索万豪集团旗下所有品牌酒店
- 查询万豪酒店详细信息（设施/房型/政策/周边）
- 搜索万豪酒店套餐（含早/连住/门票等打包产品）
- 搜索酒店/景点周边餐厅美食

## 不能做什么

- 不支持海外酒店搜索
- 不支持在线下单（提供预订链接跳转平台完成）
- 万豪品牌以外的国际连锁酒店数据可能不完整

## 使用提示

- 万豪酒店先搜索获取名称，再查详情信息更完整
- 套餐通常比单订优惠10-30%，优先查看packages
- 美食搜索基于高德地图，自动定位周边
- 价格实时变动，以预订页面为准

## 🔗 搭配使用

- **酒店聪明订** — 多平台比价，找到最低价
- **景点智能推荐** — 住哪玩哪一站规划
- **高德地图全能版** — 导航到酒店、查周边设施

## 数据流向

用户输入 → 本技能 → 云端代理 → 飞猪/高德API → 返回结果。代理不存储用户数据。
