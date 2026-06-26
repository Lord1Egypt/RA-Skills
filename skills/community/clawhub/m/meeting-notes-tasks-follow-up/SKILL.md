---
name: meeting-notes-tasks-follow-up
description: Lightweight meeting-notes productivity workflow for turning transcripts or raw meeting notes into clean summaries, extracted key points, and simple action lists. Use when processing meeting transcripts, call notes, workshop notes, or internal sync notes into a clear recap and a basic task list for a free ClawHub edition.
---

# Meeting Notes → Tasks & Follow-up

Run a simple, professional workflow that transforms raw meeting notes into a clear summary and a practical task list.

Keep outputs concise, readable, and easy to share with a team after a meeting.

## Workflow

Use this sequence for complete requests:

1. collect meeting context
2. clean and structure the notes
3. extract key points
4. generate simple tasks
5. produce a clean summary

## 1. Collect meeting context

Capture the operating brief before producing outputs.

Minimum inputs:

- meeting title
- meeting date if available
- participants if known
- raw notes or transcript
- desired output style
- target audience for the summary

If some information is missing, keep assumptions minimal and label unknowns clearly.

## 2. Clean and structure the notes

Use user-provided notes, transcript text, or manually reviewed meeting content.

Normalize the material into these buckets whenever possible:

- context
- decisions
- discussion points
- blockers
- next steps

Rules:

- remove filler and repetition
- preserve important names, dates, and decisions
- do not invent commitments that are not supported by the source notes

## 3. Extract key points

Identify the most important information from the meeting.

Capture these fields whenever possible:

- main objective
- important decisions
- open questions
- risks or blockers
- notable follow-up topics

Use `references/templates.md` for key-point and summary structure.

## 4. Generate simple tasks

Convert explicit next steps into a practical action list.

Recommended task fields:

- task
- owner if stated
- status defaulting to `todo`
- note

Rules:

- only generate simple tasks that are clearly implied or directly stated
- if no owner is given, mark owner as `unassigned`
- if no due date is mentioned, leave it blank rather than guessing

Use `scripts/task_extractor.py` to convert meeting text into a basic tasks CSV.

## 5. Produce a clean summary

For the final recap, include:

- short meeting summary
- key decisions
- important discussion points
- simple task list
- unanswered questions

Keep the tone professional, clear, and easy to forward.

## Output order

For a complete request, produce outputs in this order:

1. meeting context
2. concise summary
3. key points
4. task list
5. open questions

## Style standard

Write for busy teams.

Prefer:

- short paragraphs
- bullets over long prose
- plain language
- clearly labeled sections

Avoid:

- bloated meeting minutes
- invented deadlines or responsibilities
- overcomplicated project-management language

## Community edition note

This free edition focuses on transcript cleanup, key point extraction, simple task generation, and a polished meeting summary. Smart prioritization, personalized follow-up emails, integrations, and follow-up tracking are reserved for the premium edition.

## Resources

Use bundled resources when useful:

- `references/templates.md` for recap and task templates
- `scripts/task_extractor.py` to convert notes into a simple task CSV
- `scripts/meeting_summary.py` to generate a compact structured meeting summary
