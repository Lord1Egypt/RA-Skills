---
name: meituan-travel-assistant
description: 零配置即装即用｜景点门票酒店机票一键查｜含预订链接和实时价格｜本地生活特价直达
tags: [美团旅行, 酒店查询, 机票查询, 火车票查询, 景点门票, 行程规划, 旅行助手, 出行, meituan, travel]
tools:
  - name: tool_meituan_travel_query
    description: 美团旅行综合查询，酒店/机票/火车票/景点门票/行程规划
    primaryEnv: MEITUAN_PROXY_URL
    env:
      - name: MEITUAN_PROXY_URL
        description: 美团代理URL（自动配置，无需手动设置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: city
        type: string
        description: 城市名，如"北京"、"上海"
        required: true
      - name: query
        type: string
        description: 自然语言查询，如"北京到上海的机票"、"杭州西湖附近酒店"
        required: true
---

# 美团旅行助手

零配置即装即用的美团旅行查询技能，酒店/机票/火车票/景点门票/行程规划一站式服务，数据覆盖全国300+城市。

## 能做什么

- **酒店查询**：按城市查酒店，含价格和预订链接
- **机票查询**：查航班价格和时刻
- **火车票查询**：查车次、票价、余票
- **景点门票**：查景点门票价格
- **行程规划**：智能推荐出行方案

## 不能做什么

- 不支持在线下单/支付，预订链接跳转美团APP或网页完成
- 部分小城市数据覆盖可能不完整，建议用大城市名查询

## 使用示例

1. "帮我查北京到上海的机票"
2. "杭州西湖附近500元以内的酒店"
3. "上海迪士尼门票多少钱"
4. "周末两天成都游玩攻略"
5. "广州到三亚的火车票"

## 注意事项

- 价格实时变动，以实际预订页面为准
- 查询通过云端代理转发到美团旅行API，代理不存储用户数据

## 使用提示

- 查完酒店 → 用高德打车技能生成打车链接前往
- 查完景点 → 用高德路线规划技能查怎么去
- 查完机票 → 用火车票比价技能对比价格
