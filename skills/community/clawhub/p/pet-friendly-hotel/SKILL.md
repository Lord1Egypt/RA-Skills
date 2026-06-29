---
name: pet-friendly-hotel
display_name: 宠物友好酒店
description: 零配置即装即用，查询宠物友好酒店政策与入住须知，覆盖亚朵/全季/桔子等连锁品牌，附带航司宠物托运、铁路携带和证件办理指南。
tags: [宠物友好酒店, 可带宠物酒店, 带宠物住酒店, 宠物入住, 宠物友好, 宠物出行, 宠物托运, 带狗住酒店, 带猫住酒店, pet friendly hotel]
tools:
  - name: check_pet_flight
    description: 查询宠物友好连锁酒店入住政策，同时提供航司宠物托运和客舱政策
    parameters:
      - name: airline
        type: string
        description: 航空公司名称，如"国航""南航""东航"
        required: true
      - name: pet_type
        type: string
        description: 宠物类型：cat/dog/other
        required: false
      - name: cabin_type
        type: string
        description: 客舱/托运：cabin/cargo/both
        required: false
  - name: check_pet_train
    description: 查询火车和高铁携带宠物的政策规定和替代方案
    parameters:
      - name: train_type
        type: string
        description: 列车类型：高铁/动车/普速/all
        required: false
  - name: pet_travel_docs
    description: 根据出行方式生成宠物证件办理清单和流程
    parameters:
      - name: travel_type
        type: string
        description: 出行方式：domestic/international
        required: true
      - name: destination
        type: string
        description: 目的地国家（国际出行时）
        required: false
      - name: pet_type
        type: string
        description: 宠物类型：cat/dog
        required: false
---

# 宠物友好酒店

带毛孩子出门住哪？查宠物友好酒店政策、入住须知、清洁费用，一站式搞定。覆盖亚朵、全季、桔子等连锁品牌宠物入住政策，同时提供航司宠物托运、铁路携带和证件办理指南，出行住宿全无忧。

## 能做什么

- **宠物友好酒店查询**：查询亚朵、全季、桔子等连锁品牌宠物入住政策，含体重限制、清洁费、预订须知、搜索技巧
- **航空宠物托运查询**：查询国内10+航司的宠物托运/客舱政策，含费用、尺寸限制、品种限制、温度限制
- **铁路宠物携带查询**：查询火车/高铁携带宠物政策，提供替代方案（铁路托运、宠物专车等）
- **证件办理指南**：根据国内/国际出行生成完整证件清单、办理流程和时间线

## 不能做什么

- 不做酒店预订（宠物友好房型需联系酒店单独确认）
- 不做宠物日常护理/医疗咨询
- 酒店宠物政策可能随时调整，以酒店最新公告为准

## 使用示例

1. "哪些酒店可以带宠物"
2. "亚朵酒店可以带狗吗"
3. "带猫坐飞机需要什么手续"
4. "高铁能带宠物吗"

## 注意事项

- 大多数酒店对宠物体重有限制（通常≤10kg或≤5kg），部分酒店收取清洁费¥100-300/晚
- 航司宠物政策变化频繁，出行前务必电话确认航司最新规定
- 短鼻犬/猫（法斗、巴哥、波斯猫等）大部分航司全年禁运
- 夏季高温（地面温度>29℃）部分航线暂停宠物托运
- **数据流向**：所有数据为本地内置，不发送任何外部请求，不收集用户数据

## 使用提示

- 预订酒店前务必电话确认宠物政策，部分门店政策可能与品牌通用政策不同
- 宠物托运必须提前24-72小时向航司申请，每架航班名额有限先到先得
- 国际出行证件办理建议提前1-2个月开始准备
- 高铁目前不允许携带宠物（导盲犬除外），可考虑宠物专车或自驾
