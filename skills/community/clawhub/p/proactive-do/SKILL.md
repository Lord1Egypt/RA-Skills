---
name: proactive-do
description: >-
  Proactive todo execution, heartbeat-driven review, and structured follow-up for a
  markdown todo system. Use when the agent needs to review `todo/todo.md`, pick the
  top 3 `[new]` items, do tasks that look doable within about 1 hour, draft simple
  plans for tasks likely to take over 1 hour, update `[new|wip|done]` labels,
  maintain per-task journals under `agent_work/`, reconcile work after about 2.5
  hours, and send concise start/finish reports by email instead of chat. Strong
  triggers include: heartbeat prompts, system events mentioning `todo/todo.md`,
  `[new]` / `[wip]` / `[done]`, "proactive-do", "review todos", "pick top 3",
  "do it now if under 1 hour", "draft a plan", "reconcile statuses", and
  "agent_work" journals.
---

# Proactive-Do

A lightweight workflow for proactive execution of a human's todo list with recurring reviews, clear state labels, structured documentation, and concise reporting.

## Quick start

1) Source of truth
- Todos live in todo/todo.md, grouped by date headings (e.g., "## YYYY-MM-DD").
- Items are bullets with a state label: "- [new] ..., - [wip] ..., - [done] ...".
- Only these three states are valid.
- Strict preservation rule: never delete existing todo items from todo/todo.md automatically. You may append new items and revise existing items in place (for example, changing only the state label or updating the text of the same line), but you must not remove lines/items unless the owner/requester explicitly asks for deletion.

2) Initialize phase (install-time only; do not run on every review)
- Run these setup actions when the skill is first installed or first adopted in a workspace, not during each 3h review or 2.5h follow-up.
- Ensure these paths exist; create them if missing:
  - todo/
  - todo/todo.md
  - agent_work/
  - agent_work/heartbeat_emails/
  - agent_work/proactive-do/
- If todo/todo.md does not exist, create it with a minimal starter structure:
  - a top-level heading or today's date section ("## YYYY-MM-DD")
- If agent_work/proactive-do/delivery_prefs.md is referenced later but missing, do not fail; create the parent folder and continue with fallback behavior per notification policy.
- Initialization must be non-destructive: create missing paths only, do not remove or overwrite existing content.

3) Cadence (recommended)

2) Cadence (recommended)
- Every 3 hours: scan all [new] items and pick the top 3 to address this pass (leave the rest for later) to reduce load.
- Every 2.5 hours: reconcile what was worked on; mark [done] if finished, else [wip] with a one-line reason + next action.
- Use OpenClaw cron to schedule system events that trigger these reviews (see Cron payloads below).

3) Decision policy
- If a selected [new] item appears doable within ~1 hour: do it now during the 3h review.
- If it likely needs >1 hour: write a simple, structured plan (steps + rough time estimate) and leave the item [new] until kickoff; when starting work, flip to [wip].
- If assistance/approval is needed: halt, report to the owner/requester, and wait.
- Search online when needed.
- If blocked twice on the same point: stop, record the failure and next step, mark [wip], and report.

4) Selection heuristics (for "top 3")
Default ranking when not specified by the owner/requester:
1) Explicit priority hints in the text (e.g., "priority: high"),
2) Fit for ≤1 hour (quick wins first),
3) Recency/clarity of the item.
When in doubt, take the first three [new] items in file order.

5) Per-task journal (agent_work/)
- When beginning work on an item: create a folder agent_work/YYYY-MM-DD_HHMM_nickname.
- Inside, maintain a running log: start time, linked todo text, decisions, commands, files created, errors, attempts, results.
- For harder tasks include a small plan with time estimate and critical steps.
- Place any generated files/documents inside this folder.

6) Reporting
- Every report must name the todo/project it concerns.
- For ≤1h tasks done now: include Result, Key steps, and any links to outputs.
- For >1h tasks: include Plan (steps + estimate), Current status ([new|wip]), and where the journal folder lives.

