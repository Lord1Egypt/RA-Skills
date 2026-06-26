---
name: ops-issue-followup
description: Use when the user asks Codex to follow up, analyze, investigate, or is @mentioned for a project/system maintenance or operations issue. Guides Codex to clarify the issue, identify the owning project, gather context, align on the analysis plan, investigate inside the project, ask when uncertain, and summarize findings for possible llm wiki archival.
---

# Ops Issue Follow-up

Use this skill as a daily maintenance and operations assistant for project or system issues. The goal is to keep investigation aligned before going deep.

## Workflow

1. Confirm the issue
- Restate the observed symptom, expected behavior, impact, time range, and examples.
- Separate confirmed facts from assumptions, memory, and unverified clues.
- If key facts are missing, ask concise follow-up questions.

2. Identify ownership and related projects
- Determine which project, service, system, table, queue, job, or external dependency is involved.
- If ownership cannot be inferred from the request or current context, ask the user before investigating deeply.

3. Gather project context
- Prefer project-local context first: `AGENTS.md`, README, architecture docs, runbooks, config examples, tests, and relevant source paths.
- If available, use llm wiki or similar knowledge base for historical decisions and operational context.
- Treat wiki/history as context, not proof; verify against code, logs, configs, or current runtime evidence when possible.

4. Align on the analysis direction
- Summarize the likely investigation branches.
- Call out the recommended branch and why.
- Ask for confirmation when multiple plausible directions could lead to very different work.

5. Investigate in the project
- Switch into the relevant project/workspace before reading code or running commands.
- Enumerate entrypoints before tracing implementation details.
- For operational data issues, map: data record -> producer -> input source -> transport/proxy/dependency -> persistence/reporting.
- When uncertain, ask the user instead of inventing missing runtime facts.

6. Resolve or narrow the issue
- Provide confirmed findings, likely causes, and remaining unknowns.
- If code/config changes are needed, state target files and intent before editing.
- If validation is possible, run concrete verification commands and report actual results.

7. Summarize and preserve
- End with a concise incident-style summary: symptom, scope, root cause or likely cause, evidence, fix/next steps.
- When useful, propose writing the summary to llm wiki, including a suggested title and structure.
