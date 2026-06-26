---
name: jt-meeting-summary
description: Pure prompt guidance for generating faithful meeting and call summaries. Use when the model should summarize transcripts into meeting minutes, concise summaries, ten-minute summaries, speaker summaries, action items, titles/tags, or visual-summary prompts without calling external APIs or tools.
---

# JT Meeting Summary

## Purpose

Guide the model to generate faithful, structured summaries from meeting or call transcripts. This skill is instruction-only: do not call external APIs, internal services, workflow endpoints, or retrieval tools unless the user separately asks for them.

## Mode selection

Choose exactly one primary mode:

| User asks for | Use |
|-|-|
| 会议纪要、完整纪要、任务表、todo、JSON 输出 | `references/full-minutes-json.md` |
| 简约纪要、会议总结、Markdown 纪要、普通总结 | `references/concise-minutes.md` |
| 十分钟纪要、长会分段总结、按时间段总结 | `references/ten-minute-summary.md` |
| 通话记录总结、电话录音总结 | `references/call-summary.md` |
| 会议摘要、章节摘要、发言人摘要、标题/关键词、金句、新鲜词 | `references/summary-components.md` |
| 漫画总结、图片总结、视觉总结、文生图提示词 | `references/visual-summary-prompt.md` |

If ambiguous, default to `concise-minutes.md`. If the user needs downstream parsing, choose `full-minutes-json.md`.

## Universal workflow

1. Read the full transcript and identify time markers, speakers, utterances, and any meeting metadata.
2. Normalize only obvious ASR errors when context is clear. Do not invent missing names, roles, dates, numbers, decisions, or causes.
3. Remove duplicate, filler, background-noise, and pure acknowledgement content unless it confirms a decision.
4. Segment by coherent discussion topics, not by arbitrary fixed length unless the user requests time-based output.
5. Extract and preserve:
   - meeting topic and agenda
   - participants or stable speaker ids
   - speaker-specific views and evidence
   - decisions, consensus, disagreements, risks, blockers
   - tasks with owner and deadline
   - unresolved questions
6. Produce the requested format exactly.
7. Self-check every speaker, task owner, deadline, and conclusion against the transcript before final output.

## Hard rules

- Do not call interfaces, APIs, databases, workflow services, or web endpoints as part of this skill.
- Do not fabricate absent fields. Use `原文未涉及`, `未明确责任人`, or `未明确时间` when needed.
- Preserve speaker names exactly. If names are absent, use `发言人0`, `发言人1`, etc.
- Separate each speaker's own views; never cross-attribute or merge viewpoints.
- Capture conflicts and consensus explicitly when present.
- For phone-call transcripts, introduce phone numbers once if needed, then use speaker numbers in summaries; mask phone numbers unless raw identifiers are required.
- For JSON modes, output strict valid JSON only and no Markdown code fence.
- Keep summaries shorter than the transcript. For content under 30 seconds with no concrete information, output `暂无`.

## Usage examples

- “Use $jt-meeting-summary to generate formal JSON meeting minutes and todo items from this transcript.”
- “Use $jt-meeting-summary to summarize this sales call into concise Markdown.”
- “Use $jt-meeting-summary to create a ten-minute summary for this long meeting.”
- “Use $jt-meeting-summary to generate title, keywords, speaker summaries, and action items.”
- “Use $jt-meeting-summary to turn this meeting summary into a comic-style image prompt.”

## Reference loading guidance

Load only the reference matching the selected mode. Load `summary-components.md` together with another reference only when the user asks for multiple derived artifacts such as minutes plus title/tags/speaker summaries.
