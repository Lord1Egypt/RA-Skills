# Summary components

Use when the user asks for one or more derived artifacts rather than complete minutes.

## Meeting abstract / 会议摘要

Produce a concise paragraph or bullet list covering:

- meeting purpose and context
- top 3–6 discussion points
- decisions/conclusions
- open risks or blockers
- action items if present

Keep it faithful and shorter than source. Do not invent missing decisions.

## Chapter / topic summary / 章节摘要

For each segment:

- title: no more than 15 Chinese characters when possible
- summary: 100–200 Chinese characters, `总-分` or `总-分-总`
- key speakers and positions
- conclusions/actions from the segment

## Speaker summary / 发言人摘要

```markdown
- **发言人/姓名**：
  - 核心观点：...
  - 主要依据/问题：...
  - 建议/承诺/待办：...
  - 与他人的共识或分歧：...
```

Rules:

- Keep each speaker independent.
- Never attribute another speaker's content to this speaker.
- Include all substantive speakers, not just high-frequency speakers.
- Ignore pure acknowledgements like “嗯/好的/明白/谢谢” unless they confirm a decision.

## Title and tags / 标题关键词

Generate:

```json
{"title":"不超过20字","keywords":["关键词1","关键词2","关键词3"]}
```

Rules:

- Title should reflect the core theme, not generic “会议纪要”.
- Keywords should be concrete nouns or short noun phrases from the transcript.
- Avoid names as keywords unless the meeting is centered on the person.

## Quotes / 金句

Only extract memorable statements that are actually present. If no strong quote exists, say none rather than fabricating one.

## Fresh terms / 新鲜词

Extract unusual domain terms, product names, acronyms, or repeated new words. Include a short source-grounded explanation when possible.
