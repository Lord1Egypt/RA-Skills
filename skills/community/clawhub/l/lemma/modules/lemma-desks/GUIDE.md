---
name: lemma-desks
description: "Use when building a Lemma desk: design multi-page operator workflows, define pages and reusable components before coding, scaffold the app correctly, wire lemma-sdk, test realistic behavior, and upload a verified bundle."
---

# Lemma Desks

Use this skill when building or updating a Lemma desk.
A desk is the pod's full operator web application, not a one-page landing screen.

## Required Flow

Always work through this sequence:

1. define the operator loop and information architecture in this skill
2. produce a mandatory page map, component plan, and state matrix before coding
3. scaffold the app correctly
4. pass the backend readiness gate
5. wire the client and auth correctly
6. build real screens around real pod resources
7. test the desk in a browser
8. upload only after verification

Mechanical build guidance lives here.
Core design guidance also lives here.
`DESIGN.md` is supplemental reference only.
Testing guidance lives in `testing.md`.

Do not start desk work as the first proof that a pod works.
Tables, folders, functions, agents, and workflows should be designed and tested first.

Choose a theme from awesome-design-md

Use the [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md)
repo as the source of truth for theme tokens. Each file in that repo is a
design-md for one real product. Read the file for your chosen theme and extract
from it — do not invent tokens.


## Architecture-First Contract

Before writing component code, define these artifacts in the response.
If these are missing, stop and design before coding.

### 1. Operator loop brief

Capture:

- primary operator role
- repeated job to be done
- scan fields (what users triage quickly)
- focused task (what users need detail views for)
- primary actions (approve, assign, escalate, create, resolve)

### 2. Mandatory page map

For each route, include:

- route path
- page purpose
- primary actions
- data dependencies (`records`, `functions`, `workflows`, `tasks`)
- navigation entry points and exits

Minimum expectation for non-trivial desks:

- one queue or list page
- one detail page or detail pane
- one action page or modal flow for create/edit/decision work

### 3. Mandatory component system plan

Define app-shell and domain components before implementation.

Required app-shell components:

- `AppShell`
- `Sidebar` or `TopNav` (as chosen by IA)
- `Topbar`
- `PageHeader`
- `EmptyState`
- `ErrorState`

Required domain components (adapt names to domain):

- queue/list component, for example `TicketsTable`
- detail component, for example `TicketDetailPanel`
- action component, for example `AssignOwnerDialog` or `ApprovalActions`

Reuse rule:
Do not duplicate near-identical page-specific components when one shared component can serve multiple routes.

### 4. Mandatory state matrix

For every primary page, define behavior for:

- loading
- empty
- error
- success
- permission denied

Do not ship pages that only render success state.

## Desk Complexity Gate

Default to a multi-route desk, not a single-page app.

Use a single page only when all are true:

- one operator job only
- one primary entity only
- no distinct review/detail/action contexts
- no need for cross-page navigation

If two or more operator jobs exist, require multi-route IA.
If queue and detail both exist, require list-detail or separate detail route.

## Banned UI Anti-Patterns

- landing-page hero layout as the main desk UI
- decorative KPI wall with no operator action path
- fake placeholder actions not wired to real backend calls
- one giant page mixing unrelated workflows with no route boundaries
- static mock data as the only source of truth for critical actions

## Backend Readiness Gate

Do not wire desk actions until backend readiness is verified.

Quick validation checklist:

- integration smoke-test artifacts exist for each external app call path
- every desk-triggered function has a green standalone smoke test
- every workflow started from the desk has a green test run
- function names and example payloads are documented for desk developers
- failed upstream calls surface explicit UI or API errors instead of silent success states

If any item is red, stop desk action wiring and fix backend readiness first.

## When To Use This Skill

Use `lemma-desks` when humans need:

- navigation across multiple jobs or screens
- queues, inboxes, forms, and detail views
- repeatable operational workflows
- a structured front end on top of pod resources

Do not use a desk as a static poster or a single decorative page.

## Design Reference Usage

Use `DESIGN.md` as optional deeper reference for layout archetypes and theme polish.
Do not depend on reading `DESIGN.md` to enforce core architecture rules; enforce them from this `GUIDE.md` first.

## Scaffold

```bash
bash ./modules/lemma-desks/scripts/init-artifact.sh expense-desk --pod-id <pod-id>
```

The scaffold sets up:

- Vite + React + TypeScript
- `lemma-sdk@latest`
- Tailwind and helpers
- `.env.local`
- preview helpers
- bundle script
- `@/` path alias

If `--pod-id` is omitted, replace the placeholder before running the app.

## Required Env

```bash
VITE_LEMMA_API_URL=${LEMMA_BASE_URL}
VITE_LEMMA_AUTH_URL=${LEMMA_AUTH_URL}
VITE_LEMMA_POD_ID=${LEMMA_POD_ID}
LEMMA_DESK_DEV_PORT=5173
```

