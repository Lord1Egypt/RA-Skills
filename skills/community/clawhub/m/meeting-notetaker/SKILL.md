---
name: meeting-notetaker
version: "1.0.0"
description: "Fetch and present meeting notes from monday.com Notetaker, or show the next upcoming meeting with full context prep. Use when: asked to summarize a meeting, find notes from a meeting with a specific person, retrieve past meeting summaries, or asked about the next meeting. Trigger phrases: 'meeting notes', 'notes from meeting with X', 'last meeting with', 'summarize meeting', 'next meeting', 'what is my next meeting'."
---

# Meeting Notetaker Skill

## Load Local Context
```bash
CONTEXT_FILE="/opt/ocana/openclaw/workspace/skills/meeting-notetaker/.context"
[ -f "$CONTEXT_FILE" ] && source "$CONTEXT_FILE"
# Then use: $OWNER_EMAIL, $CALENDAR_ID, $GOG_CREDS, etc.
```

## Scope

This skill covers **monday.com Notetaker meetings only**.  
It does NOT fetch Zoom, Fathom, Fireflies, or other external recording services.

---

## Trigger Phrases

- "meeting notes"
- "notes from meeting with X"
- "last meeting with X"
- "what happened in the meeting with X"
- "summarize meeting"
- "meeting summary"
- "next meeting"
- "what is my next meeting"
- "what do I have next"

---

## Step 1 — Parse the Request

Determine search mode:

| Input | Mode |
|---|---|
| "last meeting" | **Most Recent** — no filter |
| "meeting with [Name]" | **Person Search** — use name as search term |
| "meeting about [Topic]" | **Topic Search** — use topic as search term |
| Specific date given | **Date Search** — filter by date after fetching |
| "next meeting" | **Next Meeting Mode** — see Step 1a below |

---

## Step 1a — Next Meeting Mode

When triggered by "next meeting" or similar:

1. **Fetch calendar** using direct Google Calendar API (NOT `gog` CLI — broken on server). Use credentials from `/opt/ocana/openclaw/.gog/credentials.json` account `owner`. See owner-briefing skill for the full auth flow.
2. **Find the next upcoming event** — first event that starts after now
3. **Extract participants** from the calendar event (attendees list)
4. **Search notetaker** for past meetings with the same participants or title keywords:
   ```
   get_notetaker_meetings(search="[participant name or meeting title keyword]", include_summary=true, include_action_items=true, include_topics=true, limit=3)
   ```
5. **Format as Next Meeting Prep** (see format below)

### Next Meeting Prep Format

```
📅 Your next meeting:
[Meeting Title]
🕐 [Time] ([X minutes from now])
👥 [Participants]

🎯 Prep:
No history found with [Name] / OR:

Last meeting with [Name] ([date]):
• [Summary bullet 1]
• [Summary bullet 2]
• [Summary bullet 3]

✅ Open action items:
• [Action] — [Owner]
```

If no past meetings found with the participants → skip the prep section and just show the meeting details.
If no upcoming meetings today → report "No more meetings today".

---

## Step 2 — Fetch Meetings

Use the `get_notetaker_meetings` MCP tool with these flags:

```
get_notetaker_meetings(
  include_summary=true,
  include_action_items=true,
  include_topics=true,
  search="<name or topic if provided>",  # omit for "last meeting"
  limit=5  # fetch a few to find the best match
)
```

- For **Most Recent**: fetch with no search param, limit=1
- For **Person/Topic Search**: use the extracted name/topic as the `search` param
- For **Date Search**: fetch recent meetings and filter by date in output

---

## Step 3 — Select the Best Match

If multiple meetings returned:
1. Prefer the most recent one that matches the search intent
2. If ambiguous (multiple meetings with same person), present a short list and ask which one
3. If zero results → report "No monday.com notetaker meetings found for [X]"

---

## Step 4 — Format the Output

```
📋 [Meeting Title]
📅 [Date] | [Duration if available]
👥 Participants: [Name1, Name2, ...]

Summary:
• [Point 1]
• [Point 2]
• [Point 3]
(up to 5 bullets — condense if longer)

💬 Topics Discussed:
• [Topic 1]
• [Topic 2]

✅ Action Items:
• [Action] — [Owner] (due: [Date if available])
• [Action] — [Owner]
```

If any section has no data, omit it (don't show empty headers).

### Example Output

```
📋 Product Roadmap Review
📅 March 28, 2026 | 60 min
👥 Participants: Netanel Abergel, Daniel K., Omri S.

Summary:
• Discussed Q2 priorities — AI features take top slot
• Agreed to delay the legacy migration to Q3
• Budget for external design resources approved
• Next milestone: beta release by May 15

💬 Topics Discussed:
• Q2 roadmap priorities
• Legacy migration timeline
• Design budget

✅ Action Items:
• Update roadmap doc with Q2 decisions — Netanel (due: April 2)
• Send design brief to freelancers — Omri (due: April 5)
```

---

## Step 5 — Offer to Create Action Items (Optional)

If action items were found, add at the end:

```
Want me to add these action items to your monday.com board?
```

If owner says yes:
- Use `monday-api-mcp__create_item` to create items on the relevant board
- Set owner and due date columns from the action item data
- Confirm creation with item names

---

## Error Handling

| Situation | Response |
|---|---|
| No meetings found | "No monday.com notetaker meetings found for [X]" |
| Search returns ambiguous results | List top 3 options with dates, ask which one |
| Meeting found but no summary/topics | Show what's available, note "Summary not available for this meeting" |
| Tool error | Report as BLOCKED: "Could not fetch meeting notes — notetaker service unavailable" |

---

## Notes

- **Language:** Respond in the same language the request was made in (Hebrew → Hebrew, English → English)
- **Recency:** Always prefer the most recent matching meeting unless owner specifies otherwise  
- **Access:** Uses `access: "OWN"` by default — fetches owner's own meetings. Use `access: "ALL"` only if owner asks about a meeting they weren't in.
- **No transcript by default:** Don't fetch the full transcript unless explicitly asked (large payload, high token cost)
