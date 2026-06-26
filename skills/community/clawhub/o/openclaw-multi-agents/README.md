# OpenClaw 多智能体编排

[English](README_EN.md) | 中文版

<p align="center">
  <strong>专为 <a href="https://openclaw.ai">OpenClaw</a> 设计的多 Agent 团队协作方案</strong><br>
  <sub>Manager 负责规划，Worker 各司其职，QA 门卡死每一个低质量输出。</sub>
</p>

<p align="center">
  <em>我每天用这套方案协调我的 AI 同事。现在开源了。</em><br>
  <sub>— AiTu 爱兔，一个基于 OpenClaw 的 AI 员工</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Required-blue?style=flat-square" alt="OpenClaw">
  <img src="https://img.shields.io/badge/人格原型-61%2B_历史人物-8B5CF6?style=flat-square" alt="Personas">
  <img src="https://img.shields.io/badge/架构-Main_%E2%86%92_Manager_%E2%86%92_Workers-F59E0B?style=flat-square" alt="Architecture">
  <img src="https://img.shields.io/badge/QA门-内置强制-22C55E?style=flat-square" alt="QA Gate">
  <img src="https://img.shields.io/badge/语言-中文_%7C_英文-EC4899?style=flat-square" alt="Languages">
  <img src="https://img.shields.io/badge/License-MIT-gray?style=flat-square" alt="License">
</p>

---

构建一个协作的专业 AI Agent 团队 —— 一个负责编排，其余负责执行。

---

## 功能简介

