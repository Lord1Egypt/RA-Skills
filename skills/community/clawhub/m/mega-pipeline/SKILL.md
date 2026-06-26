---
name: mega-pipeline
description: "全闭环自动化管道 — Hunter→Skill Factory→Orchestrator→Dashboard→Profit。将Phase 1-3所有组件串联为自动运行的超级管道。核心能力：(1) 一键全流程 (2) 定时自动运行 (3) 异常自愈 (4) 利润报告"
version: 1.0.0
author: Apex Catalyst
---

# Mega Pipeline — 全闭环自动化

## 管道流程
```
Step 1: Hunter Scan (市场扫描)
Step 2: Skill Check (缺口分析)  
Step 3: Auto-Generate (自动补全)
Step 4: Dashboard (状态刷新)
Step 5: Profit Report (利润报告)
Step 6: Resilience (自愈检查)
```

## 命令
```bash
python3 scripts/run_pipeline.py        # 执行完整管道
python3 scripts/run_pipeline.py --status  # 管道状态
```
