# Presentation Master — Agent 入口

> 本仓库是 skills-repo 组织下的演示技能库。面向独立开发者、创业者和自由职业者，覆盖演讲表达、演示设计、内容创建和模板制作，帮你做出有说服力的演示。采用 skills-repo 组织的 **superpower 架构**。

## 目录约定（superpower）

```
presentation-master/
├── SKILL.md                          # L1 路由层：唯一入口，只做索引
├── references/                       # L2 深层 playbook
│   ├── deck-structure-playbook.md
│   ├── slide-content-rules.md
│   └── visual-design-principles.md
├── skills/                           # L3 细粒度子技能
│   ├── presentation-creator/SKILL.md
│   ├── ppt-template-creator/SKILL.md
│   ├── presentation-design/SKILL.md
│   └── presentation-delivery/SKILL.md
├── scripts/                          # L4 确定性脚本：check_presentation.py
├── assets/                           # L5 模板资源：presentation_rules.json 等
├── AGENTS.md / README.md / LICENSE / .gitignore
```

## 加载顺序（渐进式加载）

1. 先读 `SKILL.md` 路由表，判断任务属于哪一类。
2. **方法论决策**（结构 / 内容规则 / 视觉原则）→ 读 `references/` 对应 playbook。
3. **落地具体动作**（创建 / 模板 / 设计 / 表达）→ 调 `skills/<name>/SKILL.md`。
4. **确定性自检**（字数/标题层级/一致性）→ 跑 [scripts/check_presentation.py](scripts/check_presentation.py)。
5. 套用 `assets/` 模板，不重复造轮子。

## 技能清单

| 环节 | 技能 | 文件 | 用途 |
|------|------|------|------|
| 表达 | presentation-delivery | [skills/presentation-delivery/SKILL.md](skills/presentation-delivery/SKILL.md) | 演讲表达：叙事结构、节奏控制、观众互动 |
| 设计 | presentation-design | [skills/presentation-design/SKILL.md](skills/presentation-design/SKILL.md) | 演示设计：视觉层级、信息图表、排版美学 |
| 创建 | presentation-creator | [skills/presentation-creator/SKILL.md](skills/presentation-creator/SKILL.md) | 演示创建：从大纲到完成稿的全流程 |
| 模板 | ppt-template-creator | [skills/ppt-template-creator/SKILL.md](skills/ppt-template-creator/SKILL.md) | PPT 模板：主题定制、母版设计、品牌模板 |

## 使用场景

- 创业者准备投资人路演 Pitch Deck
- 独立开发者做产品演示和客户提案
- 自由职业者准备项目汇报和竞标方案
- 技术分享和会议演讲的内容准备

## 相关仓库

- `office-master` — 办公效率（格式转换、PPT 自动化），本仓库聚焦演示内容和设计
- `startup-founder` — 创业技能（点子验证、MVP、融资），本仓库聚焦演示呈现
- `visual-designer` — 视觉资产创作（排版、插画、海报、品牌），本仓库聚焦演示文稿的制作和表达

> 本仓库聚焦**演示文稿的内容创作和表达呈现**，与 office-master 的办公自动化和 startup-founder 的商业策略互补。
