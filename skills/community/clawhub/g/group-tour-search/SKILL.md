---
name: group-tour-search
display_name: 跟团游搜索与推荐
description: 搜索跟团游、私家团、纯玩线路，支持场景推荐（海边、古镇、亲子、山水等），并提供到目的地的火车票和机票查询，多旅游平台数据直连。
tags: [跟团游, 旅游度假, 私家团, 纯玩, 小团, 火车票, 机票, travel, tour]
tools:
  - name: search_tour
    description: 搜索跟团游线路，支持目的地搜索和场景推荐
    parameters:
      - name: destination
        type: string
        description: 旅游目的地，如"三亚"、"丽江"、"张家界"
        required: false
      - name: query
        type: string
        description: 场景或需求描述，如"想去海边"、"亲子游"、"古镇"、"山水"
        required: false
  - name: search_train
    description: 查询到旅游目的地的火车票/高铁票
    parameters:
      - name: departure
        type: string
        description: 出发城市，如"上海"、"北京"
        required: true
      - name: destination
        type: string
        description: 旅游目的地，如"三亚"、"丽江"
        required: true
      - name: dep_date
        type: string
        description: 出发日期，如"明天"、"7月1号"、"2026-07-01"
        required: false
  - name: search_flight
    description: 查询到旅游目的地的航班机票
    parameters:
      - name: departure
        type: string
        description: 出发城市，如"上海"、"北京"
        required: true
      - name: destination
        type: string
        description: 旅游目的地，如"三亚"、"丽江"
        required: true
      - name: dep_date
        type: string
        description: 出发日期，如"明天"、"7月1号"、"2026-07-01"
        required: false
---

# 跟团游搜索与推荐

搜索跟团游、私家团、纯玩线路，支持场景智能推荐，并提供到目的地的火车票和机票查询。

## 能做什么

- **跟团游搜索**：输入目的地查跟团游/私家团/纯玩线路，含价格、评分、景点、预订链接
- **场景推荐**：说"想去海边""亲子游""古镇"等场景，自动推荐匹配目的地和线路
- **火车票查询**：查到旅游目的地的高铁/火车票，含车次、票价、时刻
- **机票查询**：查到旅游目的地的航班，含航班号、价格、时刻

## 使用示例

1. "三亚跟团游" → 搜三亚5条线路
2. "想去海边玩" → 推荐三亚/厦门/北海等海边目的地线路
3. "亲子游推荐" → 推荐适合亲子的跟团游
4. "上海到三亚的火车票" → 查火车/高铁
5. "北京飞丽江的机票" → 查航班

## 注意事项

- 价格实时变动，以实际预订页面为准
- 数据来源为多旅游平台直连，不存储用户数据