## Critical Wiring Rules

1. Import `AuthGuard` from `lemma-sdk/react`, not `lemma-sdk`.
2. Import `lemma-sdk/react/styles.css` in `main.tsx`.
3. Create the `LemmaClient` once at module load time in `src/lib/client.ts`.
4. Every desk needs a `public_slug` for its eventual hosted URL.

## Client Singleton

`src/lib/client.ts`

```ts
import { LemmaClient } from "lemma-sdk";

export const client = new LemmaClient({
  apiUrl: import.meta.env.VITE_LEMMA_API_URL,
  authUrl: import.meta.env.VITE_LEMMA_AUTH_URL,
  podId: import.meta.env.VITE_LEMMA_POD_ID,
});
```

## main.tsx Wiring

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { AuthGuard } from "lemma-sdk/react";
import "lemma-sdk/react/styles.css";
import App from "./App";
import { client } from "./lib/client";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AuthGuard client={client}>
      <App />
    </AuthGuard>
  </React.StrictMode>,
);
```

## Operation Decision Rule

| Situation | Call |
| --- | --- |
| Single-table write | `client.records.create/update/delete` |
| Reusable deterministic multi-table action | `client.functions.runs.create` |
| Judgment-heavy action | `client.tasks.create` |
| Multi-step orchestration | `client.workflows.runs.start` |

## Project Structure Expectations

Default structure for non-trivial desks:

- `src/app/AppShell.tsx` for shared layout chrome
- `src/routes/*` for route-level pages
- `src/components/*` for reusable UI and domain components
- `src/features/<domain>/*` for domain-specific view models and action handlers
- `src/lib/client.ts` for the Lemma client singleton

Do not implement the entire desk in one `App.tsx` file unless the desk passes the single-page complexity exception.

## SDK Patterns

### List rows

```ts
const response = await client.records.list("accounts", {
  limit: 20,
  sortBy: "updated_at",
  order: "desc",
});
const items = response.items.map((item) => item.data ?? item);
```

### Create a record

```ts
await client.records.create("tasks", {
  title: "Send follow-up",
  status: "OPEN",
  source: "desk",
});
```

### Call a function

```ts
const run = await client.functions.runs.create("create_pipeline_alert", {
  input: { opportunity_id: "opp_123", severity: "HIGH" },
});
```

### Run an agent via task

```ts
const task = await client.tasks.create({
  agent_name: "meeting_brief_writer",
  input_data: { opportunity_name: "Acme", stage: "PROPOSAL" },
});
const messages = await client.tasks.messages.list(task.id!);
```

### Start a workflow

```ts
const run = await client.workflows.runs.start("opportunity-intake", {});
```

## Assistant Embedding

Use `AssistantEmbedded` when the desk needs a ready-made conversational surface.
It is the recommended default when a desk should expose an assistant without building the entire chat UI from scratch.

## Build, Test, Upload

### Build and preview

```bash
npm run dev
npm run preview:url
npm run build
npm run bundle
```

### Test before upload

Read `testing.md` and verify:

- auth works
- the desk loads the expected pod
- core user actions succeed
- console and network behavior look sane
- the main operator flow works in a browser

### Upload

```bash
lemma desk bundle-upload expense-desk \
  --pod-id <pod-id> --source-dir . --html-file ./bundle.html
```

Only upload after real preview and browser validation.

## Upload Quality Gate

Before upload, verify all are true:

- information architecture is implemented as designed (routes, tabs, or list-detail)
- queue/list, detail, and action surfaces are present for non-trivial desks
- every critical action is wired to real `records`, `functions`, `tasks`, or `workflows` calls
- loading, empty, error, success, and permission-denied states exist on primary pages
- no placeholder buttons or dead-end UI flows remain

## Known CLI Behavior

Read shared CLI behavior notes in [`../lemma-main/references/known-cli-behavior.md`](../lemma-main/references/known-cli-behavior.md), especially command payload shapes for function and workflow runs.

## Common Failure Modes

### `TypeError: Cannot read properties of undefined (reading 'auth')`

The client is not a module-level singleton or is imported incorrectly.

### Sign-in page is unstyled

`lemma-sdk/react/styles.css` is missing.

### Dev server unreachable through workspace preview

The Vite config is missing `host: "0.0.0.0"` and `allowedHosts: true`.

### Actions fail after the UI loads

Check:

- `VITE_LEMMA_POD_ID`
- resource names
- workflow or function names
- backend resource availability in the pod

## Related Files

- `DESIGN.md`: operator workflow, nav, and layout guidance
- `testing.md`: browser testing and upload verification guidance

## Related Skills

Route to:

- `lemma-main` when the operating model still needs design work
- `lemma-workspace` when the desk is being served or tested inside a workspace
- `lemma-widget` when the user needs an inline visual instead of a full desk
