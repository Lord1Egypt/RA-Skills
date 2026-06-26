# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Claude Code Skill（非传统代码项目），用于在 OpenClaw 上创建多个独立的飞书机器人 Agent。

## 项目结构

```
openclaw-new-agent/
├── SKILL.md          # Skill 定义文件（核心）
├── README.md         # 用户文档
└── assets/           # README 中的图片资源
```

## 重要说明

这是一个 Skill 包仓库，不是传统应用项目：
- **无构建命令** — 无需编译、打包
- **无测试命令** — 无单元/集成测试
- **无 lint 命令** — 无代码检查

## 主要文件

- **SKILL.md** — Skill 的完整定义，包含创建飞书机器人的分步流程（收集配置 → 备份 → 创建工作区 → 修改配置 → 验证）
- **README.md** — 用户面向的文档，说明痛点和解决方案

## 工作区结构

OpenClaw 的工作区位于 `~/.openclaw/`，结构如下：

```
~/.openclaw/
├── openclaw.json                    # 主配置文件
├── workspace/                       # 主工作区
└── workspace-{name}/               # Agent 工作区（平级）
    ├── SOUL.md                      # Agent 角色定义
    ├── USER.md                      # 用户信息
    ├── AGENTS.md                    # 工作区说明
    └── memory/                      # 每日工作日志
```

## 常用命令

OpenClaw 自身命令（在本机已安装 openclaw 时使用）：

```bash
# 验证配置
openclaw doctor --non-interactive

# 重启 Gateway
openclaw gateway restart

# 查看日志
cat ~/.openclaw/logs/gateway.log
```

## 相关文档

- OpenClaw 官方文档：`~/.nvm/versions/node/v22.22.1/lib/node_modules/openclaw/docs/`
- 飞书插件文档：`~/.openclaw/extensions/openclaw-lark/`
