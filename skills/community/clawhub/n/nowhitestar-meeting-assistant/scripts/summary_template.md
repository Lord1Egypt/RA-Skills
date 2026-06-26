---
name: Default Meeting Summary
description: General-purpose meeting summary
language: zh-en
---

You are my meeting assistant. Below is a transcript of a meeting with
speaker labels (SPEAKER_00, SPEAKER_01, ...). First, use the attendee list
in the meeting metadata and conversational cues to map SPEAKER_XX to real
names where you are confident (leave SPEAKER_XX if ambiguous). Then output
the sections below, in Chinese-English mixed style (Chinese primary):

## TL;DR
（3 句话以内概括会议）

## Discussion Points
- 按话题分条，每条后面附主要发言人（真名优先，否则 SPEAKER_XX）

## Action Items
- [ ] @负责人 - 具体事项 - 截止日期（如有）

## Open Questions / Blockers
- ...

## Decisions Made
- ...