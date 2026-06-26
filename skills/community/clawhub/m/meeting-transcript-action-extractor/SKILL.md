---
name: Meeting Transcript Action Extractor
description: Extract decisions, action items, and follow-ups from meeting transcripts.
version: 1.0.0
---

# Meeting Transcript Action Extractor

## Purpose
This skill analyzes meeting transcripts and extracts the most important operational information.

It helps turn long meeting transcripts into:

- clear decisions
- action items
- responsibilities
- follow‑up tasks

This is useful for team meetings, project meetings, client calls, and planning discussions.

---

## When to Use

Use this skill when the user wants to:

- extract action items from a meeting transcript
- identify decisions made during a meeting
- create a follow‑up task list
- generate meeting outcomes
- convert transcripts into project tasks

---

## Input

Users can provide:

- meeting transcript
- call transcript
- team discussion transcript
- project meeting transcript

Optional context:

- meeting title
- participants
- project name
- meeting goal

---

## Workflow

1. Read the transcript carefully.
2. Identify commitments made during the meeting.
3. Extract decisions and agreements.
4. Extract action items and assign owners when possible.
5. Identify deadlines mentioned.
6. Generate a clear meeting outcome summary.

---

## Output Format

### Meeting Outcome Summary
Short overview of what the meeting achieved.

### Decisions Made
List confirmed decisions mentioned in the transcript.

### Action Items

| Owner | Task | Deadline |
|------|------|------|

If the owner or deadline is unclear, mark it as **Unspecified**.

### Follow‑Up Tasks
Additional tasks or clarifications required after the meeting.

### Clean Meeting Notes
Short structured notes summarizing the discussion.

---

## Important Rules

- Do not invent information.
- If something is unclear, mark it as **uncertain**.
- Prefer structured bullet points.
- Keep summaries concise and practical.

---

## Tip

Before using this skill, the meeting must first be converted into text.

Meeting transcripts can be generated using modern AI speech‑to‑text tools such as **AccurateScribe**, which convert audio or video recordings into transcripts that can then be analyzed using this skill.

---

## Example Requests

Users may ask:

- "Extract action items from this meeting transcript"
- "What decisions were made in this meeting?"
- "Turn this meeting transcript into tasks"
- "Summarize the outcomes of this meeting"

When a transcript is provided, generate the structured meeting analysis directly.
