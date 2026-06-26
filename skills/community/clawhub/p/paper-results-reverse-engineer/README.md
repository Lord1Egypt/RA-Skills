# Paper Results Reverse Engineer (v3.0.4)

拆解和学习心理学论文 Results 部分的写作逻辑。Results 不是数据堆砌，而是有章可循的叙事——这个 skill 做的就是把这套叙事拆开来给你看。

## 适用场景

- 贴入一篇论文的 Results 全文或部分段落
- 上传论文 PDF 文件
- 提供图表 caption + 对应的结果段落
- 上传图表截图
- 给出摘要 + 方法 + 结果
- 询问："拆这篇结果部分" / "这张图怎么讲" / "这个段落在写什么"
- 需要从已发表的 Results 中提取写作策略
- 需要制作 PPT 汇报讲稿
- 需要检查统计报告的规范性

**覆盖领域：** 认知 / 社会 / 人格 / 发展 / 教育 / 临床 / 心理测量 / 认知神经科学 / fMRI / EEG / 元分析 / 质性研究 / 混合方法 / 方法学 / 模拟。

## 输出模式

| 模式 | 触发方式 | 输出内容 |
|------|---------|---------|
| **quick（快速）** | "快速看一下" / "大概拆一下" | Study Profile + Module B（结构地图）+ Module D（核心图表）+ Module E（证据边界）+ 自检。不含 Module C 和 F。 |
| **standard（标准，默认）** | 不指定模式 / "正常生成" | 完整 Study Profile + Module A–G。Module C：段落/聚类级拆解（每段 2–4 个聚类）。Module F：PPT 页建议 + 一句话讲稿 + 证据边界（不含完整讲稿）。 |
| **close-reading（精读）** | "逐句拆解" / "完整精读" / "做 PPT" / "汇报讲稿" | 最大深度完整 A–G。Module C：逐句标注。Module F：完整逐字讲稿 + Q&A + 备用 slide。长论文可分阶段执行。 |

所有模式均采用 **file-first 输出**：完整分析写入 Markdown 文件，聊天框仅返回文件路径 + 3–5 个核心发现 + 自检 + 人工复核项。

## Module H：写作迁移包

当你需要借鉴目标论文的 Results 写作风格来写自己的 Results（配合 `academic-results-writer`），Module H 会生成一个压缩版迁移包，包含：

- 研究设计迁移摘要及兼容性评估
- 结果组织模板，含可迁移性评级（可迁移 / 部分可迁移 / 不可迁移）
- 段落和图表的叙事模式（抽象提取，不复制原文）
- Results–Discussion 边界指南
- 风险标记及迁移决策
- 推荐的 writer 模式

## 推荐上手 Prompts

### Quick 模式

请使用 paper-results-reverse-engineer，quick mode，快速拆解这篇论文 Results。只输出 Study Profile、Module B、核心图表、Module E 证据边界和简短自检。聊天框只返回文件路径、核心发现、自检和人工复核项。

### Standard 模式

请使用 paper-results-reverse-engineer，standard mode，分析这篇论文 Results。输出完整 A–G，Module C 使用段落/cluster 级拆解，Module F 只给 PPT 页建议、一句话讲稿和证据边界。聊天框只返回文件路径、3–5 个核心发现、自检和人工复核项。

### Close-reading 模式

请使用 paper-results-reverse-engineer，close-reading mode，用于课堂汇报。Module C 必须逐句拆解 Results，Module D 必须详细讲解核心图表，Module F 必须生成完整 PPT 汇报讲稿、可能 Q&A 和备用 slide 建议。必须区分 Results 直接结果、Discussion 解释和 skill 教学性说明。

### Module H 写作迁移包

请使用 paper-results-reverse-engineer，为这篇目标文献生成 Module H Writer Transfer Packet，供 academic-results-writer 使用。只提取 Results 结构、段落功能、图表叙事方式和可迁移写作模式；不要复制目标文献句子、统计值或结论。

## 快速示例

**输入：** 贴入一篇问卷中介效应论文的 Results 全文。

**输出（standard 模式）：**
- `outputs_md/reverse_engineer/Li_2021_Results_Reverse_Analysis.md`
- 聊天框：文件路径 + 4 个核心发现 + 自检 + 人工复核项

详见 `examples/` 中各模式的完整示例。

## 安全原则

1. **本 skill 是分析，不是复制。** 所有输出均为分析性拆解，不是对目标论文的复现。
2. **强制因果语言护栏。** 明确区分不同研究设计可以主张和不可主张的因果结论。
3. **反模板污染检查。** 防止前一篇论文的分析残留污染新分析。
4. **来源验证。** 将生成的断言与原始论文文本对照验证，而非与自身生成内容比照。
5. **Module H 绝不包含目标论文的统计数据。** 仅供 writer 参考写作模式。

## 目录结构

```
paper-results-reverse-engineer/
├── SKILL.md                 # skill 主定义
├── README.md                # 本文件
├── CHANGELOG.md             # 版本记录
├── docs/                    # 各分支详细规则
│   ├── branch-a-b-c-d-e-f.md
│   ├── branch-g-meta-analysis.md
│   ├── branch-h-qualitative.md
│   ├── branch-i-simulation.md
│   ├── execution-constraints.md
│   ├── anti-template-contamination.md
│   ├── source-verification.md
│   ├── causal-language-guardrails.md
│   └── module-h-spec.md
├── examples/                # 各模式示例
│   ├── quick.md
│   ├── standard.md
│   ├── close-reading.md
│   └── module-h-bridge.md
├── references/              # 参考材料
│   ├── examples.md
│   ├── function-labels.md
│   └── prompt-templates.md
└── tests/                   # 内部测试用例
```

## 版本

- **公开版本：** 3.0.4
- **内部版本：** psychology-results-reverse-analysis-v3.0.4-bridge
- **适用范围：** 心理学全子领域文献
