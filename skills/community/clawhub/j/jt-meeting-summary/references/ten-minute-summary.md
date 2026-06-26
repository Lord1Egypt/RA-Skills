# Ten-minute / long-meeting summary

Use for “十分钟纪要”, long transcripts, periodic summaries, or compressed long-meeting summaries.

## Core goal

Produce a structured long-form summary with faithful topic grouping, decisions, risks, and action items. If the transcript is too short, summarize what exists instead of forcing a long structure.

## Rules

- Group by coherent content, not mechanically every 10 minutes unless requested.
- Preserve chronological development for long meetings.
- For each group, identify: topic, key points, speaker positions, decisions, blockers, and next steps.
- Filter greetings, filler, repeated ASR fragments, and low-information acknowledgements.
- If content is sparse or mostly noise, return a short honest summary.

## Suggested output

```markdown
## 一、会议概览
- 主题：...
- 参会人：...
- 核心结论：...

## 二、分段/分主题纪要
### 1. 话题：...
- 时间范围：...
- 讨论要点：...
- 关键发言：...
- 结论/决策：...
- 风险/待确认：...

## 三、行动项
| 任务 | 负责人 | 时间 | 来源/备注 |
|-|-|-|-|
| ... | ... | ... | ... |

## 四、整体结论
- ...
```

When strict JSON is requested, adapt the same fields into valid JSON only.
