---
name: ppt-template-creator
description: PPT 模板：主题定制、母版设计、品牌模板、样式库
source:
  type: derived
  repo: skills-repo/presentation-master
  path: skills/ppt-template-creator/SKILL.md
  url: https://skills.sh/anthropics/financial-services-plugins/ppt-template-creator
  version: 1.0.0
  updated: 2026-07-31
metadata:
  author: hope
  category: 演示
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-31
tags:
  - powerpoint
  - template
  - slide-master
  - branding
  - theme
---

# PPT Template Creator — PPT 模板制作

> 创建专业的 PowerPoint/Keynote 模板，覆盖主题定制、母版设计、品牌模板和样式库，一次设计多次复用。

## 能力

- **主题定制**：设计配色方案、字体组合、背景样式，创建统一视觉主题
- **母版设计**：Slide Master 布局设计，包括标题页、内容页、图表页、结束页
- **品牌模板**：集成 Logo、品牌色、字体系统，确保品牌一致性
- **样式库**：预设文本框、表格、图表、图片的默认样式，减少重复调整
- **多格式输出**：支持 PPTX、Keynote、Google Slides 格式的模板导出

## 使用方式

在 Claude Code 中使用 `/ppt-template-creator` 调用。

```
/ppt-template-creator 为我的 SaaS 产品设计一套品牌 PPT 模板
/ppt-template-creator 创建一套适合技术分享的简洁模板
/ppt-template-creator 设计一套包含图表和表格的专业模板
/ppt-template-creator 帮我把公司 VI 规范应用到 PPT 模板中
```

## 工作流

1. **需求收集** — 确定模板用途、品牌元素和 Slide 类型需求
2. **视觉设计** — 设计配色、字体、背景和装饰元素
3. **母版布局** — 创建 Slide Master 和 Layout，定义占位符位置
4. **样式预设** — 配置文本框、表格、图表的默认样式
5. **模板测试** — 用实际内容填充模板，验证可用性和视觉效果

## 适用场景

- 公司品牌 PPT 模板的创建和标准化
- 创业者准备路演模板
- 自由职业者建立个人品牌演示模板
- 团队统一演示文稿的视觉风格

## 限制

- 仅提供模板设计指导，不直接生成 PPTX 文件
- 复杂动画和转场效果需手动配置
- 不同演示软件（PowerPoint/Keynote）的模板兼容性有限
- 品牌规范的深度设计参考 visual-designer 仓库

## 相关参考（Playbook）

- [visual-design-principles](../../references/visual-design-principles.md)：§13 母版与主题系统、字号阶梯（≤4 档）、12 列栅格，直接对应「母版设计 / 主题定制」。
- [slide-content-rules](../../references/slide-content-rules.md)：标题层级统一、要点化规则，可固化为模板内置样式。
- 相关资产：[assets/presentation_rules.json](../../assets/presentation_rules.json)（阈值可写为模板默认样式）。