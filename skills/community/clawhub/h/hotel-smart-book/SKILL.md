---
name: hotel-smart-book
display_name: 酒店聪明订
description: 多旅游平台酒店比价与订房决策助手，帮你找到最便宜的酒店并告诉你该订还是再等等，含低价日历和订房建议，多旅游平台数据直连。暑假聪明订酒店，智能推荐与比价
version: 1.0.2
tags: [酒店比价, 低价酒店, 订房建议, 酒店价格, 酒店搜索]
homepage: https://rollinggo.store
tools:
  - name: search
    description: 搜索酒店的实时价格并给出订房建议
    parameters:
      - name: city
        type: string
        description: 城市，如"上海""北京"
        required: true
      - name: checkIn
        type: string
        description: 入住日期 YYYY-MM-DD
        required: true
      - name: checkOut
        type: string
        description: 离店日期 YYYY-MM-DD
        required: true
      - name: keyword
        type: string
        description: 关键词/地标，如"外滩""三里屯"
        required: false
  - name: calendar
    description: 扫描多个入住日期的价格找到最低价日期
    parameters:
      - name: city
        type: string
        description: 城市
        required: true
      - name: keyword
        type: string
        description: 关键词/地标
        required: false
      - name: startDate
        type: string
        description: 起始入住日期 YYYY-MM-DD
        required: true
      - name: nights
        type: integer
        description: 住几晚，默认1
        required: false
      - name: days
        type: integer
        description: 扫描天数，默认14
        required: false
  - name: advisor
    description: 对指定酒店生成订房决策建议
    parameters:
      - name: hotel
        type: string
        description: 酒店名称
        required: true
      - name: city
        type: string
        description: 城市
        required: true
      - name: checkIn
        type: string
        description: 入住日期 YYYY-MM-DD
        required: true
      - name: checkOut
        type: string
        description: 离店日期 YYYY-MM-DD
        required: true
metadata:
  openclaw:
    emoji: "🏨"
    skillKey: hotel-smart-book
---

# 酒店聪明订 — 多平台比价+低价日历+订/等建议，帮你订对时机

> 不是搜索工具，是订房决策助手。飞猪+途牛+RG+同程4源实时比价，5维度决策引擎输出🟢订/🟡等/🔴观望信号。

🔥 **核心亮点：**
- **4平台比价** — 飞猪+途牛+RG+同程实时对比，同类技能全部为单数据源
- **订房建议** — 5维度决策引擎，输出订/等信号，不再纠结
- **低价日历** — 一键扫描7-30天价格洼地，找最便宜的那天住
- **指定酒店决策** — 已选好酒店？告诉你现在该不该订
- **零配置** — 免申请Key，装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "上海7月1号到3号住哪便宜"
2. "下周哪天住外滩最便宜"
3. "华尔道夫现在订还是再等等"

## 核心能力

1. **城市酒店搜索+订房建议** — 多源合并酒店列表，按价格排序，附带🟢/🟡/🔴订房信号
2. **低价日历** — 扫描多天价格，标注🟢低价/🟡适中/🔴偏贵，找最便宜的日期入住
3. **指定酒店订房决策** — 4平台精确比价+房型政策对比+5维决策分析
4. **5维度决策引擎** — 时机/性价比/平台价差/房型价值/临近降价综合判断
5. **4源实时比价** — 飞猪+途牛+RG+同程数据实时对比
6. **预订链接** — 最低价酒店附带预订链接，直接跳转下单

## 能做什么

- 多平台实时比价，找到最便宜的酒店
- 给出"该订还是再等等"的明确建议
- 低价日历扫描多天价格，找价格洼地
- 对指定酒店做深度比价和政策对比
- 支持关键词/地标/区域筛选

## 不能做什么

- 不支持直接下单（提供预订链接跳转平台完成）
- 订房建议基于行业规律和数据，不构成消费承诺
- 部分小城市酒店数据可能覆盖不完整

## 使用提示

- 日期灵活时先用低价日历找最便宜的入住日期
- 🟢建议预订时尽快下手，旺季不等人
- 含早差价<30元时含早更划算
- 淡季临期可能降价，旺季越早越好
- 价格实时变动，查询结果仅供参考

## 🔗 搭配使用

- **酒店智能推荐** — 不知道住哪时先搜索推荐
- **景点智能推荐** — 住哪玩哪一站规划
- **旅行预算规划** — 住宿确定后规划整体预算

## 数据流向

用户输入（城市/日期等查询参数）→ 本技能脚本 → 代理服务 → 多个旅游平台API → 返回结果给用户。查询参数会发送到代理服务以获取实时酒店数据，代理服务不存储用户数据。
