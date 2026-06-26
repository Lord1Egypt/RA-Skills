---
name: meeting-notes
description: Use when you need to organize meeting notes, extract action items, and generate structured summaries. Ideal for processing raw meeting transcripts or bullet notes into clean, shareable documents with clear owners and deadlines.
---

# Meeting Notes Organizer & Action Item Extractor

Transform raw meeting notes into structured, actionable summaries.

## When to Use
- After any meeting to create a clean summary
- Processing audio transcripts from Zoom/Teams/飞书
- Weekly standups, sprint reviews, project kick-offs
- Turning messy notes into shareable team documents

## Core Workflow

### Step 1: Input Collection

Provide any of:
- Raw bullet-point notes
- Audio transcript text
- Voice memo content
- Email thread summary

### Step 2: Meeting Structure Template

```markdown
## 会议纪要 | Meeting Summary

**会议主题 / Topic:** [填写]
**日期 / Date:** YYYY-MM-DD
**参会人 / Attendees:** [姓名列表]
**主持人 / Facilitator:** [姓名]
**记录人 / Note-taker:** [姓名]

---

## 议题讨论 | Discussion Points

### 1. [议题标题]
- **背景:** 简要说明
- **讨论内容:** 关键讨论点
- **结论/决议:** 明确的决定

### 2. [议题标题]
...

---

## 行动项 | Action Items

| # | 任务 | 负责人 | 截止日期 | 优先级 | 状态 |
|---|------|--------|----------|--------|------|
| 1 | [任务描述] | @姓名 | MM-DD | 高/中/低 | 待开始 |
| 2 | | | | | |

---

## 待确认事项 | Open Questions

- [ ] [问题1] — 负责跟进：@姓名
- [ ] [问题2]

---

## 下次会议 | Next Meeting

**时间:** [日期时间]
**议题预告:** [下次讨论的主要议题]
```

### Step 3: Action Item Extraction Rules

When extracting action items, look for:
- **动词短语**: "需要"、"要"、"将"、"负责"、"跟进"
- **English triggers**: "will", "need to", "action:", "owner:", "TODO"
- **Implicit owners**: If someone proposed something, they likely own it
- **Deadlines**: Extract explicit dates; if none, flag as "TBD"

### Step 4: Priority Classification

```
高优先级 (High): 影响下次会议、有明确截止日期、阻塞其他任务
中优先级 (Medium): 本周内需完成、依赖关系中等
低优先级 (Low): 长期改进、无明确截止日期
```

### Step 5: Distribution Checklist

- [ ] 发送给所有参会人
- [ ] 同步到项目管理工具（Jira/飞书/Notion）
- [ ] 在下次会议前 review 行动项完成情况
- [ ] 未完成项自动滚动到下次会议

## Output Formats

**Slack/飞书快速摘要:**
```
📋 [会议主题] 纪要 - YYYY-MM-DD
✅ 决议：[1-2句核心决定]
📌 行动项（共N项）：
  · @张三 - [任务] - 截止 MM-DD
  · @李四 - [任务] - 截止 MM-DD
❓ 待确认：[未解决问题数]
完整纪要：[链接]
```

## Pro Tips

1. **会议开始前** 明确记录人，确保覆盖所有行动项
2. **实时确认** 行动项负责人，不要会后猜测
3. **48小时原则** 会议结束48小时内发出纪要
4. **版本控制** 大型会议纪要建议保存版本历史
