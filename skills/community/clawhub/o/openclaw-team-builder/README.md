# OpenClaw Team Builder

> AI Agent 团队管理工具 — 让你的 AI 团队像公司一样运转

[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.x-blue)](https://docs.openclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 它做什么？

OpenClaw 原生支持多 Agent，但缺少**团队管理**能力：

- 没有组织架构 → Team Builder 提供树状层级管理
- 没有批量操作 → 一键部署"超级个体"4人团队
- 没有健康检查 → 自动扫描 agentToAgent、SOUL.md、binding 缺失
- 没有一键修复 → 根据体检结果自动修复所有问题
- 没有回退机制 → 每次操作自动备份，随时撤回

## 双模式

| 模式 | 用户 | 触发方式 |
|------|------|----------|
| TUI 交互式 | 人类 | `bash team-builder.sh`（无参数） |
| CLI 批处理 | AI Agent | `bash team-builder.sh --tree --json` |

## 快速开始

### 作为 ClawhHub Skill 安装

```bash
npx clawhub install team-builder
```

### 手动安装

```bash
mkdir -p ~/.openclaw/skills/team-builder/scripts/
cp scripts/team-builder.sh ~/.openclaw/skills/team-builder/scripts/
cp SKILL.md ~/.openclaw/skills/team-builder/
```

### 独立脚本使用

```bash
# 直接运行 TUI
bash openclaw-team-builder.sh

# CLI 模式
bash openclaw-team-builder.sh --tree --json
bash openclaw-team-builder.sh --add --id finance --soul template:caiwu --yes
```

## CLI 命令速查

```bash
TB="bash ~/.openclaw/skills/team-builder/scripts/team-builder.sh"

$TB --tree [--json]                          # 查看架构
$TB --add --id <id> [--name --emoji --role --parent --soul --model] [--yes]  # 新增
$TB --solo [--model <m>] [--yes]             # 超级个体模板
$TB --suggest --goal "业务目标" [--json]     # 目标驱动团队推荐
$TB --channels [--agent <id>] [--json]      # 渠道状态
$TB --channels --agent <id> --channel telegram --token <t> --yes  # 添加 bot
$TB --templates [--json]                     # 角色模板列表
$TB --checkup [--json]                       # 健康检查
$TB --fix [--yes]                            # 一键修复
$TB --status [--json]                        # 军团状态
$TB --rollback [--index N] [--yes]           # 回退
```

## 角色模板

内置 9 个开箱即用的角色模板：

| Key | 角色 | Emoji |
|-----|------|-------|
| xingzheng | 行政助手 | 📋 |
| caiwu | 财务助手 | 💰 |
| hr | 人力资源 | 👥 |
| kefu | 客服专员 | 🎧 |
| yunying | 运营专家 | 📈 |
| falv | 法务顾问 | ⚖️ |
| neirong | 内容创作 | ✍️ |
| shuju | 数据分析 | 📊 |
| jishu | 技术支持 | 🔧 |

## 系统要求

- OpenClaw >= 2026.3.0
- python3
- macOS 或 Linux（bash 3.2+）

## 版本兼容性

脚本启动时会自动检测 OpenClaw 版本。如果版本低于 2026.3.0，会给出明确提示并终止运行。

## 许可证

MIT License — 详见 [LICENSE](LICENSE)
