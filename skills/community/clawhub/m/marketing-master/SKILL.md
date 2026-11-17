---
name: marketing-master
description: >-
  AI Agent 营销大师技能库：覆盖 SEO 审计与内容营销、高转化文案撰写、内容策略规划、着陆页构建、转化率优化（CRO）、付费广告投放与素材迭代六大能力，让独立开发者与小团队也能专业地推向市场。触发词："SEO"、"关键词研究"、"技术
  SEO"、"文案"、"PAS"、"AIDA"、"StoryBrand"、"着陆页"、"转化率"、"内容策略"、"编辑日历"、"主题集群"、"内容衰减"、"CRO"、"A/B 测试"、"表单转化"、"付费广告"、"ROAS"、"广告素材"、"素材疲劳"。
agent_created: true
metadata:
  version: 1.1.0
  category: 营销
  difficulty: 进阶
  platform: skills-repo
  created: 2026-07-26
  updated: 2026-11-02
  architecture: superpower
tags:
  - marketing
  - seo
  - copywriting
  - content-strategy
  - landing-page
  - paid-ads
---

# Marketing Master 营销大师

> 把 AI 编程助手变成一名覆盖「SEO 审计 → 内容策略 → 文案撰写 → 着陆页构建」全链条的营销搭档。本技能采用 superpower 架构：`SKILL.md` 只做路由，深层方法论放在 `references/`，细粒度能力放在 `skills/` 子技能，按需加载、互不干扰。

## 何时使用

- 需要做 **SEO 审计**：关键词研究、技术 SEO 诊断、竞品与 SERP 分析
- 需要写**高转化文案**：着陆页、广告、邮件，用 PAS / AIDA / StoryBrand 框架
- 需要规划**内容策略**：主题集群、编辑日历、内容衰减检测
- 需要**构建着陆页**：高转化结构、视觉层次、响应式与 CTA 优化
- 需要做 **转化率优化（CRO）**：着陆页/定价页/表单的转化诊断、CTA 文案与信任提升
- 需要投 **付费广告**：平台与预算选型、账户结构、素材工厂与疲劳轮换、指标熔断

## 能力索引（超级技能路由）

本技能采用渐进式加载。`SKILL.md` 仅作路由，**按需**读取下列条目，避免一次性占满上下文。

### 深层 playbook（`references/`，串联与决策）

| 任务 | 读取 | 关键词（grep 线索） |
|------|------|---------------------|
| 全流程技能选型：四种能力怎么串、黄金顺序、从哪开始的决策树、典型陷阱 | [references/growth-channel-matrix.md](references/growth-channel-matrix.md) | growth-channel-matrix, 黄金顺序, 技能选型, 决策树, 关键词聚类, 着陆页骨架 |
| 内容策略方法论：新建/更新/重组决策树、主题集群、编辑日历、内容衰减、分发 | [references/content-strategy-playbook.md](references/content-strategy-playbook.md) | content-strategy-playbook, 主题集群, 编辑日历, 内容衰减, 分发策略 |

### 细粒度子技能（`skills/`，可独立安装调用）

| 任务 | 调用 | 关键词（grep 线索） |
|------|------|---------------------|
| SEO 审计与内容营销：关键词聚类、技术 SEO、竞品分析、内容审计 | [skills/seo-auditor/SKILL.md](skills/seo-auditor/SKILL.md) | seo-auditor, 关键词, 技术SEO, 竞品分析, SERP |
| 高转化文案撰写：PAS/AIDA/StoryBrand 框架的着陆页与广告文案 | [skills/copywriting-pro/SKILL.md](skills/copywriting-pro/SKILL.md) | copywriting-pro, PAS, AIDA, StoryBrand, 文案, CTA |
| 内容策略规划：主题集群、编辑日历、内容衰减检测 | [skills/content-strategist/SKILL.md](skills/content-strategist/SKILL.md) | content-strategist, 编辑日历, 主题集群, 内容衰减 |
| 着陆页构建：高转化结构、视觉层次、响应式、CTA 优化 | [skills/landing-page-builder/SKILL.md](skills/landing-page-builder/SKILL.md) | landing-page, 转化率, Hero, 视觉层次, 响应式 |
| 转化率优化（CRO）：着陆页/定价页/表单的转化诊断、CTA 文案、信任与异议处理 | [skills/cro-optimizer/SKILL.md](skills/cro-optimizer/SKILL.md) | cro-optimizer, CRO, 转化率, 表单转化, A/B测试, 信任标识, 异议处理 |
| 付费广告投放与素材迭代：平台预算选型、账户结构（ABO/CBO）、创意即定向、素材疲劳轮换与指标熔断 | [skills/paid-ads/SKILL.md](skills/paid-ads/SKILL.md) | paid-ads, 付费广告, PPC, ROAS, CAC, CPM, ABO, CBO, 素材疲劳, 熔断 |

> 路由规则：先判断任务属于「获取流量 / 创作内容 / 转化承接」哪一类；纯技术 SEO 调 `seo-auditor`，写词调 `copywriting-pro`，排期调 `content-strategist`，落地页调 `landing-page-builder`，付费买量与素材迭代调 `paid-ads`；需要串联全流程或建立整体方法论时读 `references/` 中的 playbook。

## 可运行脚本（scripts/）

| 脚本 | 用途 | 关键参数 |
|------|------|----------|
| [scripts/editorial_calendar.py](scripts/editorial_calendar.py) | 按主题集群与频率生成 Markdown 编辑日历 | `--pillars --freq --start --weeks` |
| [scripts/decay_score.py](scripts/decay_score.py) | 老文内容衰减打分与更新优先级 | `--title/--days/--drop/--core` 或 STDIN |
| [scripts/keyword_cluster.py](scripts/keyword_cluster.py) | 关键词按意图（信息/商业/交易）聚类 | `--pair "词" "意图"` 或 STDIN |

> 这三个脚本把 references/ 中的方法落成可执行的工具，直接 `python3 scripts/<name>.py --help` 查看用法。

## 适用场景

- 网站 SEO 健康检查与搜索引擎排名优化
- 产品发布/活动推广的文案与着陆页
- 博客/官网的长期内容规划与更新
- 独立开发者以低成本做专业级营销

## 限制

- 付费投放覆盖采买方法论（`paid-ads`），但不代操作广告账户、不直接执行真实预算变更
- 不涉及大规模邮件营销自动化与 B2B 企业级策略
- 文案、SEO 与投放效果依赖产品定位准确性，不替代专业投放决策
