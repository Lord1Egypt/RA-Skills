# Example: Connected mode (ONEPRESS_API_KEY)

> Prerequisites: `ONEPRESS_API_KEY` is set — obtained via the pairing flow
> (`POST /api/connect`, browser-confirmed; see SKILL.md) or created manually at
> getonepress.com → Settings → Account → API keys.

## User asks

> "Do me a competitive landscape deck on AI coding agents — 10 slides, partner meeting Friday."

## Agent flow

**1. Clarify once if needed** — audience is partners, goal is clear, so draft the task and submit:

```
POST https://www.getonepress.com/api/v1/conversations
Authorization: Bearer $ONEPRESS_API_KEY
Content-Type: application/json

{
  "message": "Create a 10-slide competitive landscape deck on AI coding agents.\n\nAudience: investment partners evaluating the space\nGoal: map the key players, their positioning, and where the white space is\nResearch: use current public sources; cite them on-slide\nMust include: Cursor, Devin, Claude Code, Copilot, Windsurf; funding and pricing tiers\nTone/style: data-dense, concise\nOutput: slide deck I can export to PPTX.",
  "title": "AI coding agents — competitive landscape"
}
```

```json
{"conversationId": "conv_01jabc...", "injected": false}
```

**2. Poll** every 15–30s:

```
GET https://www.getonepress.com/api/v1/conversations/conv_01jabc...
Authorization: Bearer $ONEPRESS_API_KEY
```

```json
{
  "conversation_id": "conv_01jabc...",
  "title": "AI coding agents — competitive landscape",
  "status": "done",
  "preview_path": "Deck/ai-coding-agents-landscape/index.html",
  "updated_at": "2026-10-03T08:12:44.000Z",
  "answer": "Done — 10-slide deck in Deck/ai-coding-agents-landscape/index.html, 23 cited sources…"
}
```

**3. Report to the user:**

> Your deck is done — 10 slides, 23 cited sources, covering Cursor/Devin/Claude Code/Copilot/Windsurf with funding and pricing tiers.
>
> Open it at https://www.getonepress.com/app → "AI coding agents — competitive landscape" — preview, share as a live link, or export to PPTX/PDF there.

**4. Follow-ups stay in the same conversation:**

```
POST https://www.getonepress.com/api/v1/conversations/conv_01jabc...
Authorization: Bearer $ONEPRESS_API_KEY
Content-Type: application/json

{"message": "Add a slide comparing context-window sizes"}
```
