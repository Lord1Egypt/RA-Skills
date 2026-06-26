# openclaw-health-audit

**OpenClaw 系统健康审计与自动修复 Skill** | v1.0.0

> OpenClaw System Health Audit & Auto-Repair Skill

---

## 简介 / Overview

本 Skill 提供 OpenClaw 实例的持续健康监控，解决 LLM Token 消耗的四类隐性成本问题：

This skill provides continuous health monitoring for OpenClaw instances, addressing four types of hidden LLM token cost issues:

| 类别 | 问题 | 典型影响 |
|------|------|---------|
| A | System Prompt 体积漂移 | 每会话 +500-2000 tokens |
| B | Cron Job 配置违规 | 任务挂起 / 会话污染 / 模型成本 10x |
| C | 孤儿 Session 积累 | 状态文件膨胀 |
| D | Token 消耗趋势异常 | 失控任务早期预警 |
| E | LLM 缓存配置漂移（可选）| 对话 cache 命中率归零 |

---

## 安装 / Installation

```bash
# 1. 克隆或下载 skill 到 OpenClaw skills 目录
cd ~/.openclaw/workspace/skills/
# clawhub install openclaw-health-audit  (待 ClawHub 上线后)

# 2. 运行安装向导（推荐）
python3 openclaw-health-audit/scripts/audit_wizard.py
```

向导自动完成：
- 测量当前 prompt 文件大小并生成个性化阈值
- 检测已安装的子代理
- 检测 semantic-router（决定是否启用 Category E）
- 生成 `config/config.json`
- 可选注册 48h 定期检查 Cron Job

---

## 使用 / Usage

```bash
SKILL=~/.openclaw/workspace/skills/openclaw-health-audit

# 生成健康报告（供 agent 推送 Telegram）
python3 $SKILL/scripts/health_monitor.py --report

# 预览报告（不修改任何文件）
python3 $SKILL/scripts/health_monitor.py --dry-run

# 修复指定编号的问题
python3 $SKILL/scripts/health_monitor.py --fix "1,3"

# 修复全部问题
python3 $SKILL/scripts/health_monitor.py --fix all

# 列出可修复的命令
python3 $SKILL/scripts/health_monitor.py --list-fixes

# 重新运行安装向导（更新配置）
python3 $SKILL/scripts/health_monitor.py --setup
```

---

## 配置 / Configuration

配置文件：`config/config.json`（由向导生成，也可手动参考 `config/config.template.json` 调整）

关键配置项：

```json
{
  "prompt_files": {
    "SOUL.md": {"warn": 6144, "alert": 8192}
  },
  "checks": {
    "cache_config": false
  }
}
```

Category E（缓存配置监控）默认关闭，需要 semantic-router M1/M3 补丁时才启用。

---

## 工作原理 / How It Works

详见 `references/layer-audit-guide.md`。核心三层框架：

**Layer 1（架构层）**：System Prompt 体积 × 多 Agent 乘数效应
**Layer 2（Extension 层）**：Cron 违规 + Session 积累 + 缓存命中率
**Layer 3（使用习惯层）**：模型选择 + 会话压缩频率

---

## 文件结构 / File Structure

```
openclaw-health-audit/
├── SKILL.md                    # Agent 使用说明
├── clawhub.yaml                # ClawHub 发布配置
├── scripts/
│   ├── health_monitor.py       # 主监控脚本（配置驱动）
│   └── audit_wizard.py         # 安装向导
├── config/
│   └── config.template.json    # 配置模板
├── templates/
│   ├── SOUL_COMPACT.md         # 子代理 SOUL.md 精简模板
│   └── cron_health_job.json    # Cron Job 模板
└── references/
    └── layer-audit-guide.md   # 三层审计方法论
```

---

## 许可证 / License

MIT License — 自由使用、修改和分发

---

*作者：halfmoon82 | 首发：2026-03-05 | OpenClaw v0.12+*
