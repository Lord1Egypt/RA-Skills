---
name: pet-travel-guide
display_name: 宠物出行助手
description: 宠物出行助手，覆盖国内10+航司宠物托运/客舱政策、铁路携带规定和证件办理指南，带毛孩子出行查政策、办证件一站搞定，零配置即装即用。
tags: [宠物出行, 宠物托运, 宠物上飞机, 宠物坐火车, 宠物证件]
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

# 宠物出行助手 — 航空托运+铁路政策+证件办理，带毛孩子出门不踩坑

> 覆盖国内10+主流航司宠物政策，高铁/火车携带规定，国内/国际证件办理完整指南。

🔥 **核心亮点：**
- **10+航司覆盖** — 国航/南航/东航/海川/春秋等宠物托运/客舱政策全查
- **铁路政策** — 高铁/火车携带宠物规定+替代方案（宠物专车/托运）
- **证件办理** — 国内/国际出行完整证件清单、流程和时间线
- **品种限制提醒** — 短鼻犬/猫禁运提醒，温度限制提示
- **零配置** — 纯本地数据，无需网络

## 快速入门

**3个开场白示例，复制即用：**

1. "国航可以带猫上飞机吗"
2. "高铁能带狗吗"
3. "带猫出国需要办什么证件"

## 核心能力

1. **航司政策查询** — 10+航司宠物托运/客舱政策，含费用、尺寸、品种、温度限制
2. **铁路政策查询** — 高铁/火车携带宠物规定+替代方案
3. **证件办理指南** — 国内/国际出行证件清单、流程和时间线
4. **品种限制** — 短鼻犬/猫(法斗/巴哥/波斯猫)禁运提醒
5. **温度限制** — 夏季高温(>29℃)部分航线暂停托运
6. **提前申请** — 托运需提前24-72小时申请，名额有限先到先得

## 能做什么

- 查询国内航司的宠物托运和客舱政策
- 查询火车/高铁携带宠物政策和替代方案
- 生成国内/国际出行的宠物证件办理清单和流程

## 不能做什么

- 不做宠物订票/预订（需联系航司单独申请）
- 不做宠物日常护理/医疗咨询
- 不做宠物托运代操作

## 使用提示

- 宠物托运必须提前24-72小时向航司申请，每架航班名额有限
- 航空箱需符合IATA标准，三边之和≤158cm为常见要求
- 国际出行证件办理建议提前1-2个月开始准备
- 高铁目前不允许携带宠物（导盲犬除外），可考虑宠物专车或自驾
- 短鼻犬/猫大部分航司全年禁运，出行前务必确认

## 🔗 搭配使用

- **宠物友好酒店** — 查哪些酒店可以带宠物入住
- **自驾出行规划** — 自驾带宠物的路线规划
- **出行保障助手** — 含宠物相关保障的旅行保险

## 数据流向

所有数据为本地内置，不发送任何外部请求，不收集用户数据。
