---
name: profit-agent
description: "利润优化引擎 — 订单管理/计价/结算模拟。核心能力：(1) 订单管理 (2) 计价模型 (3) 成本追踪 (4) 利润计算"
version: 1.0.0
author: Apex Catalyst
---

# Profit Agent — 利润优化引擎

## 架构
```
订单录入 → 成本核算 → 计价策略 → 利润计算 → 报告生成
```

## 命令
```bash
python3 scripts/order_manager.py --new-order   # 新建订单
python3 scripts/order_manager.py --report      # 利润报告
python3 scripts/order_manager.py --simulate    # 模拟运行
```
