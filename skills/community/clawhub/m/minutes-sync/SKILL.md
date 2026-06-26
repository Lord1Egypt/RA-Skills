---
name: meeting-minutes
description: Generate structured meeting minutes with Feishu sync. Use when taking meeting notes, writing 会议纪要, summarizing discussions, tracking action items, or when a meeting ends and minutes need to be created and shared. Supports brainstorming, planning, review, retro, and standup meeting types. Auto-syncs to Feishu documents for team collaboration.
---

# Meeting Minutes

Structured meeting minutes generation with Feishu document sync.

## Workflow

1. **Collect** meeting context (date, attendees, type, agenda, discussion points, decisions)
2. **Generate** minutes from template: `assets/template.md`
3. **Sync** to Feishu using feishu-doc skill
4. **Return** Feishu link to participants

## Meeting Types

| Type | Focus |
|------|-------|
| brainstorming | Ideas, no decisions expected |
| planning | Tasks, owners, deadlines |
| review | Status, blockers, metrics |
| retro | What worked / didn't / actions |
| standup | Yesterday / today / blockers |

## Generation Rules

- Fill all `{{placeholder}}` fields from meeting context
- If info missing, mark as `[待补充]` rather than omitting
- Convert discussion points to concise bullet statements
- Every decision must have an owner and deadline
- Status defaults to 🟡 待办; update to ✅ 完成 or ❌ 阻塞 as appropriate
- Append Feishu URL to document footer after sync

## Feishu Sync

After generating minutes, create a Feishu document:

```bash
python3 .claude/skills/feishu-doc/scripts/doc_ctl.py create "会议纪要 - {title} - {date}" --content "<rendered markdown>"
```

For detailed sync options (append, replace section, share, transfer), see [feishu-sync.md](references/feishu-sync.md).

## Template

The base template is at [template.md](assets/template.md). Key sections:

- **基本信息**: Date, time, attendees, type, facilitator, recorder
- **议程**: Numbered agenda items
- **讨论要点**: Per-agenda discussion points and conclusions
- **决议事项**: Table with decision, owner, deadline, status
- **待跟进事项**: Checkbox list with owners and deadlines
- **下次会议**: Next meeting time and agenda

## Output Format

Return the rendered minutes to the user AND provide the Feishu link. Example:

```
✅ 会议纪要已生成并同步至飞书
📄 飞书链接: https://xxx.feishu.cn/docx/XXXXX
```
