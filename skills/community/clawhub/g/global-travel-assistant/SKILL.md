---
name: global-travel-assistant
display_name: 全球旅游助手
description: 国内旅行一站式助手，飞猪+高德双引擎驱动，10个工具覆盖行程规划、火车票、机票、酒店、景点门票、极速搜索、万豪酒店、美食推荐、市内交通含打车，零配置即装即用。
tags: [国内旅行, 行程规划, 飞猪旅行, 酒店机票, 景点门票]
tools:
  - name: plan_trip
    description: AI行程规划，输入目的地和天数，返回推荐行程安排
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: search_train
    description: 火车票查询，输入出发地、目的地和日期，返回车次、余票和票价
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: search_flight
    description: 机票查询，输入出发城市、到达城市和日期，返回航班号、价格和时刻
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: search_hotel
    description: 酒店搜索，输入目的地和入住离店日期，返回酒店信息和预订链接
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: search_poi
    description: 景点门票查询，输入关键词或城市，返回景点信息和购票链接
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: search_fast
    description: 飞猪极速搜索，快速查询景点、酒店、门票等商品
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: search_marriott_hotel
    description: 万豪酒店搜索，搜索万豪集团旗下酒店含价格和预订链接
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: get_marriott_hotel_info
    description: 万豪酒店详情，获取酒店设施、评分、房型等详细信息
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: search_food
    description: 美食推荐，基于位置搜索周边餐厅，返回名称、评分、人均消费和地址
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: search_transport
    description: 市内交通，查询打车预估费用、公交地铁路线，并生成高德打车一键唤端链接
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
---

# 全球旅游助手 — 飞猪+高德双引擎，10个工具覆盖国内旅行全链路

> 从行程规划到订票订房到市内打车，飞猪8个工具+高德2个工具，零配置即装即用。

🔥 **核心亮点：**
- **双引擎驱动** — 飞猪旅行+高德地图，覆盖从规划到出行的完整链路
- **AI行程规划** — 输入目的地和天数，一键生成推荐行程
- **10个工具全覆盖** — 火车票/机票/酒店/景点/美食/交通/打车，应有尽有
- **高德打车** — 一键生成打车链接，打开高德地图直接叫车
- **零配置** — 免申请Key，装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "帮我规划3天成都游"
2. "北京到上海明天的高铁"
3. "杭州西湖附近酒店"

## 核心能力

1. **AI行程规划** — 输入目的地和天数，生成推荐行程安排
2. **火车票查询** — 输入出发地/目的地/日期，返回车次、余票和票价
3. **机票查询** — 输入城市对和日期，返回航班号、价格和时刻
4. **酒店搜索** — 输入目的地和入住离店日期，返回酒店信息和预订链接
5. **景点门票** — 查询景点信息和购票链接，支持关键词搜索
6. **美食推荐** — 基于位置搜索周边餐厅，返回评分、人均消费和地址
7. **万豪酒店** — 搜索万豪集团旗下酒店含详情和预订链接
8. **市内交通** — 打车预估+公交地铁路线+高德打车一键唤端

## 能做什么

- 规划国内旅行行程，覆盖200+城市
- 查询火车票、机票实时余票和价格
- 搜索酒店并获取预订链接
- 查询景点门票信息和购票链接
- 搜索周边美食餐厅
- 规划市内交通路线并生成打车链接

## 不能做什么

- 行程规划仅供参考需根据实际调整
- 不支持直接下单（提供预订链接跳转平台完成）
- 仅覆盖国内旅行，出境游请使用出境游旅行助手
- 打车费用为预估值，实际以网约车平台为准

## 使用提示

- 行程规划建议提供目的地和天数，越具体越好
- 火车票查询建议提供具体日期，余票实时变动以12306为准
- 酒店搜索建议提供入住和离店日期
- 市内交通结果自动生成高德打车链接，点击即可唤起高德地图APP

## 🔗 搭配使用

- **铁路12306火车票** — 专项火车票查询，更详细的余票信息
- **高德地图全能版** — 更全面的地图能力，含路线规划和POI搜索
- **景点智能推荐** — AI智能推荐景点，适合不知道去哪玩的场景

## 数据流向

飞猪工具通过飞猪SCF代理获取实时数据，高德工具通过高德SCF代理获取数据，代理服务不存储用户数据。
