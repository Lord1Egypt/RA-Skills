---
name: pans-pricing-engine
description: |
  AI算力销售定价引擎。根据客户规模、合同期限、预付金额计算阶梯折扣价。
  支持数量/时长/预付三重折扣累乘，生成报价单。
  触发词：定价计算, 折扣报价, GPU价格, 阶梯折扣, pricing engine, quote generator
---

# pans-pricing-engine

AI算力销售定价引擎 — 根据客户规模、合同期限、预付金额计算阶梯折扣报价。

## 触发词
定价计算, 折扣报价, GPU价格, 阶梯折扣, pricing engine, quote generator

## 功能
- 支持 H100 / A100 80GB / A100 40GB / L40S / A10G 五种GPU
- 数量折扣（10-50卡5% / 51-100卡10% / 101-500卡15% / 500+卡20%）
- 时长折扣（1年5% / 2年10% / 3年15%）
- 预付折扣（季度3% / 半年5% / 年付10%）
- 三重折扣累乘，最高可达 40%+
- 支持 JSON 输出和多方案对比

## 使用方式

### 查看所有GPU基础价格
```bash
python3 scripts/pricing.py --list
```

### 单个方案报价
```bash
python3 scripts/pricing.py --gpu H100 --count 100 --duration 24 --prepay year
```

### 多方案对比
```bash
python3 scripts/pricing.py --compare --scenarios h100_100_24m, h100_200_36m
```

## 折扣规则

| 维度 | 条件 | 折扣 |
|------|------|------|
| 数量 | 10-50卡 | 5% |
| 数量 | 51-100卡 | 10% |
| 数量 | 101-500卡 | 15% |
| 数量 | 500+卡 | 20% |
| 时长 | ≥12月 | 5% |
| 时长 | ≥24月 | 10% |
| 时长 | ≥36月 | 15% |
| 预付 | 季度预付 | 3% |
| 预付 | 半年预付 | 5% |
| 预付 | 年付 | 10% |
