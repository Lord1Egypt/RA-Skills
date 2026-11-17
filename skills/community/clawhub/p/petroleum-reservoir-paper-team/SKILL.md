---
name: petroleum-reservoir-paper-team
title: 石油工程油藏论文写作专家团（部署器）
description: 一键将「石油工程油藏论文写作专家团」安装到 WorkBuddy 专家目录并注册。该专家团面向石油工程油藏方向科研人员，八角色协作覆盖选题、调研、写作、事实核查、风格打磨、审稿与排版全流程，内置 OnePetro/CNKI/SCI 等数据库清单与核心期刊审稿标准。当用户要求安装、部署或使用该专家团时加载本技能。
categories:
  - Research
  - Knowledge
  - Productivity
keywords:
  - petroleum-engineering
  - reservoir-engineering
  - academic-writing
  - research-collaboration
  - paper-review
agent_created: true
---

# 石油工程油藏论文写作专家团 · 部署技能

本技能把内置的 **石油工程油藏论文写作专家团** 部署到当前用户的 WorkBuddy 专家目录，使其出现在「专家中心 → 我的专家」中，可立即使用。

## 专家团构成

| 角色 | 名字 | 职责 |
|------|------|------|
| 资深主编（主理人） | 周审稿 | 统筹调度、质量终审、审稿评级 |
| 选题策划 | 赵选题 | 挖掘高价值油藏方向论文选题 |
| 调研专家 | 张素材 | 检索 OnePetro/EI/Scopus/CNKI 等数据库 |
| 知识管家 | 王整理 | 整合多平台笔记为知识库 |
| 写手 | 李文章 | 撰写结构完整的学术论文初稿 |
| 事实核查专家 | 吴查查 | 核对数据、引用、公式与实验细节 |
| 风格打磨师 | 刘风格 | 统一个人学术表达风格 |
| 排版设计师 | 陈排版 | 图表、引用与期刊格式规范 |

## 何时使用

- 用户说「安装/部署油藏论文专家团」「加载石油工程论文写作团队」「使用石油工程油藏论文写作专家团」。
- 用户已安装本技能后，首次需要把专家团落到本地专家目录。

## 部署步骤（必做）

**运行自带部署脚本**，它会把 `assets/petroleum-reservoir-paper-team/` 复制到
`$WORKBUDDY_CONFIG_DIR/plugins/marketplaces/my-experts/plugins/`（默认 `~/.workbuddy/...`），
并向 `marketplace.json` 注册。脚本幂等，可重复运行。

```bash
# 用任意 Python 3 运行（仅标准库，无需安装依赖）
python3 "<本技能目录>/scripts/deploy_expert.py"
```

> 说明：`<本技能目录>` 即本 SKILL.md 所在目录。脚本会自动定位 `assets/` 与目标专家目录。

## 部署后

1. 提示用户：在 WorkBuddy 左侧「专家」→「我的专家」中即可看到「石油工程油藏论文写作专家团」。
2. 用户可直接发起对话，例如：
   - 「基于深度学习压裂停泵压力去噪方向，推荐3个有创新性的论文选题」
   - 「整理我的研究笔记，生成一份油藏方向论文大纲」
   - 「审阅这篇油藏工程论文初稿，按核心期刊标准给出修改意见」

## 备注

- 专家团为 Team 型，运行需 WorkBuddy 具备多 Agent 协作能力（能跑子 Agent 流程）。
- 卸载：删除 `~/.workbuddy/plugins/marketplaces/my-experts/plugins/petroleum-reservoir-paper-team/` 并从 `marketplace.json` 移除对应条目即可。
