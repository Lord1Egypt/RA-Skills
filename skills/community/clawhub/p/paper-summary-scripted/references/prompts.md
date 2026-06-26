# Prompt mapping

Use these variables conceptually when reproducing the Dify workflow:

- `language`: requested output language
- `cleaned_text`: cleaned paper text extracted from the original source
- `summary_text`: generated summary version
- `detailed_text`: generated detailed version
- `contribution_text`: generated contribution extraction

## Summary version

```text
你是一位严谨的计算机科学审稿人。请严格基于以下论文内容生成“摘要版”。一定要生成{{language}}版。

要求：
1. 必须包含三要素：原版题目、研究背景痛点、核心方法名称、主要实验结果（至少一个关键数字）。
2. 禁止添加原文未提及的评价性词汇（如“卓越的”、“开创性的”），只陈述事实。
3. 如果原文中未明确给出实验结果，请注明“原文未提供具体实验数据”。
4. 不要有“好的，已根据您提供的论文内容，生成**版摘要”这种废话。

论文内容：
{{cleaned_text}}
```

## Detailed version

```text
请生成“详细版”摘要。一定要生成{{language}}版。不要有“好的，已根据您提供的论文内容，生成**版摘要”这种废话。必须使用以下结构：

### 1. 背景与动机
简述研究背景、现有问题、本文目标。

### 2. 核心方法
详细描述模型架构、算法流程、创新点。如有公式或算法伪代码，请简要概括。

### 3. 实验设置
- 数据集：列出所有使用的数据集及其划分方式。
- 基线模型：列出对比的方法。
- 评价指标：使用的指标。

### 4. 主要结果与消融实验
- 主要结果：与基线对比的表格数据（若原文有）。
- 消融实验：关键组件的影响分析（若原文有）。

### 5. 局限性（若有）
若原文讨论了方法的不足，请摘录。

论文内容：
{{cleaned_text}}
```

## Contribution extraction

```text
请提炼本文的“学术贡献”。一定要生成{{language}}版。输出格式如下：

- **贡献 1**：[具体创新点]
  支撑依据：[引用原文段落或页码]
- **贡献 2**：[具体创新点]
  支撑依据：[引用原文段落或页码]
...

注意：
1. 每个贡献必须是独立的创新点，而非实验观察结果。
2. 支撑依据必须从原文中直接摘录或概括，不能凭空捏造。
3. 不要有“好的，已根据您提供的论文内容，生成**版摘要”这种废话。

论文内容：
{{cleaned_text}}
```

## Quality judgment

```text
请分别检查以下三个生成内容与原文的一致性：
原文：{{cleaned_text}}
1. 摘要版：{{summary_text}}
2. 详细版：{{detailed_text}}
3. 贡献提炼：{{contribution_text}}

对每个输出给出评分（1-5）和错误列表。
```

## Execution rule

The quality judgment stage must be called only after the summary, detailed, and contribution stages have all completed. Its input includes all three generated outputs plus the original cleaned text.
