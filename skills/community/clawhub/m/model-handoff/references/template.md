# HANDOFF.md Starter Template

Copy this to your workspace root as `HANDOFF.md` and fill in the sections.

---

```markdown
# HANDOFF.md — Model Switch Context

Read this when you are a new model taking over a session. This is your fast-boot.

## Who you are
- You are **[Agent Name]** — [one-line persona description]
- [Tone/style notes. e.g. "Formal, call user Sir."]
- Full persona: read `SOUL.md`

## Who you're helping
- **[User Name]** — [role, location]
- [Any key personal context worth noting]
- Full context: read `USER.md` and `MEMORY.md`

## Active projects

### [Project Name]
- **Status:** [In progress / Blocked / Done]
- **Key files:** `path/to/file.ext`, `path/to/other.ext`
- **Next steps:** [What needs to happen next]

### [Project Name]
- **Status:** [In progress / Blocked / Done]
- **Key files:** `path/to/file.ext`
- **Next steps:** [What needs to happen next]

## Agent roster
| ID | Model | Role |
|----|-------|------|
| main | [model] | Orchestrator |
| [agent-id] | [model] | [role] |

## Key credentials & tools
- **[Service]:** credentials in `[filename]`
- **[Service]:** API key in `[filename]`
(Never inline secrets here — point to files only)

## Behavioral rules
- [Critical rule 1]
- [Critical rule 2]
- [Critical rule 3]

## How to keep this file current
- Update when user says "switching to [model]" — do it immediately
- Update when significant project milestones are reached
- Remove stale/completed projects on each update

## Last updated
[YYYY-MM-DD ~H:MM TZ] — [one-line session summary]
```
