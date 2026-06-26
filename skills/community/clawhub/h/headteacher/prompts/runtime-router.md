# Runtime Router

Use this prompt after setup is complete.

The runtime has two top-level capability families:

1. `data operations`
2. `generate artifact`

Always identify the family first, then choose the primary intent.

## Intent routing

Route each user request into exactly one primary intent:

- `setup workspace`
- `connect backend`
- `bootstrap schema`
- `inspect existing workspace`
- `migrate from subject-teacher base`
- `append records`
- `query student/class data`
- `generate artifact`
- `sync artifact`

## Routing rules

### `setup workspace`

Use when no workspace manifest exists or setup is incomplete.

### `connect backend`

Use when the user wants to switch or add Feishu / Notion / Obsidian.

### `inspect existing workspace`

Use when the user provides a Base token, Base link, or existing workspace path.

### `migrate from subject-teacher base`

Use when the existing Feishu Base looks like a subject-teacher database.

### `append records`

Use for student info, grades, conduct logs, parent communication, seat plans, duty schedules, committee updates.

Within this intent, distinguish:

- one-time import: bulk initialize or migrate existing material
- dynamic append: add new exam, conduct, contact, or schedule records during daily use

### `query student/class data`

Use for summaries, statistics, dashboards, follow-up questions, and class status reports.

Within this intent, distinguish:

- longitudinal read: one student across time
  - examples: timeline, growth path, repeated contacts, behavior trend
- horizontal read: many students at one time slice
  - examples: current class snapshot, partial cohort comparison, one exam or one week view

### `generate artifact`

Use for `.docx`, `.xlsx`, `.pptx` outputs only after structured data exists.

Typical subtypes:

- arrangement artifacts
  - seat plan
  - duty schedule
  - committee table
- presentation / communication artifacts
  - parent meeting PPT
  - class notice
  - parent visit record

If the request is for a seat plan or duty schedule, ask which arrangement attributes matter most, such as:

- score
- gender
- height
- dorm or group
- behavior or conduct constraints

### `sync artifact`

Use when the user wants generated files uploaded or linked back to the backend.
