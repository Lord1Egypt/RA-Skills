---
name: IoT智能设备管理
slug: iot-smart-device-manager
description: 面向智能家居和工业物联网场景的设备监控、协议适配（MQTT/CoAP/Zigbee）、故障诊断、自动化规则配置和能耗优化
version: 1.0.0
author: ai-gaoqian
tags:
  - iot
  - smart-home
  - mqtt
  - automation
  - edge-computing
  - device-management
metadata:
  openclaw:
    requires:
      - web_search
      - python_executor
      - shell_executor
---

# IoT智能设备管理

## 使用方式
用户描述IoT设备管理需求，包括设备接入、协议配置、自动化场景编排、故障排查、能耗分析等。

## 执行流程
1. 设备发现：识别网络中的IoT设备并确认通信协议（MQTT/CoAP/Zigbee/BLE/WiFi）
2. 协议适配：生成MQTT topic配置、CoAP端点定义、Zigbee cluster映射
3. 自动化规则：使用if-this-then-that模式编排设备联动规则
4. 故障诊断：分析设备离线原因并提供排查步骤
5. 能耗分析：计算设备功耗并推荐优化策略

## 输出格式
- 设备拓扑图（设备列表及通信关系）
- MQTT主题树和payload格式定义
- 自动化场景YAML配置文件
- 故障排查决策树
- 能耗报告（按设备/时段/场景分析）

## 注意事项
- 支持主流IoT平台（Home Assistant/Tuya/AWS IoT/Azure IoT Hub）
- MQTT配置默认使用TLS加密
- 自动化规则支持时间/传感器/设备状态等多条件触发
- 故障诊断需考虑网络层/应用层/硬件层三级排查
