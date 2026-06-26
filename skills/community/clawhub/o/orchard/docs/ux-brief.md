# OrchardOS Dashboard — UX/UI Design Brief

## Mission
Redesign the OrchardOS dashboard as a **first-class tool** that feels native to the OpenClaw ecosystem. It should look and feel like it belongs alongside the OpenClaw control panel — same design language, same quality bar.

---

## Context

**What is OrchardOS?**
An agentic project management plugin for OpenClaw. It manages projects, tasks (with statuses: pending/ready/running/review/done/failed/blocked), knowledge bases, and agent run history. Think Linear or Plane, but for AI agents.

**Where it lives:** Served at `http://10.50.0.10:18790` — a proxy that handles auth and forwards to the gateway.

**Current state:** A functional but rough 1500-line single-file HTML/CSS/JS SPA. Works, not pretty.

---

## OpenClaw Design System (extract from their live CSS)

Match this exactly — do NOT use GitHub-dark or other themes.

```css
:root {
  /* Backgrounds */
  --bg: #0e1015;
  --bg-accent: #13151b;
  --bg-elevated: #191c24;
  --bg-hover: #1f2330;
  --card: #161920;

  /* Text */
  --text: #d4d4d8;
  --text-strong: #f4f4f5;
  --muted: #838387;

  /* Borders */
  --border: #1e2028;
  --border-strong: #2e3040;

  /* Accent (OpenClaw red) */
  --accent: #ff5c5c;
  --accent-hover: #ff7070;
  --accent-subtle: #ff5c5c1a;
  --accent-glow: #ff5c5c33;

  /* Status colors */
  --ok: #22c55e;
  --warn: #f59e0b;
  --danger: #ef4444;
  --info: #3b82f6;
  --accent-2: #14b8a6; /* teal */

  /* Typography */
  --font-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* Radii */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;

  /* Shadows */
  --shadow-sm: 0 1px 2px #00000040;
  --shadow-md: 0 4px 16px #0000004d;
}
```

