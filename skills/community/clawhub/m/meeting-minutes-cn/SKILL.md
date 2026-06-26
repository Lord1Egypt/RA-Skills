---
name: meeting-minutes
description: Generate structured meeting minutes from templates, sync to Feishu, and track action items. Use when the user asks to create meeting notes (会议纪要/会议记录), summarize a meeting, or generate minutes from discussion context.
tags: ['meeting', 'minutes', 'feishu', 'productivity', 'chinese']
---

# Meeting Minutes Skill

Generate structured meeting minutes, sync to Feishu, and track action items.

## When to Use

- User asks to create meeting minutes / 会议纪要 / 会议记录
- User wants to summarize a meeting or discussion
- User provides meeting context and wants structured output

## Workflow

1. **Gather context**: Ask for or infer meeting info (date, attendees, type, agenda, discussion points, action items)
2. **Generate minutes**: Use the template at `references/template.md` — fill in all `{{placeholders}}`
3. **Sync to Feishu**: Use the feishu-doc skill to create a document with the filled content
4. **Track action items**: Optionally log action items to memory for follow-up

## Template

See `references/template.md` for the full template with placeholders.

### Meeting Types

| Type | Chinese | Description |
|------|---------|-------------|
| brainstorming | 头脑风暴 | Creative ideation, no decisions expected |
| planning | 规划会 | Goal setting, roadmap, resource allocation |
| review | 评审会 | Progress check, demo, feedback |
| retro | 复盘会 | Reflection, improvement identification |

## Feishu Sync

```bash
python3 .claude/skills/feishu-doc/scripts/doc_ctl.py create "会议纪要 - {title} - {date}" --content "{minutes_content}"
```

If the feishu-doc skill is not available, output the minutes as markdown and inform the user.

## Action Item Tracking

After creating minutes, add action items to `memory/YYYY-MM-DD.md`:

```markdown
### Action Items from: {meeting_title}
- [ ] {action_1} — @{{owner_1}} — due {{deadline_1}}
- [ ] {action_2} — @{{owner_2}} — due {{deadline_2}}
```

## Example

User: "帮我写今天产品评审会的纪要"

→ Fill template with inferred/provided info
→ Create Feishu doc
→ Log action items to daily memory
→ Reply with doc link
