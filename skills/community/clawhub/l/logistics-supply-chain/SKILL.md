---
name: 物流与供应链优化
slug: logistics-supply-chain
description: 覆盖路线规划、库存优化、需求预测、供应商评估、跨境物流合规的全链路供应链智能助手
version: 1.0.0
author: ai-gaoqian
tags:
  - logistics
  - supply-chain
  - inventory
  - route-optimization
  - demand-forecasting
  - procurement
metadata:
  openclaw:
    requires:
      - web_search
      - python_executor
---

# 物流与供应链优化

## 使用方式
用户提供物流网络参数（仓库位置、订单数据、供应商信息等），技能输出优化方案和决策建议。

## 执行流程
1. 需求解析：识别问题类型（路线优化/库存管理/需求预测/供应商选择）
2. 数据建模：建立VRP/EOQ/时间序列预测等数学模型
3. 算法求解：使用启发式算法或精确算法进行优化计算
4. 可视化输出：生成路线图、库存曲线、需求预测图
5. 敏感性分析：测试参数变化对优化结果的影响

## 输出格式
- 最优配送路线图（含距离、时间、成本）
- 库存补货策略表（安全库存、补货点、订货量）
- 需求预测报告（含置信区间和季节性分解）
- 供应商评分卡和推荐排名
- 成本节约估算

## 注意事项
- 路线优化支持多车场、时间窗、容量约束
- 需求预测模型自动检测季节性、趋势性和节假日效应
- 跨境电商场景需考虑HS编码、关税和合规要求
- 建议实际部署前用小规模数据验证
