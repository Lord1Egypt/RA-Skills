---
name: langgraph-idea-generator
description: 用 LangGraph 把老板的一句话需求变成 3 行可执行代码方案（带 tool 去重，避免重复造轮子）。Use when user mentions "写代码的点子", "用代码解放双手", "LangGraph demo", or wants a quick coding plan.
---

# LangGraph Idea Generator 🐛

> **核心主题**：用代码解放双手（RULE-20260610-001）

把老板的一句话需求，经过 **分类 → 评估 → 生成 3 行落地** 三步流水线，变成可直接抄作业的代码方案。

## 适用场景

- 老板突然有个想法，想快速评估"这个能写代码吗？"
- 想看看 3 个不同切入点
- 学习 LangGraph 状态图（demo 范本）

## 流水线

```
START → classify → complexity → plan → END
        [工作]/   高/中/低    命令/场景/文件
        [生活]/
        [学习]
```

## 快速使用

```bash
# 调用（从任何目录）
idea-gen "自动汇总日报"
idea-gen "做个时间统计脚本"
echo "批量重命名工具" | idea-gen
```

## 输出格式

```
🏷️  分类：[工作] IT 运维/数据处理/自动化
📊 复杂度：中
📋 3 行落地：
命令：python3 daily_report.py --dir ~/worklogs --out daily_summary.md
场景：扫描工作日志目录，按类型分类汇总并生成 Markdown 日报。
文件：~/scripts/daily_report.py
```

## 技术栈

| 组件 | 版本 | 作用 |
|------|------|------|
| LangGraph | 1.2.6 | StateGraph 状态机 |
| langchain-anthropic | 1.4.6 | 走 Anthropic 协议调 M3 |
| M3 (MiniMax-M3) | - | 分类/评估/生成 |
| Python | 3.12+ | - |

## 文件结构

```
langgraph-idea-generator/
├── SKILL.md              # 本文件
├── skill.json            # 元数据
├── _meta.json            # OpenClaw 内部
├── .venv/                # skill 自带 venv（langgraph + langchain-anthropic）
├── scripts/
│   ├── idea_gen.py       # 核心 StateGraph 流水线
│   └── cli.sh            # CLI 入口（idea-gen 命令）
└── assets/
    └── origin.json       # ClawHub 注册（未发布）
```

## 安装说明

skill 自带 venv（`.venv/`），首次安装后**已预装依赖**。  
如需重装：`cd ~/.openclaw/workspace-coding-advisor/skills/langgraph-idea-generator && .venv/bin/pip install langgraph langchain-anthropic`

## 与 OpenClaw 集成

- **位置**：`~/.openclaw/workspace-coding-advisor/skills/`（OpenClaw 自动扫描）
- **CLI 入口**：`scripts/cli.sh` 已软链到 `~/.local/bin/idea-gen`（PATH 包含 `~/.local/bin`）
- **凭证**：用 `EM_API_KEY` 环境变量

## 扩展方向

- [ ] 加条件分支（复杂度=高 → 多走一步「拆解节点」）
- [ ] 加 checkpointer（流程可中断恢复）
- [ ] 加 tools 节点（查 ~/scripts/ 现有脚本去重）
- [ ] 接入飞书消息（直接推到老板私聊）

---

**版本**: v1.0.0  
**作者**: 码虫 coding-advisor  
**创建日**: 2026-06-22
