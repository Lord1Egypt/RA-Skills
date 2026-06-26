---
name: global-flight-search
description: 零配置即装即用｜全球航班一次搜出结果｜含座位余量和行李额度｜性价比标签智能推荐
tags: [航班查询, 航班搜索, 机票查询, 机票搜索, 订机票, 国际航班, 国内航班, 航班比价, 便宜机票]
tools:
  - name: search_flights
    description: 搜索全球航班，支持中文城市名直输
    primaryEnv: FLIGHT_PROXY_URL
    env:
      - name: FLIGHT_PROXY_URL
        description: 航班代理URL（自动配置，无需手动设置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: from_city
        type: string
        description: 出发城市，如"上海"、"东京"
        required: true
      - name: to_city
        type: string
        description: 到达城市，如"北京"、"大阪"
        required: true
      - name: from_date
        type: string
        description: 出发日期，格式YYYY-MM-DD
        required: true
  - name: search_airports
    description: 搜索机场/城市代码
    parameters:
      - name: keyword
        type: string
        description: 搜索关键词，如"浦东"、"大阪"
        required: true
  - name: check_flight_seats
    description: 查询航班座位余量
    parameters:
      - name: routing_id
        type: string
        description: 航班编号（从搜索结果获取）
        required: true
  - name: check_baggage_allowance
    description: 查询行李额度
    parameters:
      - name: routing_id
        type: string
        description: 航班编号（从搜索结果获取）
        required: true
---

# 全球航班查询与预订

零配置即装即用。基于全球航班数据，支持中文城市名直接输入。

## 能做什么

- **搜索航班**：出发城市→到达城市，支持中文城市名（如"上海→东京"）
- **搜索机场**：按关键词查找机场/城市代码
- **查询座位余量**：查看指定航线剩余座位，辅助判断购票时机
- **查询行李额度**：查看托运和随身行李政策，出行前确认

## 特色

- 100+中文城市名自动映射
- 80+航司代码中文显示
- 非民用机场自动过滤
- 直飞与中转分开展示，中转等待时间一目了然
- 性价比标签（≥80分🏆标记）
- 支持单程/往返，经济舱/商务舱/头等舱

## 不能做什么

- 无法直接预订机票（仅提供搜索和参考价格）
- 座位/行李查询需要先搜索航班获取编号
- 不支持多程/开口程

## 使用示例

1. "帮我查6月15日上海到北京的航班"
2. "搜索北京到大阪的商务舱机票"
3. "查一下浦东机场的代码"
4. "这个航班还有多少座位"
5. "查询行李额度"

## 注意事项

- 价格为参考价格，实际以预订页面为准
- 查询通过云端代理转发到全球航班数据平台，代理不存储用户数据
- 座位余量和行李额度查询需要先搜索航班获取routing_id

## 使用提示

- 中文城市名直接输入即可，无需手动输入机场代码
- 性价比标签≥80分的航班推荐优先考虑
- 直飞和中转分开展示，中转方案会标注等待时间
