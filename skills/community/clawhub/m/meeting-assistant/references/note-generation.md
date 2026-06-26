# 会议纪要生成 / Note Generation

在 ASR 已经产出结构化会议转写之后，再使用本说明生成摘要、决策和行动项。
Use this guide after ASR has produced a normalized meeting transcript.

## 目标 / Goal

把会议转写整理成可读、可追溯、可导出的会议产物。
Turn transcript segments into meeting artifacts that are useful, auditable, and easy to export.

## 推荐输出内容 / Recommended Outputs

- 摘要 / executive summary
- 议题或讨论要点 / discussion topics
- 已确认的决策 / decisions made
- 风险、阻塞项、待确认问题 / risks or blockers
- 行动项（包含负责人与时间定位） / action items with owner and timestamp
- 完整转写附录或转写链接 / full transcript appendix or reference link

## 输入结构要求 / Input Contract

优先使用包含以下字段的结构化转写。
Prefer a structured transcript with:

- `segments[].speaker`
- `segments[].start`
- `segments[].end`
- `segments[].text`
- `segments[].translation`（如需要双语输出） / when multilingual output is needed
- `duration`
- 可选 `session_id` / optional `session_id`

## 推荐处理步骤 / Suggested Processing Steps

1. 清理文本，但保留时间戳和说话人边界。 / clean transcript text while preserving timestamps and speaker turns
2. 将同一说话人、语义连续的相邻片段做轻度合并。 / merge adjacent segments from the same speaker when they form one thought
3. 根据停顿、话题切换、明确议程词识别主题边界。 / detect topic boundaries by pauses, speaker shifts, or agenda phrases
4. 提取承诺、分工、决策与待办。 / extract explicit commitments, tasks, and decisions
5. 先生成简洁纪要，再按需要附完整转写。 / produce concise notes first, then optionally attach a full transcript

## 行动项提取启发式 / Action Item Heuristics

重点关注带承诺或分配含义的表达，例如：
Look for statements that imply commitment or assignment, for example:

- “我来负责” / “I will” / “我们下周完成”
- “请你跟进” / “Can you follow up”
- “deadline” / “due” / “before Friday” / “下周一前”

每个行动项尽量保留：
For each action item, keep:

- `text`
- `owner`
- `timestamp`
- `source_speaker`
- `due_date`（仅在原文明确提到或高度确定时填写） / only if explicitly stated or clearly inferable

## 推荐 Markdown 结构 / Output Shape

```md
# 会议纪要 / Meeting Notes

## 摘要 / Summary

## 决策 / Decisions
- ...

## 行动项 / Action Items
- [负责人 / Owner] 任务内容（来源时间 / source: 12:34）

## 风险 / 待确认问题 / Risks / Open Questions
- ...

## 完整转写 / Transcript
- [00:15] speaker_0: ...
```

## 双语会议建议 / Multilingual Guidance

- 如果用户要求翻译，优先保留原文转写与目标语言摘要两套信息 / keep both source transcript and translated summary when useful
- 不要让翻译文本覆盖原始发言 / do not overwrite the source-language quote with translated text
- 做双语纪要时，摘要可以用用户指定语言输出，但时间点要始终对应原始转写 / keep source timestamps in bilingual notes

## 可靠性要求 / Safety Guidance

- 要明确区分“原文转写”和“模型总结” / separate verbatim transcript from interpreted summary
- 无法判断负责人的行动项统一标为 `Unassigned` / mark uncertain owners as `Unassigned`
- 不要臆造不存在的结论、负责人或截止日期 / avoid inventing unsupported decisions or deadlines
