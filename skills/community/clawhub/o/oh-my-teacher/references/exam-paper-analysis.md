# Exam Paper Analysis

Use this file for `/paper-analyze`, past papers, sample finals, question banks, homework sets, and teacher-provided review papers.

## ima Workflow

1. Use `search source=kb` to locate past papers, sample papers, homework, answer keys, and review sheets.
2. Use `fetch` for each concrete paper or answer key before extracting details.
3. Use `subagent_spawn type=research` when there are many papers or long answer keys.
4. Update the course homepage through `ima-note` with the analysis summary.

## Output Contract

```markdown
# 往年题分析

## Evidence Scope
- 已分析资料:
- 来源等级:
- 限制: 基于已导入试卷推断，不代表真实命题。

## 题型分布
| 题型 | 出现次数 | 平均分值 | 典型知识点 | 来源 |
|---|---:|---:|---|---|

## 高频知识点
1.
2.
3.

## Chapter Frequency For Priority Ranking
| Chapter/topic | Paper count | Question types | Typical wording | Linked teacher/scope evidence | Confidence |
|---|---:|---|---|---|---|

## 出题模式
- 

## 扣分模式
- 

## 本周复习策略
- 必练:
- 快速过:
- 暂时降优先级:

## Next Action
```

## Rules

- Never claim real exam prediction certainty.
- Separate uploaded-paper evidence from common-syllabus inference.
- If answer keys are missing, mark grading-pattern conclusions as low confidence.
- For ima, write the final summary to the course homepage or a dedicated paper-analysis note when note tools are available.
