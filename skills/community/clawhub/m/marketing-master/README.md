# 营销大师技能库

> AI Agent Skills for Marketing —— 覆盖 SEO 审计、文案撰写、内容策略、着陆页构建、转化率优化与付费广告投放

## 定位

为独立开发者和小团队提供一套可安装的 AI Agent 营销技能，让 Claude Code 成为你的营销搭档。

## 核心理念

> 好产品需要好营销。用 AI 降低营销门槛，让独立开发者也能专业地推向市场。

- **数据驱动**——从关键词研究到转化率优化，每个决策有数据支撑
- **框架优先**——PAS/AIDA/StoryBrand 等成熟框架，降低创意门槛
- **一站完成**——从策略规划到落地执行，覆盖营销全链条

## 技能清单

| 环节 | 技能 | 描述 | 来源 |
|------|------|------|------|
| 🔍 SEO 审计 | `seo-auditor` | SEO 与内容营销：关键词聚类、技术 SEO、竞品分析、SERP 追踪 | [衍生](https://skills.sh/aradotso/marketing-skills/seo-content-marketing-claude-skills) |
| ✍️ 文案撰写 | `copywriting-pro` | 营销文案：PAS/AIDA/StoryBrand 框架，着陆页、广告文案 | [衍生](https://skills.sh/onewave-ai/claude-skills/landing-page-copywriter) |
| 📅 内容策略 | `content-strategist` | 编辑日历、主题集群设计、内容衰减检测、分发策略 | [衍生](https://skills.sh/agricidaniel/claude-blog/blog-calendar) |
| 🎯 着陆页 | `landing-page-builder` | 着陆页构建：高转化结构、视觉层次、响应式布局、CTA 优化 | [衍生](https://skills.sh/nexu-io/open-design/copywriting) |
| 📈 转化率优化 | `cro-optimizer` | 转化率优化（CRO）：着陆页/定价页/表单转化诊断、CTA 文案、信任与异议处理 | [衍生](https://github.com/coreyhaines31/marketingskills/tree/main/skills/cro) |
| 💸 付费广告 | `paid-ads` | 付费流量采买与素材迭代：平台预算选型、账户结构（ABO/CBO）、创意即定向、素材疲劳轮换与指标熔断 | [衍生](https://github.com/coreyhaines31/marketingskills/tree/main/skills/ads) |

## 快速开始

```bash
npx skills add skills-repo/marketing-master@seo-auditor -g -y
npx skills add skills-repo/marketing-master@copywriting-pro -g -y
npx skills add skills-repo/marketing-master@content-strategist -g -y
npx skills add skills-repo/marketing-master@landing-page-builder -g -y
npx skills add skills-repo/marketing-master@cro-optimizer -g -y
npx skills add skills-repo/marketing-master@paid-ads -g -y
```

## 推荐工作流

```
SEO 审计 → 内容策略 → 文案撰写 → 着陆页构建
seo-       content-     copywriting-  landing-
auditor    strategist   pro           page
                                   builder
```

## 许可

MIT

## 安装 / Install

整库安装（含全部 6 个子技能）与单技能安装命令如下，按需在终端执行：

```
npx skills add skills-repo/marketing-master -g -y
npx skills add skills-repo/marketing-master@seo-auditor -g -y
```

> 把 `@seo-auditor` 换成任意子技能目录名即可单独安装：`seo-auditor`、`copywriting-pro`、`content-strategist`、`landing-page-builder`、`cro-optimizer`、`paid-ads`。

## 子技能索引

| 子技能 | 说明 |
|--------|------|
| seo-auditor | SEO 与内容营销：关键词聚类、技术 SEO、竞品分析、SERP 追踪 |
| copywriting-pro | 营销文案：PAS/AIDA/StoryBrand 框架，着陆页、广告文案 |
| content-strategist | 编辑日历、主题集群设计、内容衰减检测、分发策略 |
| landing-page-builder | 着陆页构建：高转化结构、视觉层次、响应式布局、CTA 优化 |
| cro-optimizer | 转化率优化（CRO）：着陆页/定价页/表单转化诊断、CTA 文案、信任与异议处理 |
| paid-ads | 付费广告投放与素材迭代：平台预算选型、账户结构、创意即定向、疲劳轮换与指标熔断 |
