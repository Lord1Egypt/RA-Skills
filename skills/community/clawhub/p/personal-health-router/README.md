# Health Copilot: Eating, Sleep, and Exercise Tracking / 健康副驾：饮食、睡眠与运动追踪

## Overview / 概述

**Health Copilot** is a comprehensive health-management skill that bridges the gap between raw data recognition and long-term reporting. It combines advanced analysis of meals, sleep, and exercise with automated Feishu (Lark) persistence and derived health assessments.

**Health Copilot（健康助理）** 是一个全链路健康管理 skill。它打通了从原始数据识别到长期报表分析的完整环节，将饮食、睡眠、运动的深度分析与飞书（Lark）自动落库及衍生健康评估引擎完美结合。

---

## Key capabilities / 关键能力

### 1. Recognition & Analysis / 识别与分析
- **Nutrition**: Photo-based calorie and macro estimation from meals.
- **Sleep**: Screenshot-based extraction of sleep stages and recovery signals (Apple Health, Android).
- **Exercise**: Extraction of workout metrics and training load from app screenshots (Garmin, Strava, etc.).
- **Weekly Reassessment**: Cross-domain interpretation of nutrition, sleep, and exercise signals.

### 2. Persistence & Automation / 持久化与自动化
- **Automated Bootstrapping**: Create all required Bitable tables, fields, and views from a config file.
- **Daily Rollups**: Automated aggregation of raw logs into a `Monthly Health Calendar`.
- **Weekly Assessments**: Automated generation of comprehensive weekly reports with risk scoring.
- **Dashboards**: Automated creation/refresh of monthly health overview dashboards with trends.

### 3. Architecture / 架构特性
- **English-Only Core**: Reliable internal schema using English field names for stable reporting scripts.
- **Bilingual documentation**: Full EN/ZH documentation for human users.
- **Config-Driven**: Customize any threshold, label, or wording without touching code.

---

## What it does / 主要功能

This skill handles four primary domains / 这个 skill 涵盖四大领域：

1.  **Nutrition / 营养**
    - Analyze photos -> Estimate nutrients -> Log to Feishu.
    - 拍照分析 -> 营养估算 -> 飞书落库。
2.  **Exercise / 运动**
    - Analyze screenshots -> Extract metrics -> Assess load -> Log to Feishu.
    - 截图分析 -> 指标提取 -> 负荷评估 -> 飞书落库。
3.  **Sleep / 睡眠**
    - Analyze screenshots -> Extract recovery/HRV -> Log to Feishu.
    - 截图分析 -> 恢复/HRV 提取 -> 飞书落库。
4.  **Cross-domain reporting / 跨域报表**
    - Rebuild monthly calendar -> Rebuild weekly assessment -> Refresh dashboard.
    - 重建月度日历 -> 重建周度评估 -> 刷新看板。

---

## Quick start / 快速开始

1.  **Install**: `clawdhub install personal-health-router`
2.  **Configure**: Create `config.json` based on `references/config-template.md`.
3.  **Bootstrap**: `node scripts/bootstrap_health_tables.js config.json`
4.  **Track**: Use the router to recognize food, sleep, or workouts.
5.  **Report**: Run the Python/Node scripts in `scripts/` to generate summaries and dashboards.

---

## Version note / 版本说明

**v1.0.0**: Major update consolidating the analysis router with the Feishu persistence engine. This version introduces an English-only internal table schema for enhanced reliability of reporting scripts.

**v1.0.0**: 重大更新，将分析路由与飞书持久化引擎深度融合。此版本引入了纯英文内部表结构，以提升自动化报表脚本的稳定性。

---

## Installation / 安装

```bash
clawdhub install personal-health-router
```

Update to the latest version / 更新到最新版本：

```bash
clawdhub update personal-health-router
```