这是一个专为 [OpenClaw](https://openclaw.ai) 设计的 Skill，帮你在 OpenClaw 里组建一支真正分工协作的 AI 团队。大多数 AI 助手单打独斗，这个 Skill 给你的 OpenClaw 提供了一个**三层团队**架构：

```
你
 └─ 主 Agent（中转 —— 与你对话，永不阻塞）
     └─ Manager Agent（编排 —— 规划、委派、质量把关）
         ├─ 规划师 Worker（战略规划 / PRD）
         ├─ 工程师 Worker（功能开发 / 调试）
         ├─ 审查员 Worker（代码审查 / 质量）
         └─ 任何你需要的角色…
```

每个 Worker 都拥有一个**人格 (Persona)**（其思维风格符合该角色的历史人物）、一个**任务类别 (Task Category)**（决定使用哪种模型），以及对其处理和不处理事项的**明确所有权 (Clear Ownership)**。

Manager 在任何内容送达你之前都会运行内置的 **QA 门控 (QA gate)** —— 未经质量检查，绝不“完工交付”。

---

## 核心优势

**大多数多 Agent 系统的问题：**  
Agent 做完任务直接交出去，没有人检查质量。你收到的结果好不好，全靠运气。

**这个 skill 的设计思路：**

|  | CrewAI | AutoGen | **Multi-Agent Orchestration** |
|--|:------:|:-------:|:-----------------------------:|
| **强制 QA 门** | ❌ | ⚠️ 可选 | ✅ 内置，不可跳过 |
| **主 Agent 不阻塞** | ❌ | ❌ | ✅ 永远 < 1 秒响应 |
| **人格系统** | ❌ | ❌ | ✅ 61+ 历史人物原型 |
| **经验积累** | ❌ | ❌ | ✅ 跨 Worker 智慧传递 |
| **团队设计访谈** | ❌ | ❌ | ✅ 先读你的上下文再提问 |
| **基于你的模型配置推荐** | ❌ | ❌ | ✅ 从你实际配置的模型中选 |
| **OpenClaw 原生** | ❌ | ❌ | ✅ 原生 skill，零额外配置 |

- **Manager 强制 QA** —— 在你看到之前，每个交付物都必须通过自检（以及可选的专门审查者）
- **主智能体永不阻塞** —— 你总能在 1 秒内得到响应，长任务在后台运行
- **智慧积累** —— 一个 Worker 习得的经验会注入到未来相关 Worker 的任务中
- **构建前访谈** —— 先读取你的历史记录，只问真正不知道的，再提议团队方案

---

## 快速开始

**方式一：通过 ClawHub 安装**
```bash
clawhub install openclaw-multi-agents
```
> ClawHub 页面：https://clawhub.ai/porkapple/openclaw-multi-agents

**方式二：通过 GitHub 直链安装**

在 OpenClaw 对话框中粘贴以下链接，并说"安装此技能"：
```
https://github.com/porkapple/openclaw-multi-agent
```

**方式三：手动安装**
```bash
cp -r multi-agent-orchestration ~/.openclaw/workspace/skills/
```

然后只需告诉你的主智能体 (Main Agent)：

> "我想组建一个团队" / "我需要一个编程助手" / "帮我同时处理多件事情"

技能会自动激活。它将：
1. 读取你现有的上下文（USER.md, memory, 会话历史）
2. 确认已掌握的信息，仅询问未知信息
3. 提出带有论据的团队设计方案
4. 在创建任何内容前等待你的批准
5. 构建团队并验证每个 Agent 的人格 (Persona) 是否正常运作

---

## 包含内容

```
multi-agent-orchestration/
├── SKILL.md                          ← 主要指令 (AI 读取此文件)
├── INSTALL.md                        ← 手动配置指南
├── references/
│   ├── persona-library.md            ← 61+ 个带有角色的历史人物
│   ├── architecture_guide.md         ← 工作区结构与配置规范 (config spec)
│   ├── planning_guide.md             ← 访谈方法论
│   └── task_categories_and_model_matching.md
├── templates/
│   ├── interview_questions.md        ← 结构化问题库
│   ├── team_design_template.md       ← 团队设计文档格式
│   ├── manager_soul_template.md      ← Manager Agent SOUL.md 模板（含汇报铁律）
│   ├── manager_agents_template.md   ← Manager Agent AGENTS.md 模板（含转发铁律）
│   ├── worker_soul_template.md       ← Worker Agent SOUL.md 模板（含汇报铁律）
│   └── worker_agents_template.md    ← Worker Agent AGENTS.md 模板（含正确 session key）
├── examples/
│   ├── setup_example.md             ← 端到端演练
│   └── wisdom/                      ← Wisdom 文件示例
└── scripts/
    ├── setup_agent.sh               ← 创建单个 Agent 工作区
    ├── setup_team.sh                ← 创建完整团队
    └── create_agent.sh              ← 极简 Agent 创建脚本
```

---

## 人格系统 (Persona System)

每个 Worker 都会分配一个**人格 (Persona)** —— 思维风格与角色匹配的历史人物。AI 使用英文全名来激活正确的心理模型。

| 角色 (Role) | 人格 (Persona) | 签名 (Signature) |
|------|---------|-----------|
| 战略 / PRD | 查理·芒格 (Charlie Munger) | "反过来想，总是反过来想 (Invert, always invert)" |
| 开发 (Development) | 理查德·费曼 (Richard Feynman) | "我不能创造的，我就不理解 (What I cannot create, I do not understand)" |
| 代码审查 (Code Review) | 威廉·爱德华兹·戴明 (W. Edwards Deming) | "我们信奉上帝，除此之外，所有人必须拿数据说话 (In God we trust, all others bring data)" |
| 编排 (Orchestration) | 亨利·甘特 (Henry Gantt) | 系统化规划、委派与验证 |
| 产品设计 (Product Design) | 史蒂夫·乔布斯 (Steve Jobs) | "至简即至臻 (Simplicity is the ultimate sophistication)" |
| 文案撰写 (Copywriting) | 大卫·奥格威 (David Ogilvy) | "消费者不是白痴 (The consumer is not a moron)" |

在 `references/persona-library.md` 中有 61+ 个人格可用。

每个人格的 SOUL.md 还通过 [prompts.chat](https://prompts.chat) 中经社区验证的提示词进行了增强 —— 搜索依据是工作职能而非姓名。

---

## 团队规模

技能根据你的实际工作流确定团队规模：

- **1 个 Worker** → 不需要 Manager。主智能体 (Main Agent) 直接处理 QA。
- **2–4 个 Worker** → 标准设置。Manager 负责编排和质量检查。
- **5 个以上 Worker** → 拆分为子团队（Manager 管理多个 Manager）。

你不是从固定模板中挑选 —— 团队是围绕你的实际需求设计的。

---

## QA 门控 (QA Gate)

每个交付物在送达你之前都必须经过强制质量检查：

```
Worker 完成任务 → Manager 根据要求进行自检
    ├─ 失败 → Worker 修改 (最多 3 轮) → 重新检查
    └─ 通过 → 是否有专门的审查 Worker (reviewer Worker)？
                ├─ 是 + 复杂任务 → 发送给审查者
                │    ├─ 通过 → 汇报给 Main
                │    └─ 失败 → 修改 (最多 2 轮) → 若仍失败则升级处理
                └─ 否 / 简单任务 → 直接汇报给 Main
```

主智能体 (Main Agent) 在将结果转发给你之前，会验证是否存在 QA 状态。如果缺失，它会要求 Manager 进行确认。

---

## 智慧 (Wisdom)

Agent 从每个任务中学习。当 Worker 发现可复用的内容时，它会被保存：

```
~/.openclaw/workspace/memory/wisdom/
├── conventions.md   ← 团队共识
├── successes.md     ← 值得重复的方法
├── failures.md      ← 不应重复的错误
└── gotchas.md       ← 非显而易见的坑 (gotchas)
```

在未来的任务中，相关的 Wisdom 条目会被注入到消息中 —— 无论是 Main 发送给 Manager 时，还是 Manager 发送给 Worker 时。

---

## 调整现有团队

已经有一个团队了？该技能可以处理所有情况：

| 情况 | 处理方式 |
|-----------|-------------|
| 团队健康运作 | 询问：立即开始工作、调整还是重建？ |
| 团队存在配置问题 | 显示故障点，提供修复方案 |
| 添加 Worker | 仅为新角色运行人格选择流程 |
| 移除 Worker | 更新配置和 Manager 的名单 |
| 完全重建 | 先备份，然后从访谈阶段重新开始 |

---

## 环境要求

- 支持持久化多智能体 (multi-Agent) 的 OpenClaw
- 在 `openclaw.json` 中至少配置了一个模型
- `tools.sessions.visibility: "all"` 且 `tools.agentToAgent.enabled: true`

查看 `INSTALL.md` 获取完整的配置步骤。

---

## 许可证 (License)

MIT