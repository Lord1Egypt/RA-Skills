# Full meeting minutes JSON

Use for formal meeting minutes, task tables, or machine-readable output.

## Process

- Correct clear ASR mistakes and remove repeated/noisy content.
- Infer a concise meeting topic from the full transcript; keep it under 20 Chinese characters when possible.
- Group scattered content into agenda topics.
- For each topic, preserve enough detail to explain problems, discussion, decisions, and next steps.
- Pay special attention to task assignment, problem discussion, answers, conclusions, consensus, deadlines, and owners.

## Output schema

Output strict JSON only:

```json
{
  "topic": "不超过20字的会议主题",
  "time": "会议时间；原文未涉及时写原文未涉及",
  "person": "发言人0,发言人1 或真实姓名列表",
  "agenda": "议题1,议题2,议题3",
  "minutes": "Markdown 字符串，按议题整理",
  "todoTask": [
    {"task": "具体任务", "owner": "责任人或未明确责任人", "time": "时间节点或未明确时间"}
  ]
}
```

## `minutes` field structure

```markdown
**议题1：议题标题**
**主要需求、观点、问题**
1. ...

**解决方案/结论**
1. ...；若未确定，写“问题未解决”。

**任务分配与时间节点**
- 责任人：具体任务（时间节点）

---
```

## Missing information

- Missing time: `原文未涉及`
- Missing participants: use speaker ids.
- Missing owner: `未明确责任人`
- Missing deadline: `未明确时间`
- No resolved answer: `问题未解决`
