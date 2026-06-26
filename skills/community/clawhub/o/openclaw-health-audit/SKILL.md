---
name: openclaw-health-audit
description: OpenClaw 系统健康审计与自动修复 — 监控 prompt 体积、Cron 合规、Session 清理、Token 消耗
version: 1.0.0
author: halfmoon82
tags: [health, audit, monitoring, cron, token-cost, maintenance, cost-optimization]
requires_approval: false
homepage: https://clawhub.ai/halfmoon82/openclaw-health-audit
---

# openclaw-health-audit

OpenClaw 系统健康审计与自动修复工具。发现并修复 prompt 体积漂移、Cron Job 违规、孤儿 Session 积累、Token 消耗异常等隐性成本问题。

## ⚠️ Security & Permissions Declaration

**Privileged operations performed by this skill (all user-initiated):**

| Operation | Purpose | Scope |
|-----------|---------|-------|
| Read `~/.openclaw/openclaw.json` | Inspect config for health issues | Read-only |
| Read OpenClaw logs | Detect anomalies and cost spikes | Local files only |
| List and inspect Cron Jobs | Check isolation compliance | Local OpenClaw API |
| Run local Python health-check scripts | Analyze system state | No network required |
| Update Cron Job `sessionTarget` | Auto-fix isolation violations | OpenClaw sessions only |

**What this skill does NOT do:**
- Does NOT delete or modify user data
- Does NOT access API keys directly
- Does NOT send data to external servers
- Does NOT run with elevated (sudo/root) privileges

## 首次安装

```bash
python3 {skill_dir}/scripts/audit_wizard.py
```

向导将自动：
1. 测量当前 prompt 文件大小并生成个性化阈值
2. 检测已安装的子代理
3. 检测 semantic-router（决定是否启用 Category E）
4. 生成 `config/config.json`
5. 可选注册 48h 定期 Cron Job

## 触发词

以下关键词会触发本 skill：
- `健康检查`、`system health`、`health check`
- `健康报告`、`health report`、`audit`
- `运行监控`、`检查 cron`、`token 消耗`

## 生成健康报告

```bash
python3 {skill_dir}/scripts/health_monitor.py --report
```

将报告发送给用户（Telegram/Discord），等待用户回复修复指令。

## 修复指令解析

用户回复以下内容时，执行对应命令：

| 用户回复 | 执行命令 |
|---------|---------|
| `health fix all` | `health_monitor.py --fix all` |
| `health fix 1,3` | `health_monitor.py --fix "1,3"` |
| `health fix 2` | `health_monitor.py --fix "2"` |
| `health skip` | 跳过，等待下次检查 |

## 报告格式说明

```
🔍 OpenClaw 健康报告 (2026-03-05 02:00)

🔴 告警: 1 | 🟡 警告: 2 | ✅ 正常类别: 2/5

问题清单:

🔴 [1] [B] Cron Job 违规: 3 个
   - [abc12345...] weekly-report: sessionKey 非 null（污染主会话）
   💊 修复: 修复 3 个违规 Job

🟡 [2] [A] SOUL.md 体积漂移: 9KB (9215B)
   阈值: warn=6KB, alert=8KB
   💊 修复: 手动审查 SOUL.md，将非核心内容移至 memory/LESSONS/lessons.md

────────────────────────────────────────
• "health fix all" — 执行全部 (2 项)
• "health skip" — 本次忽略
```

## 监控类别说明

| 类别 | 检查内容 | 可自动修复 |
|------|---------|----------|
| A | System Prompt 体积漂移 | ❌ 手动 |
| B | Cron Job 合规性 | ✅ 自动 |
| C | 孤儿 Session（>N 天无活动）| ✅ 自动 |
| D | Token 消耗趋势 | ❌ 手动 |
| E | 缓存配置完整性（可选，需 semantic-router M1/M3）| ❌ 手动 |

## 更新配置

```bash
# 重新运行向导更新阈值
python3 {skill_dir}/scripts/audit_wizard.py

# 手动编辑配置
# config/config.json
```

## 调试命令

```bash
# 预览报告（不修改任何文件）
python3 {skill_dir}/scripts/health_monitor.py --dry-run

# 列出所有可执行的修复命令
python3 {skill_dir}/scripts/health_monitor.py --list-fixes

# 执行全部修复
python3 {skill_dir}/scripts/health_monitor.py --fix all
```
