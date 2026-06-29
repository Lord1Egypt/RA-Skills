---
name: pet-travel-guide
display_name: 宠物出行助手
description: 零配置即装即用，提供3项宠物出行工具，支持航空宠物政策查询、铁路携带政策和证件办理指南，覆盖国内10+航司。
tags: [宠物, 宠物出行, 宠物托运, 宠物上飞机, 宠物坐火车, 宠物友好, 动物检疫, 疫苗, 宠物旅行, pet travel, 航空托运]
tools:
  - name: check_pet_flight
    description: 查询国内主流航司的宠物托运和客舱政策
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

# 宠物出行助手

带毛孩子出行，查政策、办证件、找住处，一站式搞定。覆盖国内10+主流航司宠物托运/客舱政策、铁路携带规定和证件办理指南。

## 能做什么

- **航空政策查询**：查询国内10+航司的宠物托运/客舱政策，含费用、尺寸限制、品种限制、温度限制等
- **铁路政策查询**：查询火车/高铁携带宠物政策，提供替代方案（铁路托运、宠物专车等）
- **证件办理指南**：根据国内/国际出行生成完整证件清单、办理流程、时间线和避坑指南

## 不能做什么

- 不做宠物订票/预订（宠物托运需联系航司单独申请）
- 不做宠物日常护理/医疗咨询
- 不做宠物托运代操作
- 航司政策可能随时调整，以航司最新公告为准

## 使用示例

1. "国航可以带猫上飞机吗"
2. "高铁能带狗吗"
3. "带猫出国需要办什么证件"
4. "南航宠物托运多少钱"

## 注意事项

- 航司宠物政策变化频繁，出行前务必电话确认航司最新规定
- 短鼻犬/猫（法斗、巴哥、波斯猫等）大部分航司全年禁运
- 夏季高温（地面温度>29℃）部分航线暂停宠物托运
- **数据流向**：所有数据为本地内置，不发送任何外部请求，不收集用户数据

## 使用提示

- 宠物托运必须提前24-72小时向航司申请，每架航班名额有限先到先得
- 国际出行证件办理建议提前1-2个月开始准备
- 高铁目前不允许携带宠物（导盲犬除外），可考虑宠物专车或自驾
- 航空箱需符合IATA标准，三边之和≤158cm为常见要求