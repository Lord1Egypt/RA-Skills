---
name: meeting-minutes
description: Generate structured meeting minutes from discussion notes, sync to Feishu docs, and manage action items. Use when the user says "写会议纪要", "生成会议记录", "meeting minutes", "sync minutes to Feishu", or provides meeting notes/discussion context that needs to be structured into a formal document. Also use when the user wants to create meeting minutes templates, customize meeting formats, or track action items from meetings.
---

# Meeting Minutes

Generate structured meeting minutes, sync to Feishu, and track action items.

## Workflow

1. **Collect input** — Ask for (or infer from context): date, attendees, meeting type, agenda, discussion notes, action items
2. **Render template** — Use `assets/template.md` as the base; fill placeholders with provided data
3. **Sync to Feishu** — If feishu-doc skill is available, create a Feishu doc with the rendered content
4. **Track action items** — Extract action items into a structured format for follow-up

## Template

Read `assets/template.md` for the full template. Key sections:

- Meeting Info (date, attendees, type, facilitator)
- Agenda
- Key Discussion Points
- Action Items (table: item / owner / deadline / status)
- Decisions Made
- Next Steps

### Meeting Types

| Type | Focus |
|------|-------|
| brainstorming | Ideas, no decisions yet |
| planning | Goals, milestones, assignments |
| review | Progress, blockers, adjustments |
| retro | What worked, what didn't, improvements |

## Feishu Sync

When the feishu-doc skill is available:

```bash
python3 .claude/skills/feishu-doc/scripts/doc_ctl.py create "会议纪要 - {title} ({date})" --content "{rendered_content}"
```

Use `--share` or `--owner` to grant access to attendees.

## Action Item Extraction

After rendering, extract action items as structured data:

```json
{
  "items": [
    {"item": "...", "owner": "...", "deadline": "...", "status": "pending"}
  ]
}
```

Save to `memory/action-items-{date}.json` for follow-up tracking.

## Customization

- Edit `assets/template.md` to change the template structure
- Add custom sections by modifying the markdown template
- Meeting types can be extended in the type table above
