---
name: hotel-smart-pro
description: 零配置即装即用，提供5项酒店搜索工具，支持万豪品牌查询、酒店详情、套餐推荐、周边餐饮搜索，基于飞猪与高德数据直连
tags: [酒店搜索, 万豪酒店, 酒店推荐, 周边餐饮, 飞猪旅行, 高德地图, hotel, marriott]
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

# 酒店智能搜索

零配置即装即用的酒店搜索技能，5项工具覆盖酒店搜索、万豪品牌搜索/详情/套餐、周边餐饮，飞猪+高德数据直连。

## 能做什么

- **酒店搜索**：自然语言描述需求，搜索国内酒店
- **万豪品牌搜索**：覆盖万豪/喜来登/JW/威斯汀/丽思卡尔顿等品牌
- **万豪酒店详情**：获取设施、房型、政策等完整信息
- **万豪套餐**：搜索含餐/含SPA/含景点等组合优惠
- **周边餐饮**：基于位置搜索附近餐厅美食

## 使用示例

1. "三亚亚龙湾亲子酒店"
2. "上海JW万豪"
3. "三亚丽思卡尔顿亲子套餐"
4. "西湖附近美食"

## 注意事项

- 价格实时变动，以实际预订页面为准
- 查询通过云端代理转发到飞猪旅行+高德地图API，代理不存储用户数据
