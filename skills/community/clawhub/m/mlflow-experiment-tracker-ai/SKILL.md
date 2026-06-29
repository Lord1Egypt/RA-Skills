---
name: MLflow Experiment Tracker
slug: mlflow-experiment-tracker
description: >
  MLflow 实验追踪智能助手。自动分析实验运行结果、对比超参数配置、
  检测过拟合风险、推荐最优模型，为机器学习团队提供端到端的实验管理能力。
version: 1.0.0
author: ai-gaoqian
tags:
  - mlops
  - machine-learning
  - mlflow
  - experiment-tracking
  - model-selection
metadata:
  openclaw:
    requires: ">=1.0.0"
---

# MLflow Experiment Tracker

## 概述

面向 MLflow 用户的实验分析技能，将原始运行日志转化为可操作的模型优化决策。

## 核心能力

### 1. 实验运行分析
- 自动解析 MLflow Tracking Server 数据
- 可视化训练曲线（loss/accuracy 趋势）
- 检测训练异常（震荡、发散、平台期）
- 识别最佳 checkpoint

### 2. 超参数对比
- 多实验横向对比矩阵
- 超参数重要性排序（基于 SHAP/fANOVA）
- 推荐下一轮搜索空间
- 可视化平行坐标图（Parallel Coordinates）

### 3. 过拟合检测
- 训练/验证集指标差距分析
- Early Stopping 最佳时机推荐
- 学习率调度策略评估
- 正则化强度适宜性检查

### 4. 模型选优与注册
- 多指标加权评分排名
- 推荐注册到 MLflow Model Registry 的候选模型
- 生成模型卡（Model Card）文档
- 版本兼容性检查

### 5. 实验管理增强
- 批量重命名和标签管理
- 实验归档和清理建议
- 资源消耗分析（GPU 时、内存峰值）
- 实验复现检查清单

## 使用方式

```
分析实验运行: <experiment_id>
对比超参数: <experiment_ids>
推荐最优模型: <experiment_id> <metric_name>
检测过拟合: <run_id>
```

## 输出格式

- 实验分析仪表板（Markdown + 图表）
- 超参数对比矩阵表
- 模型推荐报告（含排名理由和部署建议）
- 过拟合风险热力图

## 数据底座

基于 MLflow 2.x 官方文档、Optuna/Hyperopt 超参优化最佳实践、Google ML Crash Course、Full Stack Deep Learning 课程内容，覆盖 100+ 常用 ML 指标和 50+ 调参策略。

## 定价

¥0.50 / 次分析
