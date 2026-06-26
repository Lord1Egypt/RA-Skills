# NextFromKnowledge Release Notes

## Short Description

把知识、笔记、调研和图谱结果，直接转成下一步动作、计划、决策或最小实验。

## Marketplace Card Copy

Title:
- NextFromKnowledge

Short description:
- 知识行动官，把知识和图谱结果直接推进成下一步动作、计划或决策

Install hook:
- 不是继续总结知识，而是把“知道了很多”推进到“现在该做什么”

## Announcement Copy

NextFromKnowledge 这条线，不是再做一个总结器。

它要解决的是一个更真实的问题:
- 笔记看完了，然后呢
- 调研做完了，然后呢
- 知识图谱出来了，然后呢

这一版把事情收敛到 5 个高价值结果:
- 给出直接的下一步动作
- 给出短周期行动计划
- 在几个方向之间做出判断
- 设计最小可验证实验
- 只指出真正会改变决策的信息缺口

它和 Knowledge Connector 是天然上下游:
- Knowledge Connector 负责 connect knowledge
- NextFromKnowledge 负责 decide the next move

## Suggested Tags

- latest
- knowledge
- action
- planning
- decision
- productivity

## Suggested Repo Name

- `openclaw-skill-next-from-knowledge`

## Publish Command

```bash
clawhub publish /absolute/path/to/next-from-knowledge \
  --slug next-from-knowledge \
  --name "NextFromKnowledge" \
  --version "1.0.0" \
  --changelog "Initial release of NextFromKnowledge: turn notes, research, and knowledge graph outputs into the next action, plan, decision, or experiment." \
  --tags "knowledge,action,planning,decision,experiment,productivity"
```