## Categorization policy
When the owner/requester says "add a todo":
- Assign exactly one primary category from: quick search | setup | prototype | try out | learn | write.
- Add one generation tag: code | no-code.
- Append to todo/todo.md (today's section) using:
  - "- [new] <Title> — <short description> [category: <category>; gen: <code|no-code>]"
- Update prioritization: quick search/setup tend to be picked more often; prototype/try out medium; learn/write lower for push.
- Persist this behavior in the local workspace policy/memory files when that is appropriate for the environment.

## Notification delivery (heartbeat)
- Prefer email over chat for heartbeat notifications.
- Send email via gog CLI (Gmail / Google Workspace CLI) when it is available.
- Resolve sender, recipient, and fallback behavior from a local preference file when present:
  - `agent_work/proactive-do/delivery_prefs.md`
- If no preference file exists, ask once for delivery settings or use the current chat as a temporary fallback.
- Start email (at 3h review start):
  - Subject: "[assistant] start doing on 3 todos + <abbr>" (abbr = short names of the 3 todos)
  - Body: full text of the 3 selected todos; concise (≈2-minute read)
- Follow-up email (at 2.5h reconciliation):
  - Subject: "[assistant] finish 3 todos + <abbr>" (same abbr)
  - Body: brief summary of what was done, results, failures, and done/not-done per task (≈2-minute read)
- Archive a copy of each email under `agent_work/heartbeat_emails/`.
- Keep local preferences out of the published skill package unless they are intentionally shared.

## 3h Review — Execution flow
1) Parse todo/todo.md for the latest date section and list all items marked [new].
2) Rank candidates using the selection heuristics and pick the top 3 for this pass.
3) For each of the top 3:
   - Estimate difficulty/time. If ≤1h:
     - Flip to [wip], create agent_work folder, execute.
     - On success, flip to [done] and report.
     - If blocked twice, keep [wip], record why + next action, and report.
   - If >1h:
     - Draft a short plan (steps + estimate), store it in agent_work folder template (can be pre-created without kickoff), and report.
4) Summarize what was done/planned, referencing the todo lines.
5) Notification: send the Start email using gog CLI per the template above.

## 2.5h Follow-up — Reconciliation flow
1) Review items touched in the last 2.5h (from your journal and recent edits).
2) If finished: mark [done] and report the completion.
3) If not yet finished: ensure [wip] with a one-line reason and next action; update the journal accordingly; report.
4) Notification: send the Finish email using gog CLI per the template above.

## Cron payloads (copy/paste)
- 3h review payload text:
  "Heartbeat: review todo/todo.md for [new] items. Pick the top 3 to act on this pass. For each selected [new]: if ≤1h, do it now and report; if >1h, draft a simple plan with estimate and report. Maintain agent_work/ journals and include the todo/project name in every report. Deliver the start report by email per the proactive-do skill notification policy."

- 2.5h follow-up payload text:
  "Follow-up heartbeat: review all work performed in the past 2.5h. For each task, if completed mark [done]; else mark [wip] with a one-line reason and next action. Report the changes and reference the related todo/project. Deliver the finish report by email per the proactive-do skill notification policy."

## File conventions
- Todo file: todo/todo.md (single source of truth; preserve all existing items, do not delete automatically)
- States: [new], [wip], [done] (no other labels)
- Date sections: markdown H2 "## YYYY-MM-DD"
- Agent journals: agent_work/YYYY-MM-DD_HHMM_nickname/
  - journal.md — running log (start time, intent, steps, errors, outputs)
  - plan.md — for >1h tasks (steps + estimate + critical steps)
  - outputs/ — any artifacts created

## Heuristics for "≤1 hour"
- Low external dependencies; small scope; familiar stack; no required approvals.
- Examples: formatting/rewording docs, light scripting/automation, small data tidying, basic research + short writeup.
- If uncertain, default to plan-first and request clarification.

## Safety / escalation
- Halt and report for any action requiring explicit approval or external messaging on behalf of the owner/requester.
- Never loop indefinitely. Two failed attempts on the same blocker → stop, label [wip], report.
- Always include the todo/project name and journal path in reports.

## Templates and helpers
- See references/templates.md for copy/paste templates:
  - agent_work journal.md
  - agent_work plan.md
  - Report blocks for "done" and "plan" updates

## Notes
- Keep SKILL.md lean; store verbose templates in references/.
- Prefer fewer larger edits to files (respect rate limits and avoid tight loops when writing externally).
