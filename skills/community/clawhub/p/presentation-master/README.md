# Presentation Master — 演示技能库

> 面向独立开发者、创业者和自由职业者的演示技能集合。覆盖演讲表达、视觉设计、内容创建和模板制作。

## 架构说明（superpower）

本仓库采用 skills-repo 组织的 **superpower 架构**：

- `SKILL.md` — 唯一入口，只做能力路由（本文件）
- `references/` — 深层 playbook：演示结构、幻灯片内容规则、视觉设计原则
- `skills/` — 4 个细粒度子技能，可单独安装
- `scripts/` — `check_presentation.py` 大纲内容规范自检（纯标准库、可复现）
- `assets/` — 内容规则配置、合规大纲示例、结构模板

渐进式加载：Agent 先读路由表，按需读取 `references/` 或 `skills/`，重复任务交给脚本。

## 技能清单

| 技能 | 描述 | 安装量 | 来源 |
|------|------|--------|------|
| presentation-delivery | 演讲表达：叙事结构、节奏控制、观众互动、Q&A 应对 | 2.3K | [skills.sh](https://skills.sh/refoundai/lenny-skills/giving-presentations) |
| presentation-design | 演示设计：视觉层级、信息图表、排版美学、配色方案 | 1.8K | [skills.sh](https://skills.sh/jwynia/agent-skills/presentation-design) |
| presentation-creator | 演示创建：大纲构思、内容组织、Slide 编写、全流程 | 1.8K | [skills.sh](https://skills.sh/getsentry/skills/presentation-creator) |
| ppt-template-creator | PPT 模板：主题定制、母版设计、品牌模板、样式库 | 1.3K | [skills.sh](https://skills.sh/anthropics/financial-services-plugins/ppt-template-creator) |

## 工作流

```
内容构思 ──→ 模板设计 ──→ 视觉呈现
(presentation-creator)  (ppt-template-creator)  (presentation-design)
                                │
                                └──→ 演讲表达
                                     (presentation-delivery)
```

## 安装

```bash
# 安装全部演示技能（推荐）
npx skills add skills-repo/presentation-master -g -y

# 按需安装
npx skills add skills-repo/presentation-master@presentation-delivery -g -y
npx skills add skills-repo/presentation-master@presentation-design -g -y
npx skills add skills-repo/presentation-master@presentation-creator -g -y
npx skills add skills-repo/presentation-master@ppt-template-creator -g -y
```

## 与本组织其他仓库的关系

- **office-master** — 办公效率（格式转换、PPT 自动化），本仓库聚焦演示内容和设计
- **startup-founder** — 创业技能，本仓库聚焦演示呈现
- **visual-designer** — 视觉资产创作，本仓库聚焦演示文稿制作
