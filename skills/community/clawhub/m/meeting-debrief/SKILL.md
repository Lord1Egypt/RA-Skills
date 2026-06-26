---
name: meeting-debrief
description: Process meeting transcripts to extract action items, recommendations, key topics, relationships, and generate Excalidraw visualizations. Use when the user shares a meeting transcript, recording notes, or conversation summary and wants a structured debrief with visual output.
version: 1.0.0
author: dynoclaw
user-invocable: true
metadata: {"openclaw":{"emoji":"🎙️"}}
---

# Meeting Debrief

Transform raw meeting transcripts into structured debriefs with Excalidraw visualizations, action items, and strategic recommendations.

## Input

The user provides a meeting transcript (timestamped conversation, Fathom notes, raw text, or pasted recording output). If no transcript is provided, ask the user to paste or attach one.

## Processing Steps

### Step 1 — Identify Participants & Context

- Extract speaker names (map "You" to the user, "Others" to named participants)
- Determine meeting type: discovery, follow-up, pitch, check-in, negotiation, brainstorm
- Note the date if mentioned, otherwise use today's date

### Step 2 — Extract Key Topics

Group the conversation into 3-7 major topics discussed. For each topic:
- **Topic name** (2-5 words)
- **Summary** (2-3 sentences)
- **Key details** (bullet points of specific facts, numbers, names mentioned)

### Step 3 — Extract Entities

Pull out all named entities:
- **People** — name, role/title, organization
- **Companies** — name, stage, sector, what they do, key metrics
- **Organizations** — accelerators, universities, investors mentioned
- **Products/Services** — specific offerings discussed
- **Financial figures** — funding amounts, valuations, revenue targets

### Step 4 — Action Items

Extract every action item with:
- **What** — specific task
- **Who** — responsible party
- **When** — deadline or timeframe if mentioned
- **Priority** — High / Medium / Low (inferred from urgency and impact)

### Step 5 — Recommendations

Based on the conversation, generate 3-5 strategic recommendations:
- What opportunity or risk was identified
- Suggested next move
- Why it matters

### Step 6 — Generate Excalidraw Visualization

Build an Excalidraw JSON file that visually maps the meeting. The diagram should include:

1. **Title banner** at the top with meeting name, date, and participants
2. **Business model / structure section** — if the other party described how their business works, visualize it as a flow diagram
3. **Portfolio / entities section** — cards for each company or entity discussed with key stats
4. **Action items section** — checklist-style boxes with owner and deadline
5. **Recommendations section** — highlighted boxes with strategic suggestions
6. **Relationship map** — connections between you, the other party, and opportunities

Use the Excalidraw JSON template in `templates/excalidraw-base.json` as a starting structure. Generate element IDs using random alphanumeric strings (10 chars).

#### Excalidraw Element Guidelines

- Use `rectangle` elements for cards and sections
- Use `text` elements for labels and content
- Use `arrow` elements for relationships and flows
- Use `diamond` elements for decision points
- Color coding:
  - `#1e1e1e` background for title banner, white text
  - `#dbeafe` (light blue) for topic/entity cards
  - `#dcfce7` (light green) for action items
  - `#fef3c7` (light yellow) for recommendations
  - `#fce7f3` (light pink) for key relationships/opportunities
  - `#f3e8ff` (light purple) for financial/metrics

Save the Excalidraw file as `meeting-debrief-[participant]-[YYYY-MM-DD].excalidraw` in the current working directory.

### Step 7 — Output Summary

Present the debrief in this format:

```
## Meeting Debrief: [Meeting Title]
**Date:** [date]  |  **Participants:** [names]  |  **Type:** [meeting type]

---

### Key Topics
[numbered list with summaries]

### Companies & Entities
[table: Name | Sector | Stage | Key Metric | Notes]

### Action Items
| # | Task | Owner | Deadline | Priority |
|---|------|-------|----------|----------|
| 1 | ... | ... | ... | ... |

### Recommendations
1. **[Title]** — [description and rationale]

### Files Generated
- `meeting-debrief-[name]-[date].excalidraw` — Visual meeting map (open in Excalidraw or VS Code with Excalidraw extension)
```

### Step 8 — CRM Integration (Optional)

If CRM tools are available (HubSpot or Zoho), offer to:
- Create/update contacts for participants
- Log meeting notes
- Create deals if investment/partnership opportunities were discussed
- Tag with relevant pipeline stage

## Guidelines

- Be thorough in extraction — capture specific numbers, dates, and names
- Infer action items even if not explicitly stated (e.g., "I'll send you my calendar" = action item)
- Recommendations should be strategic and actionable, not generic
- The Excalidraw visualization should be readable and well-spaced (min 200px between elements)
- If the transcript is very long (>30 min), focus on the most substantive sections
- Always generate the Excalidraw file — this is the core differentiator of this skill
