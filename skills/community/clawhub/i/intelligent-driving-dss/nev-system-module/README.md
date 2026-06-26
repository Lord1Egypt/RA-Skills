# NEV System Module (新能源系统模块)

## 用途
本模块提供新能源汽车（NEV, New Energy Vehicle）系统的核心概念定义、数据结构及接口规范，支持智能驾驶决策系统中的能源管理、电池状态监测、充电策略优化等功能。

**适用对象：** 智能电动汽车、插电式混合动力汽车、燃料电池汽车等新能源车型

## 核心组件
- `README.md` - 模块总览和使用指南
- `概念定义.md` - 新能源系统关键术语和定义
- `数据结构.json` - 标准数据模型和接口定义
- `能源管理.md` - 电池管理系统 (BMS) 与能量分配策略
- `充电管理.md` - 充电桩交互、充电状态监测和充电策略
- `安全监测.md` - 热失控预警、高压系统防护

## 数据交换格式
所有模块间通信采用 JSON 格式，符合 ISO 21434（汽车网络安全）和 GB/T 32960（新能源汽车远程通信协议）标准。

## 接口示例
```javascript
// 获取当前电池状态
const batteryStatus = await NEVAPI.getBatteryStatus({ vin });

// 查询充电站信息
const chargingStation = await NEVAPI.findChargingStation({ location, powerLevel });

// 优化能量管理策略
const energyStrategy = await NEVAPI.optimizeEnergyManagement({ route, weather });
```

---
_此模块由 intelligent-driving-dss 技能自动维护，与 core-traffic-rules 配合使用_
