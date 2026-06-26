# 示例会话（中文）

## 用户输入

```text
请用这个 skill 训练我读论文。先生成精度报告，再开始提问。
论文：Semi-supervised Decentralized Personalized Federated Learning
```

## 理想输出骨架

# Precision Report

## Session Metadata
- Session ID: 2026-04-20-demo-01
- Date: 2026-04-20
- Language: 中文
- Paper: Semi-supervised Decentralized Personalized Federated Learning
- Source type: PDF + LaTeX
- Prior learning state detected: no

## Prior-State Carryover
- Strongest retained dimensions: 无
- Weakest retained dimensions: 无
- Recurring error patterns: 无
- Recommended starting difficulty: 中等

## Pre-Question Diagnostic Hypothesis
- Reading risk: 容易停留在“半监督 + 去中心化 + 个性化联邦学习”几个关键词层面，但不能精确还原问题设定。
- Thinking risk: 可能能说出 motivation，但未必能解释为什么作者这样分解模块或损失项。
- Methodology risk: 可能会复述实验结果，却说不清每个实验块到底在验证什么。
- Most likely weak dimensions this session:
  - Method reconstruction
  - Claims-evidence alignment
  - Scientific methodology awareness

## Initial Mastery Snapshot (Hypothesis)
| Dimension | Score (0–5) | Confidence | Notes |
|---|---:|---:|---|
| Problem understanding | 2.5 | 0.45 | 题目较长，概念负荷高 |
| Title-to-content interpretation | 2.0 | 0.40 | 多概念耦合，容易混淆 |
| Related-work relation mapping | 2.0 | 0.35 | 需要跨 PFL / semi-supervised / decentralized |
| Method reconstruction | 1.8 | 0.35 | 高风险项 |
| Formula / theorem interpretation | 1.8 | 0.30 | 高风险项 |
| Experiment interpretation | 2.0 | 0.35 | 高风险项 |
| Claims-evidence alignment | 1.8 | 0.30 | 高风险项 |
| Weakness and limitation detection | 2.0 | 0.35 |  |
| Future-direction generation | 2.5 | 0.30 |  |
| Scientific methodology awareness | 1.8 | 0.30 | 高风险项 |

## Planned Question Mix
- Total questions: 8
- Single-choice: 2
- Multi-select: 2
- Short-answer: 3
- Evidence retrieval: 1
- Critique / frontier: 1

## Session Targets
- Dimension(s) to probe first: 问题理解、方法重建
- Dimension(s) to strengthen by end of session: 实验解读、claim-evidence 对齐
- What improvement would count as success today: 能清楚说出论文究竟解决什么、核心模块如何配合、实验块分别验证什么

---

## Question 1 (Single-choice)
这篇论文最核心要解决的问题是什么？

A. 如何在中心服务器上提升全局模型精度
B. 如何在没有中心服务器的个性化联邦学习中，同时利用未标注数据并保持个体模型适配性
C. 如何把监督学习完全替换为无监督聚类
D. 如何降低 GPU 显存占用

## 用户回答

```text
B
```

## Feedback
- Judgment: Correct
- What you got right: 抓住了“无中心服务器 + 个性化 + 未标注数据利用”这三个核心约束。
- What is missing or mistaken: 还缺少“为什么这些约束同时出现会使问题更难”的解释。
- Evidence from the paper: 论文的问题设定不是普通 FL，也不是普通半监督学习，而是多约束叠加场景。
- Weakness tag(s): RP-2, ST-1
- Updated micro-score: Problem understanding +0.5

## Learning State Delta
- Dimension changes: Problem understanding 2.5 -> 3.0
- Recurring pattern: 能抓住主旨，但解释难点来源时仍偏粗略
- Next question rationale: 继续追问方法层，确认不是只会读标题

---

## End-of-Session Update

# Updated Learning State

## Current Macro Scores
- Reading: 2.8
- Thinking: 2.3
- Methodology: 2.1

## Recurring Error Patterns
- 容易先讲 motivation，后讲不清模块之间如何配合
- 实验结果能复述，但实验目的拆解不够细
- 能指出不足，但改进建议还不够 paper-grounded

## Recommended Next Session
- Target paper difficulty: 中等偏上
- Target dimensions: Method reconstruction, Claims-evidence alignment, Scientific methodology awareness
- Suggested question mix: short-answer + evidence retrieval + one frontier question
- Suggested session length: 6 questions

## Resume Note
下次对话应直接读取该 learning state，从 “Method reconstruction” 的迁移性复测题开始，而不是重新做最基础的题。
