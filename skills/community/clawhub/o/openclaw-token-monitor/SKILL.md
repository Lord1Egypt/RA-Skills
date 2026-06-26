---
name: token-monitor
description: OpenClaw Token 实时监控面板。支持：(1) SQLite 持久化存储历史数据 (2) 实时监控当前 Token 消耗（增量曲线） (3) 历史视图查看任意一天的消耗 (4) 按日/时会话汇总 (5) 人民币费用估算（MiniMax 官方定价） (6) 滚轮缩放 X 轴 (7) 图表采样防卡顿。触发场景：(1) 用户要求查看 Token 消耗 (2) 监控 AI 模型使用量 (3) 分析日/小时级别消耗趋势 (4) 排查 Token 异常消耗。
author: OldYoung
email: ericyang81@gmail.com
version: 1.2.0
tags: latest
---

# OpenClaw Token 监控中心

## 快速开始

```bash
# 启动监控服务
node skills/token-monitor/scripts/token-monitor.js

# 访问面板
open http://192.168.50.210:3000
```

## 功能一览

| 模块 | 说明 |
|------|------|
| 📊 **实时曲线** | 每 3 秒轮询，蓝线显示每次轮询的 Token 增量，橙线显示速率 (tokens/s) |
| 📈 **历史视图** | 点 ← → 或日期下拉，查看任意一天的完整消耗曲线 |
| 🏺 **SQLite 持久化** | 数据写入 `/workspace/data/token_history.db`，刷新页面不丢失 |
| 💰 **人民币估算** | 基于 MiniMax 官方定价（输入 ¥2.1/百万，输出 ¥8.4/百万） |
| 📋 **会话详情表** | 每会话 Input/Output/Total Tokens、费用、占比条 |
| 🍩 **环形图** | 各会话 Token 消耗占比分布 |
| 🔍 **滚轮缩放** | 鼠标在图表上滚轮可放大/缩小 X 轴 |
| 📷 **导出图片** | 点击"📷 导出图表"下载 PNG |

## 数据存储

- **数据库**: `data/token_history.db`（SQLite）
- **表**: `snapshots`（每次轮询各会话明细）、`rate_history`（每次轮询速率）、`daily_summary`（每日汇总）
- **轮询间隔**: 3 秒（可在页面顶部调整）
- **保留策略**: 永久保留，按日期查询

## 技术细节

- **服务器**: `token-monitor.js`（Node.js，端口 3000）
- **前端**: `token-monitor.html`（Chart.js + chartjs-plugin-zoom，纯前端无需构建）
- **数据库**: sql.js（WASM 版本，无需本地 SQLite 编译）
- **API**: `/data`（实时快照）、`/api/daily?date=YYYY-MM-DD`（历史数据）、`/api/dates`（可用日期列表）
- **依赖**: `openclaw sessions --active --json`（数据来源）

## 目录结构

```
skills/token-monitor/
├── SKILL.md          # 本文件
├── package.json
└── scripts/
    ├── token-monitor.js   # 服务器（轮询 + SQLite + API）
    └── token-monitor.html # 前端仪表盘
```
