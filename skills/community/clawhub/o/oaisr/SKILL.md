---
name: OAISR
description: |
  OAISR - Occupational AI Displacement Risk | 职业AI替代风险评估

  中文说明：
  职业AI暴露度分析工作流。当用户发送职业名称、询问"XX职业的暴露度"、或提及"AI替代风险"时激活。

  输出标准四步分析报告：
  1. 双进度条（理论暴露度 vs 实际暴露度）
  2. 任务分解表（6~8项核心工作活动的β值与估算）
  3. 综合估算（加权暴露度 + 置信度 + 核心结论）
  4. 可选：应对策略（AI不可替代能力清单）

  数据来源：Anthropic《Labor market impacts of AI》(2026-03-05)
  地址：https://www.anthropic.com/research/labor-market-impacts

  English Description:
  Occupational AI Displacement Risk Assessment. Activated when user sends a job title, asks about "AI exposure risk of XX profession", or mentions "AI replacement risk".

  Standard 4-Step Analysis Output:
  1. Dual progress bars (theoretical vs actual exposure)
  2. Task breakdown table (6-8 core work activities with β values)
  3. Comprehensive estimate (weighted exposure + confidence + key conclusion)
  4. Optional: Coping strategies (AI-irreplaceable capability清单)

  Data Source: Anthropic《Labor market impacts of AI》(2026-03-05)
---

# OAISR - 职业AI替代风险评估
## OAISR - Occupational AI Displacement Risk

## 名称定义 | Name Definition

**OAISR** = Occupational AI Displacement Risk（职业AI替代风险指数）

## 激活条件 | Activation

满足以下任一条件时激活：
- 用户发送职业名称（如"律师"、"产品经理"）
- 用户询问"XX职业的暴露度"
- 用户提及"AI替代风险"、"哪些工作会被AI取代"

Activates when:
- User sends a job title (e.g., "lawyer", "product manager")
- User asks about "XX profession's AI exposure"
- User mentions "AI replacement risk" or "which jobs will be replaced by AI"

## 输出格式：四步出图法 | Output: 4-Step Analysis

### 第一步：双进度条 | Step 1: Dual Progress Bars

```
理论暴露度（Theoretical）  [█████░░░░░]  0.52
实际暴露度（Actual）       [███░░░░░░░]  0.31
```

- 进度条使用方括号`[░░░░░░░░░░]`包裹，清晰区分已填/未填部分
- 数字标注在进度条右侧（0.00~1.00）
- 禁用emoji
- Use brackets to clearly separate filled vs empty portions
- Number shown to right of bar (0.00~1.00)
- No emoji

### 第二步：任务分解表 | Step 2: Task Breakdown Table

| 任务名称 | 理论值 | 实际值 | 估算依据 |
|---------|--------|--------|----------|
| 任务A | β=0.xx | 0.xx | 报告原文/类比推断/经验系数 |
| 任务B | β=0.xx | 0.xx | ... |
| ...（共6~8项） | | | |

### 第三步：综合估算 | Step 3: Comprehensive Estimate

- **加权综合暴露度**：理论 X.XX / 实际 X.XX
- **置信度**：高/中/低（标注适用范围）
- **核心结论**：一句话总结

- **Weighted Exposure**: Theoretical X.XX / Actual X.XX
- **Confidence**: High/Medium/Low (with scope note)
- **Key Conclusion**: One-sentence summary

### 第四步：应对策略（按需提供）| Step 4: Coping Strategies (Optional)

```
AI不可替代能力清单：
1. 复杂问题解决能力：跨领域难题拆解与方案设计
2. 深度沟通协调能力：需求洞察、情绪理解与资源协调
3. 从0到1的创造能力：新理论、产品或艺术形式的原创
4. 责任与决策能力：风险承担与不确定性环境下的判断
5. AI背书能力：对AI输出结果的质量把控与责任承担
```

## 数据来源 | Data Sources

| 指标 | 来源 | 说明 |
|------|------|------|
| 理论暴露度(β) | Eloundou et al. 2023 | 基于任务结构的自动化可行度（1=完全可行，0=不可行） |
| 实际暴露度 | Anthropic Economic Index | 真实 labor market 流量数据 |

Source: https://www.anthropic.com/research/labor-market-impacts

## 估算方法论 | Methodology

1. **任务拆解**：将目标职业拆解为5~8项核心工作活动（LAT）
2. **理论赋值**：参考β值逻辑，为每项活动赋值（0.0~1.0）
3. **实际赋值**：参考Economic Index真实流量数据
4. **加权综合**：按任务耗时占比加权平均

1. **Task Decomposition**: Break down profession into 5-8 core work activities (LATs)
2. **Theoretical Assignment**: Reference β values, assign 0.0-1.0 per activity
3. **Actual Assignment**: Reference Economic Index real traffic data
4. **Weighted Aggregation**: Weight by task time consumption

## 数据空白处理 | Handling Data Gaps

- 无直接对应任务 → 参考同类任务估算
- 实际无数据 → 理论值 × 0.5~0.6 经验系数

- No direct match → Estimate by analogy
- No actual data → Theory × 0.5-0.6 experience coefficient

## 透明度要求 | Transparency Requirements

- 每项估算**必须标注依据**（报告原文/类比推断/经验系数）
- 注明"基于方法论估算，非原始数据"

- Every estimate **must cite basis** (report原文/analogy/inference)
- Note "Estimated based on methodology, not raw data"

## 重要认知 | Key Insight

> **AI替代任务，非职业。** 高暴露度 = 部分可自动化 ≠ 职业消失。

> **AI replaces tasks, not occupations.** High exposure = partial automation ≠ job disappearance.
