# 怎样调研 (how-to-research)

> 从《怎样调研》（任仲然著，党建读物出版社 2019，"机关工作实务丛书"第二本）提炼的 Agent 技能库——不是书的摘要，而是一套可执行的调研方法论工具箱。

## 这是什么

一个 OpenClaw / Claude Code / Copilot CLI / Amp 兼容的 skill 目录，把全书十二讲的调研方法论拆解为：

- **命名框架与原则**——保留作者原话表述（如"蹲'活点'不蹲'死点'"、"求实求真求是导向"、"把握随机调研的四个基调"）
- **可执行的操作步骤**——每讲的方法都写成"何时用 / 怎么做"
- **反面模式**——作者反复警示的错误做法及原因
- **实例拆解**——刘少奇天华调研、陈云青浦调研、寻乌调查、费孝通社会调查等经典案例的压缩重述
- **决策速查表**——把作者的判断逻辑浓缩成一眼可查的规则

双用途设计：

1. **给 AI 用**——执行市场调研、竞品分析、行业研究、用户访谈等任务时，按本 skill 的方法论干活
2. **给自己用**——按讲次或主题快速检索书中观点与方法

## 目录结构

```
how-to-research/
├── SKILL.md              # 核心框架 + 讲次索引 + 主题索引（入口文件）
├── chapters/             # 十二讲逐章拆解（按需加载）
│   ├── ch01-reasons.md                # 第一讲 调研的理由
│   ├── ch02-orientation.md            # 第二讲 调研的导向
│   ├── ch03-preparation.md            # 第三讲 调研的准备
│   ├── ch04-document-research.md      # 第四讲 文献调研
│   ├── ch05-questionnaire-scale-survey.md  # 第五讲 问卷调研和量表调研
│   ├── ch06-sampling-typical-case.md  # 第六讲 抽样调研和典型调研
│   ├── ch07-immersive-fieldwork.md    # 第七讲 蹲点调研
│   ├── ch08-petition-research.md      # 第八讲 信访调研
│   ├── ch09-interview-symposium.md    # 第九讲 谈话调研和座谈会调研
│   ├── ch10-random-research.md        # 第十讲 随机调研
│   ├── ch11-research-report.md        # 第十一讲 调研报告
│   └── ch12-performance-impact.md     # 第十二讲 调研的绩效
├── glossary.md           # 全书术语表
├── patterns.md           # 方法与模式全集
├── cheatsheet.md         # 决策速查表（最实用的一层）
└── README.md
```

## 用法

**Agent 里**（OpenClaw / Claude Code 等，将本目录放入技能目录后）：

- 直接说"用怎样调研这个 skill 做一次竞品调研"→ 加载核心框架
- 问具体主题，如"问卷的答项怎么设置"→ 自动定位到对应讲次细读
- 问"ch07"→ 加载第七讲（蹲点调研）

**人读**：从 [SKILL.md](SKILL.md) 的索引进入，按需点开各讲。

## 生成方式

由 OpenClaw book-to-skill 流水线生成：216 页扫描版 PDF → OCR 全文提取（AutoClaw OCR）→ 结构分析 → 逐章提炼 → 人工校对整合。提炼遵循"提取结构，不抄原文"原则，框架命名保留作者原话。

## 版权说明

本书版权归原作者及出版社（党建读物出版社）所有。本仓库仅包含对书中方法论的提炼与转述（合理使用），不包含原文文本。
