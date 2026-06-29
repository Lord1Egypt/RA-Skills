# Wrong Question Notes

Use this file for `/wrong-note` and for wrong-answer follow-up after `/grade`, `/quiz`, or `/mock`.

## ima Workflow

1. Start from a graded answer or wrong quiz/mock item.
2. Generate a note-native wrong-question entry.
3. Use `ima-note` to create or update the wrong-question note when available.
4. Use `memory_write` only for a durable summary: course, topic, error category, next review.
5. Update the SRS table in the course homepage or output a copyable table fallback.

## Wrong Note Template

```markdown
# 错题：[topic]

## 题目

## 我的错误答案

## 正确答案

## 错因分类
- [ ] 概念不清
- [ ] 条件遗漏
- [ ] 公式记错
- [ ] 计算错误
- [ ] 方法选择错误
- [ ] 审题错误
- [ ] 表达不规范

## 最小错误点

## 修复说明

## 变式题
1. 基础题
2. 变式题
3. 综合题

## 下次复习
- Next Review:
- Difficulty:
- Tags: #错题 #[课程名] #[topic]
```

## Error Taxonomy

Classify every wrong item into exactly one primary category (add a secondary only if clearly needed). Use this fixed set so categories aggregate cleanly across notes:

- `概念不清` — concept misunderstood
- `条件遗漏` — missing/forgotten condition or assumption
- `公式记错` — wrong formula/definition recalled
- `计算错误` — arithmetic/algebra slip with correct method
- `方法选择错误` — chose the wrong approach
- `审题错误` — misread the question/requirements
- `表达不规范` — correct idea, lost points on rigor/notation/presentation

These align with the error categories in `references/practice-workflows.md` → Error Repair. Keep the exact labels — analytics below depends on them.

## Error-Type Analytics

Wrong notes are not just per-item records; their categories aggregate into a diagnosis. When the student has several wrong notes, count categories and surface the distribution so review targets the *kind* of mistake, not just individual topics:

```markdown
## 错误类型分布（近 N 题）
| 错因 | 次数 | 占比 | 行动 |
|---|---|---|---|
| 条件遗漏 | 6 | 40% | 每道证明先列条件清单 |
| 计算错误 | 4 | 27% | 限时计算专练 + 复核步骤 |
| 概念不清 | 3 | 20% | /explain + /feynman |
| 方法选择错误 | 2 | 13% | 交错练习强化题型识别 |
```

Use this in `/dashboard` and `/summary`. A dominant category changes the plan: e.g. 40% 条件遗漏 means drilling more problems helps less than a "list conditions first" habit. Mark the conclusion as derived from the available notes, not certainty.

## Output After Creation

Return:

- wrong-note title
- topic
- error category
- next review
- one immediate repair drill
- whether ima-note and memory_write succeeded, or a Markdown fallback if not
