---
name: job-monitor
description: Analyze JD text and return structured match summary.
---

# Job Monitor Skill

## Trigger

Activate when user asks:

- "Analyze this JD"
- "What is my match score?"
- "Parse this position description"
- "Search AI intern jobs on BOSS"
- "搜一下深圳 AI Agent 实习"

## Workflow

1. Read JD text provided by the user.
2. Call backend API with the `exec` tool (use `curl`):
   - If user provides JD text -> call `POST /api/jd/analyze`
     - Endpoint: `POST http://127.0.0.1:8010/api/jd/analyze`
     - Header: `Content-Type: application/json`
     - Body: `{"jd_text":"<user jd text>"}`
     - Example:
       - `curl -sS -X POST "http://127.0.0.1:8010/api/jd/analyze" -H "Content-Type: application/json" -d '{"jd_text":"<user jd text>"}'`
   - If user asks to search/scanning BOSS -> call `POST /api/boss/scan`
     - Endpoint: `POST http://127.0.0.1:8010/api/boss/scan`
     - Header: `Content-Type: application/json`
    - Body: `{"keyword":"<search keyword>","max_items":10,"max_pages":2}`
     - Example:
      - `curl -sS -X POST "http://127.0.0.1:8010/api/boss/scan" -H "Content-Type: application/json" -d '{"keyword":"深圳 AI Agent 实习","max_items":10,"max_pages":2}'`
3. Parse JSON from command stdout.
4. If API call fails or JSON is invalid, tell the user the error and ask for retry or corrected JD text.
5. Format returned JSON into a concise message:
   - For `/api/jd/analyze`: parsed title / skill list / match score / gap analysis
  - For `/api/boss/scan`: keyword / total count / pages_scanned / top jobs / optional screenshot path
6. Return result to user.

## Constraints

- Do not submit applications automatically.
- For any external platform action, require user confirmation first.
