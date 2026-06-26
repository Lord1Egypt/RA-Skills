---
name: hermes-agent-skill
description: Hermes 智能体增强系统 — 自动记忆管理、技能生成、跨会话持久化
author: openclaw
slug: hermes-agent-skill
version: 1.0.0
tags: [memory, skill-generation, agent-enhancement, automation, openclaw]
homepage: https://clawhub.ai/skills/hermes-agent-skill
---

# 🧠 Hermes Agent Skill

## 概述

将 Hermes Agent 的 Skill 自动生成 + 持久化记忆系统移植到 OpenClaw，让 OpenClaw 拥有任务复盘提炼技能和跨会话记忆的能力。

### 核心能力

| 功能 | 描述 |
|------|------|
| 🧠 **跨会话记忆** | 自动同步对话、预取相关上下文，实现连续对话体验 |
| 🔧 **Skill 自动生成** | 从任务轨迹中复盘分析，自动提炼可复用的技能 |
| 🔗 **无缝集成** | 与 OpenClaw 现有体系 100% 兼容，零入侵设计 |
| 📊 **数据导出** | 将轨迹数据导出为标准化案例，支持模型优化 |

### 基准性能

| 指标 | 实测值 | 标准 |
|------|--------|------|
| sync_turn | 0.1ms | < 500ms |
| prefetch | 3.6ms | < 500ms |
| 内存占用 | 17.8MB | < 100MB |
| 并发处理 | 10线程 | 10+ |

## 安装

### 前提条件
- OpenClaw 2026.4.15+
- Python 3.9+
- PyYAML 6.0+

### 通过 ClawHub 安装

```bash
clawhub install hermes-agent-skill
```

### 手动安装

```bash
# 1. 克隆项目
git clone https://github.com/openclaw/hermes-agent-skill.git
cd hermes-agent-skill

# 2. 安装依赖
pip install pyyaml

# 3. 初始化系统
./scripts/deploy.sh --workspace ~/.openclaw/workspace --environment production
```

## 配置

### 主配置文件

```yaml
hermes:
  enabled: true
  memory:
    enabled: true
    auto_sync: true
    max_memory_size: 500
    retention_days: 30
  skill_generation:
    enabled: true
    require_approval: true
    min_trajectories: 3
  data_export:
    enabled: true
    export_dir: data/exports
```


### 环境配置

支持三种环境：
- `development` — 调试模式，详细日志
- `staging` — 预发布验证
- `production` — 生产环境，性能优先

## 使用方法

### 初始化系统

```bash
hermes-init --workspace ~/.openclaw/workspace --config hermes.yaml --environment production
```

### 检查系统状态

```bash
hermes-status --health
```

### 在 OpenClaw 配置文件启用

```yaml
# ~/.openclaw/config.yaml
skills:
  hermes-agent-skill: true

hermes:
  enabled: true
  memory:
    auto_sync: true
```

## 版本历史

详见 [CHANGELOG.md](references/CHANGELOG.md)

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-04-23 | 初始版本：记忆系统 + Skill 生成 + 兼容性层 |

## 开发

### 本地开发

```bash
# 安装开发依赖
pip install pyyaml psutil pytest

# 运行测试
python3 tests/test_memory.py
python3 tests/test_skill_generation.py
python3 tests/test_compatibility.py
python3 tests/test_performance.py
python3 tests/test_integration.py
```

### 发布新版本

```bash
# 1. 更新版本号
echo "1.1.0" > VERSION

# 2. 更新变更日志
vim CHANGELOG.md

# 3. 发布到 ClawHub
clawhub publish ./hermes-agent-skill --slug hermes-agent-skill \
  --name "Hermes Agent Skill" \
  --version $(cat VERSION) \
  --changelog "$(head -3 CHANGELOG.md)"
```

## 许可

MIT License

---

*由 OpenClaw 社区维护 | [报告问题](https://github.com/openclaw/hermes-agent-skill/issues)*