**Status badge colors:**
- `pending` → `--muted` (grey)
- `ready` → `--info` (#3b82f6, blue)
- `running` → `--warn` (#f59e0b, amber)
- `review` → `--accent-2` (#14b8a6, teal)
- `done` → `--ok` (#22c55e, green)
- `failed` → `--danger` (#ef4444, red)
- `blocked` → `--danger` with 60% opacity

**Priority badge colors:**
- `critical` → `--danger`
- `high` → `--warn`
- `medium` → `--info`
- `low` → `--muted`

---

## API Endpoints (all relative to origin, standard OpenClaw auth model)

```
GET  /orchard/projects                          → [{id, name, goal, status, completion_score, completion_temperature, created_at}]
POST /orchard/projects                          → {id, name, goal, completion_temperature?}
GET  /orchard/projects/:id                      → project object
GET  /orchard/projects/:id/tasks                → [{id, project_id, title, description, acceptance_criteria, priority, status, assigned_role, model_override, blocker_reason, retry_count, created_at}]
POST /orchard/projects/:id/tasks                → {title, description?, acceptance_criteria?, priority?, model_override?}
GET  /orchard/projects/:id/knowledge            → [{id, content, source, created_at}]
POST /orchard/projects/:id/knowledge            → {content}
GET  /orchard/tasks/:id                         → task object
PUT  /orchard/tasks/:id                         → {status?, priority?, description?, acceptance_criteria?}
GET  /orchard/tasks/:id/runs                    → [{id, role, model, status, input, output, qa_verdict, qa_notes, started_at, ended_at}]
GET  /orchard/tasks/:id/comments                → [{id, author, content, created_at}]
POST /orchard/tasks/:id/comments                → {content, author?}
POST /orchard/wake                              → triggers queue runner
```

---

## Layout Vision

```
┌─────────────┬────────────────────────────────────────────┐
│  SIDEBAR    │  TOPBAR (breadcrumb + actions)             │
│  240px      ├────────────────────────────────────────────┤
│             │                                            │
│  OrchardOS  │  CONTENT AREA                              │
│  logo       │                                            │
│             │                                            │
│  PROJECTS   │                                            │
│  ─────────  │                                            │
│  > model-   │                                            │
│    distill  │                                            │
│  > watchdog │                                            │
│  > orchard- │                                            │
│    hardening│                                            │
│             │                                            │
│  + New      │                                            │
│    Project  │                                            │
└─────────────┴────────────────────────────────────────────┘
```

---

## Views

### 1. Projects List (`#/projects`)
- Grid of project cards (2-col on desktop, 1-col mobile)
- Each card: project name (bold), goal (2-line clamp), status badge, progress bar (`completion_score` 0–1), task status pill counts (e.g. "3 running · 5 done · 2 ready")
- "New Project" button in topbar → slide-in panel or modal
- Empty state: illustrated empty state with CTA

### 2. Project Detail (`#/project/:id`)
- Topbar: project name + status badge + "Wake Queue" button + breadcrumb
- **Tab bar**: Tasks | Board | Knowledge Base
- **Tasks tab**: filterable list. Filter chips for status + priority dropdown. Each row: title, status badge, priority badge, retry count (🔄N if >0), assigned_role chip. Click → task detail.
- **Board tab**: Kanban columns (pending | ready | running | review | done | failed). Cards show title + priority badge. Drag optional, click to navigate.
- **Knowledge Base tab**: list of KB entries (content snippet 2-line clamp, source badge, timeAgo). "Add Knowledge" → inline form.
- "New Task" button → slide-in panel with: title (required), description (textarea), acceptance_criteria (textarea), priority (select), model_override (text)

### 3. Task Detail (`#/task/:id`)
- Topbar: task title + status select (inline, changes on select) + breadcrumb
- **Meta card**: priority (inline select), assigned_role, retry_count, model_override, blocker_reason (red alert card if set)
- **Description** + **Acceptance Criteria** as readable prose blocks (not inputs unless editing)
- Edit button → toggles to editable textareas + save
- **Run History**: timeline of runs. Each: role chip, model tag, status badge, time range, qa_verdict. Expandable to show input/output in monospace code blocks.
- **Comments**: chat-style list (author avatar placeholder, name, timeAgo, content). "Add comment" at bottom — textarea + submit.

---

## Interaction Patterns

- **Navigation**: hash-based (`#/projects`, `#/project/foo`, `#/task/42`)
- **Sidebar**: shows project list, highlights active project. Collapses to icon-only on mobile.
- **Modals/panels**: prefer slide-in side panels over modals for creation flows
- **Status changes**: inline selects that PUT on change — show a brief success flash
- **Auto-refresh**: 30s polling, subtle "last updated X ago" indicator
- **Loading**: skeleton screens, not spinners
- **Errors**: inline error banners, not alerts
- **Empty states**: friendly text + action button

---

## Technical Constraints

- **Single HTML file** — all CSS and JS inline, no CDN dependencies
- Served at `/orchard/ui`, proxied via port 18790
- API base: `/orchard` (prefix already set in `const API = '/orchard'`)
- All `api()` calls should use paths like `/projects`, `/tasks/42`, etc. (NOT `/orchard/projects`)
- Do not embed gateway tokens in HTML or client-side source
- Standalone UI should prompt for a gateway token or read it from localStorage
- Gateway-route deployments may inject auth server-side, but served HTML must not contain real secrets
- Hash routing, `hashchange` + `DOMContentLoaded` listeners
- Build: `cd /home/leo/.openclaw/workspace/orchard && npm run build` (tsc, must pass clean)

---

## Deliverable

Replace `/home/leo/.openclaw/workspace/orchard/src/ui/dashboard.html` with the complete redesigned SPA.

Then run:
```bash
cd /home/leo/.openclaw/workspace/orchard && npm run build
```

Verify build passes. Do a quick API smoke test with a real local gateway token from your own OpenClaw setup:
```bash
TOKEN="<your-gateway-token>"
curl -s -H "Authorization: Bearer $TOKEN" http://127.0.0.1:18789/orchard/projects
```

Report done with: what changed, line count, any deviations from the brief.
