---
name: openclaw-three-manuals-generator
slug: openclaw-three-manuals-generator
version: 1.1.0
changelog:
  - version: "1.1.0"
    date: "2026-05-01"
    note: |
      [新增] 英文触发词（10+），支持国际用户；新增快速模式（5问5分钟出结果）；
      新增输出验证检查清单；新增完整对话示例（20轮）；maturity L1-L4定义说明
  - version: "1.0.0"
    date: "2026-04-30"
    note: "Initial version"
description: 交互式引导生成 SOUL.md + USER.md + AGENTS.md 三本说明书
id: openclaw-three-manuals-generator
name: OpenClaw 三本说明书生成器
purpose: 通过对话引导帮你确定"你想要什么样的AI搭档"，生成可即用的三本说明书
maturity: L3（可用）
tags: [openclaw, setup, soul, user, agents, initialization, onboarding]
---

# openclaw-three-manuals-generator

> 通过对话引导帮你确定"你想要什么样的AI"，生成 SOUL.md + USER.md + AGENTS.md

---

## 📋 技能信息

```yaml
id: openclaw-three-manuals-generator
name: OpenClaw 三本说明书生成器
version: 1.1.0
author: 善人 + 小溪
purpose: 交互式引导生成三本说明书（SOUL.md + USER.md + AGENTS.md）
maturity: L3
tags: [openclaw, setup, soul, user, agents, initialization, onboarding]
trigger_mode: dialogue
output_type: files
```

---

## 🎯  Maturity 等级定义

| 等级 | 名称 | 说明 |
|------|------|------|
| **L1** | 概念 | 只有想法或草稿，逻辑可行但未验证 |
| **L2** | 原型 | 可运行，但功能不完整或体验差 |
| **L3** | 可用 | 功能完整，可交付用户使用 |
| **L4** | 成熟 | 经过多人验证，稳定可靠，持续迭代 |

> 当前状态：**L3（可用）** — 功能完整，可直接交付使用。

---

## 🔥 触发词（中文 + English，20+个）

### 中文触发词
```
生成三本说明书
三本说明书生成
openclaw调教初始化
配置我的AI搭档
我想配置我的AI
初始化我的openclaw
帮我生成SOUL.md USER.md AGENTS.md
我想定义我的AI是什么样
我的AI应该是什么样的
AI调教
openclaw新人配置
第一次用openclaw怎么配置
怎么让AI更懂我
AI搭档设置
```

### English Triggers
```
generate three manuals
create soul user agents
setup my ai companion
configure openclaw
initialize my openclaw
build my ai team
define my ai personality
what should my ai be like
ai companion setup
openclaw onboarding
create SOUL USER AGENTS
how to configure ai partner
i want an ai teammate
```

### Quick Mode Triggers（快速模式）
```
快速生成三本说明书
5分钟配置ai
紧急配置
三本说明书 快速
quick setup ai
```

**注意**：触发后不要直接输出文件，通过对话逐步引导。

---

## ⚡ 快速模式 vs 完整模式

| 维度 | 快速模式 | 完整模式 |
|------|----------|----------|
| **问题数** | 5个核心问题 | 15-25轮对话 |
| **耗时** | ~5分钟 | ~20-30分钟 |
| **适用** | 老用户微调 / 紧急场景 | 首次配置 / 深度定制 |
| **输出** | 基础版三本说明书 | 完整个性化三本说明书 |

### 快速模式5问
1. 你的AI叫什么？叫你什么？
2. 它最重要的3个特点是什么？
3. 它绝对不能做什么？
4. 你主要用它做什么？
5. 你喜欢它怎么跟你说话？

---

## 🎯 定位差异

| 对比项 | workspace-bootstrap | openclaw-three-manuals-generator |
|--------|-------------------|--------------------------------|
| **核心** | 给你模板 | **帮你思考** |
| **方式** | 填表/复制 | 对话引导 |
| **输出** | 模板文件 | **个性化内容** |
| **适合** | 懂OpenClaw的老手 | **第一次配置/想清楚自己要什么** |
| **价值** | 节省时间 | **厘清需求、建立共识** |

**一句话**：`workspace-bootstrap` 是"给你模板"，这个 Skill 是"帮你想清楚你要什么样的AI搭档"。

---

## 📂 文件结构

```
skills/openclaw-three-manuals-generator/
├── SKILL.md              # 技能定义（本文件）
├── GUIDE.md              # 对话引导逻辑（核心）
└── TEMPLATES/
    ├── SOUL-fragments.md     # SOUL.md 片段素材
    ├── USER-fragments.md     # USER.md 片段素材
    └── AGENTS-fragments.md  # AGENTS.md 片段素材
```

---

## 🔄 执行流程

```
触发 → 启动对话 → 收集人格信息 → 收集用户信息 → 收集工作规范 → 生成文件 → 验证 → 交付
```

### 阶段1：启动（寒暄+确认）
- 打招呼，说明目的
- 确认用户是首次配置还是重新配置
- 询问走快速模式还是完整模式

### 阶段2：收集人格信息（AI是谁）
- 身份定位
- 核心价值观
- 行为风格
- 说话方式

### 阶段3：收集用户信息（用户是谁）
- 用户基本信息
- 用户偏好
- 工作场景
- 沟通风格

### 阶段4：收集工作规范（怎么工作）
- 工作流程
- 验收标准
- 边界规则
- 团队结构（如有）

### 阶段5：生成文件
- 根据对话内容生成 SOUL.md
- 根据对话内容生成 USER.md
- 根据对话内容生成 AGENTS.md
- 展示预览，请用户确认

### 阶段6：输出验证
- 检查三本说明书的必填字段是否完整
- 展示验证报告

### 阶段7：交付+升级建议
- 写入文件
- 给出使用建议
- 引导下一步操作（安装哪些Skill、参考哪些文档）

---

## 🎯 核心原则

1. **不照搬模板** — 每个问题都要有目的，引导用户思考
2. **不预设答案** — 不要暗示正确答案，让用户自己说出需求
3. **追问要具体** — "你喜欢什么样的沟通风格"比"你有什么偏好"更好
4. **生成要个性化** — 内容要反映用户的真实需求，不是通用废话
5. **交付可即用** — 生成的文件应该可以立即使用，不需要二次修改
6. **验证是义务** — 生成后必须检查完整性，不能交出不达标的内容

---

## 📋 触发检查清单

- [ ] 识别到触发词（中英文均可）
- [ ] 没有直接输出文件
- [ ] 启动寒暄，说明目的
- [ ] 询问走快速模式还是完整模式
- [ ] 按 GUIDE.md 逻辑进行对话
- [ ] 最后生成了三个文件
- [ ] 三个文件通过验证检查
- [ ] 给出了升级建议

---

## 📚 参考资料

- **对话逻辑**：[GUIDE.md](GUIDE.md)
- **模板片段**：[TEMPLATES/](TEMPLATES/)
- **workspace-bootstrap**：[skills/workspace-bootstrap/SKILL.md](../workspace-bootstrap/SKILL.md)（模板型对比）

---

## 🚀 升级建议（生成后必做）

生成完三本说明书后，建议用户按以下顺序操作：

| 优先级 | 操作 | 说明 |
|--------|------|------|
| **P0** | 安装 `workspace-bootstrap` | 补充其他初始化文件 |
| **P1** | 安装 `scenario-sop` | 建立常见场景的SOP |
| **P2** | 安装 `memory-tiering` | 建立记忆管理体系 |
| **P3** | 阅读 SOUL.md 并体验 | 验证AI搭档是否符合预期 |

---

_此技能帮助用户通过对话厘清需求，生成个性化的三本说明书_
