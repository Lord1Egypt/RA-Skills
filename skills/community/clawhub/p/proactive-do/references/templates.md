# Proactive-Do Templates

## agent_work/journal.md (start this when beginning work)

Title: <YYYY-MM-DD_HHMM_nickname>
Linked todo: "<full todo line>" (date section + item text)
Start time: <ISO8601>

Context / intent:
- <why this matters / expected outcome>

Log (append chronologically):
- <time> Step: <what you did>
- <time> Output/Notes: <links/filenames/findings>
- <time> Error (if any): <error message>
- <time> Attempt #n fix: <what you tried>
- <time> Status: <wip|done>

Final result (fill when done):
- Outcome: <what changed / what was delivered>
- Artifacts: <files/links>
- Time spent: <~minutes>

---

## agent_work/plan.md (for tasks >1h)

Title: <YYYY-MM-DD_HHMM_nickname> — Plan
Linked todo: "<full todo line>"
Owner: assistant
Estimate: ~<hours>

Steps:
1) <step>
2) <step>
3) <step>

Critical steps / risks:
- <risk or dependency>
- <risk or dependency>

Next check-in: <proposed time window or next 3h review>

---

## Report — task completed (≤1h or after work)

Project/Todo: <date section + item text>
Status: done
What I did:
- <brief steps>
Artifacts/Links:
- <path or URL>
Notes:
- <anything noteworthy>

---

## Report — plan proposed (>1h)

Project/Todo: <date section + item text>
Status: new (plan prepared)
Plan (steps + estimate):
1) <step>
2) <step>
Estimate: ~<hours>
Journal: agent_work/<YYYY-MM-DD_HHMM_nickname>/
Needs from you:
- <approvals, clarifications, inputs>
