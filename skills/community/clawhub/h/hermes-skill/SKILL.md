---
name: hermes-skill
description: 🤖 AI 自进化技能包 — 自动从复杂任务创建可复用技能，HOT/WARM/COLD 分层记忆管理，智能 Nudge 提醒与定时自检，持续让 AI 越用越聪明。追踪 NousResearch/Hermes-Agent 上游演进。
version: "1.1.0"
author: devrobbin
homepage: https://github.com/devrobbin/hermes-skill
license: MIT
keywords:
  - self-improving
  - auto-skill
  - memory
  - nudge
  - ai-evolution
  - hermes
  - self-learning
  - openclaw-skill
  - upstream-tracker
  - auto-evolution
triggers:
  - 自进化
  - 自我学习
  - 自动创建技能
  - 记忆管理
  - 学习系统
  - 类似 Hermes
  - 持续改进
  - 上游追踪
  - Hermes Agent
---

# HermesSkill — AI 自进化技能包

让 AI Agent 拥有**持续进化的能力**——像 Hermes Agent 一样，从经验中学习、自我改进。

## 核心模块

| 模块 | 脚本 | 说明 |
|------|------|------|
| 记忆管理 | `memory_tool.py` | HOT/WARM/COLD 三层记忆、搜索、增删 |
| Nudge 提醒 | `nudge_system.py` | 定时自检、智能提醒、知识保存触发 |
| 技能创建 | `auto_skill_creator.py` | 复杂任务自动生成可复用 skill |
| 技能评估 | `skill_evaluator.py` | 评分反馈、自动改进、usage 追踪 |
| 自检 | `self_check_cron.sh` | cron 定时健康检查 |
| **上游追踪** | `upstream_tracker.py` | 追踪 Hermes Agent 最新演进 |

## 上游追踪系统

### 追踪目标
**NousResearch/hermes-agent** — GitHub 56k+ Stars，自进化 AI Agent 标杆

### 追踪文件映射
| 上游路径 | 本地对应 |
|----------|----------|
| `agent/memory_manager.py` | `memory_tool.py` |
| `agent/memory_provider.py` | `memory_tool.py` |
| `agent/skill_commands.py` | `auto_skill_creator.py` |
| `agent/skill_utils.py` | `auto_skill_creator.py` |
| `agent/prompt_builder.py` | `nudge_system.py` |

### 使用方式

```bash
# 检查上游新提交并分析融合价值
python3 scripts/evo_main.py upstream check

# 查看追踪状态
python3 scripts/evo_main.py upstream status

# 显示具体文件对比
python3 scripts/evo_main.py upstream diff agent/memory_manager.py

# 查看融合推荐
python3 scripts/evo_main.py upstream fuse

# 列出追踪的核心文件
python3 scripts/evo_main.py upstream list
```

### 工作原理

1. **Fetch** — 从 GitHub API 获取 nousresearch/hermes-agent/main 最新 30 条 commit
2. **Detect** — 找出涉及核心模块的变更（memory、skill、prompt 等）
3. **Analyze** — 提取新增的类/方法/模式，对比本地实现，计算融合价值
4. **Record** — 高价值 diff 存入 `upstream-tracker/state.json` + 追加到 `changelog.md`
5. **Notify** — 每日 09:00 自动检查，有高价值发现时推送摘要

### 融合价值评估

| 分数 | 含义 |
|------|------|
| 7-10/10 | 上游重大新能力，值得深度融合 |
| 3-6/10 | 有借鉴价值，选择性融合 |
| 1-2/10 | 边缘改进，记录即可 |

### 存储位置
- 追踪状态: `~/self-improving/upstream-tracker/state.json`
- 变更记录: `~/self-improving/upstream-tracker/changelog.md`

## 自进化统一入口

```bash
python3 scripts/evo_main.py nudge [type]          # 检查/触发 nudge
python3 scripts/evo_main.py remember <text>       # 添加记忆
python3 scripts/evo_main.py forget <text>         # 删除记忆
python3 scripts/evo_main.py search <query>        # 搜索记忆
python3 scripts/evo_main.py stats                 # 记忆统计
python3 scripts/evo_main.py skills                # 列出 auto skills
python3 scripts/evo_main.py eval <skill,rating>   # 评估 skill
python3 scripts/evo_main.py improve <skill,notes>  # 改进 skill
python3 scripts/evo_main.py upstream <cmd>        # 上游追踪 (check|status|diff|list|fuse)
python3 scripts/evo_main.py check                 # 完整自检
```

## 定时任务
- 每小时: Nudge 自检（检查知识保存、记忆整理）
- 每天 09:00: Hermes Agent 上游追踪检查

## 版本历史
- v1.0.0: 初始版本（HOT/WARM/COLD + nudge + auto-skill）
- v1.1.0: 新增上游追踪系统，对接 Hermes Agent 主线演进

## 开发规范（重要）

本技能包本身是自进化系统，任何模块有改进时必须遵守以下规则：

### GitHub 同步规则
> **每次自身技能进化必须同步到 GitHub 仓库**

改进流程：
1. 在本地 `~/.qclaw/skills/hermes-skill/` 改进代码
2. `git add` + `git commit -m "描述"`
3. `git push` 推送到 origin/main
4. 同步更新 `SKILL.md` / `README.md` 说明（如果功能有变化）

### Changelog 追加规则
> 新增模块、重大重构或 API 变更 → 在 `upstream-tracker/changelog.md` 底部追加条目

格式：
```
## YYYY-MM-DD — vX.X.X
- [改进描述]
- [文件变更]
```

### 避免事项
- ❌ 只在本地改，不 push
- ❌ 更新代码但不更新文档
- ❌ 破坏已有的 upstream-tracker 状态文件
