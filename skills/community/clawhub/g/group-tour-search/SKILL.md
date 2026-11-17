---
name: group-tour-search
display_name: 跟团游搜索与推荐
description: 搜索跟团游、私家团、纯玩线路，支持场景推荐（海边、古镇、亲子、山水等），并提供到目的地的火车票和机票查询，多旅游平台数据直连。暑期跟团游省心出行，精选线路一键搜索
tags: [跟团游, 度假推荐, 私家团, 纯玩团, 旅游线路]
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

# 跟团游搜索与推荐 — 说一句话就能找到完美线路

> 跟团游、私家团、纯玩线路全覆盖，场景智能推荐目的地，还能顺手查到目的地的火车票和机票。

🔥 **核心亮点：**
- **场景智能推荐** — 说"想去海边"就推荐三亚/厦门/北海等海边目的地线路
- **多品类覆盖** — 跟团游、私家团、纯玩团一网打尽
- **交通联动** — 查完线路直接查火车票和机票，不用换技能
- **价格透明** — 含价格、评分、景点、预订链接，一目了然
- **零配置** — 免申请Key，装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "三亚跟团游"
2. "想去海边玩，推荐个目的地"
3. "亲子游推荐，5天左右的"

## 核心能力

1. **跟团游搜索** — 输入目的地查跟团游/私家团/纯玩线路，含价格和预订链接
2. **场景推荐** — 说"想去海边""亲子游""古镇"等场景，自动匹配目的地和线路
3. **火车票查询** — 查到旅游目的地的高铁/火车票，含车次、票价、时刻
4. **机票查询** — 查到旅游目的地的航班，含航班号、价格、时刻
5. **多平台数据** — 直连多个旅游平台，线路丰富价格真实

## 能做什么

- 搜索全国及全球跟团游、私家团、纯玩线路
- 根据场景偏好智能推荐目的地和线路
- 查询到目的地的火车票和机票
- 返回价格、评分、包含景点、预订链接

## 不能做什么

- 不支持在线下单（提供预订链接跳转平台完成）
- 不支持定制游/自由行产品（专注跟团游品类）
- 不处理签证、保险等出行配套

## 使用提示

- 目的地明确时直接搜，不明确时用场景推荐
- 查到线路后可以直接查交通，规划完整行程
- 价格实时变动，以预订页面为准

## 🔗 搭配使用

- **酒店智能推荐** — 跟团之余自由活动时住哪里
- **景点智能推荐** — 自由行时间补充景点安排
- **旅行保险助手** — 跟团出游也建议买份保险

## 数据流向

用户输入（查询参数）→ 本技能脚本 → 代理服务 → 数据源API → 返回结果给用户。查询参数会发送到代理服务以获取实时数据，代理服务不存储用户数据。
