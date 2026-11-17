---
name: miaoda-app-builder
description: >-
  Create, modify, generate, and deploy websites, web apps, dashboards, SaaS
  products, internal tools, interactive web pages, Weixin mini program, native
  iOS / Android mobile apps, games on the Baidu Miaoda (秒哒) platform using
  natural-language instructions.
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - MIAODA_API_KEY
    primaryEnv: MIAODA_API_KEY
---

# Miaoda (秒哒) App Builder

Miaoda (秒哒) is a **chat-driven full-stack application builder**.
Official website: https://www.miaoda.cn

Users describe what they want in natural language and Miaoda generates a **production-ready web product**, including:

- frontend UI
- backend services
- database schema
- integrations
- deployable hosting

Typical outputs include:

- websites
- web applications
- dashboards
- SaaS products
- admin panels
- internal tools
- landing pages
- interactive web pages
- browser games and mini games
- Weixin mini programs
- native iOS apps
- native Android apps
- research reports
- data analysis documents
- PPT / presentations
- general content documents

This skill enables AI agents to interact with the **Miaoda(秒哒) platform** to create, iterate, generate, and deploy applications.

All platform operations must be executed through the packaged CLI script:

```bash
python scripts/miaoda_api.py <command> [options]
```

Do **not** call platform APIs directly. Always use the CLI commands provided by this skill.

# When to Use This Skill

Use this skill whenever the user wants to:

* create a **website**
* create a **webpage**
* build a **web application**
* build a **dashboard**
* create a **SaaS product**
* build an **admin panel**
* build an **internal tool**
* create a **landing page**
* build an **interactive web page**
* create a **browser game**
* create a **mini game**
* build a **native iOS app**
* build a **native Android app**
* build a **mobile app** (iOS / Android)
* generate an **MVP web product**
* modify an existing **Miaoda project**
* publish or deploy a **Miaoda application**
* generate a **research report**
* create a **PPT or presentation**
* produce a **data analysis document**
* create any **general content output** (not a deployed app)

Do **not** use this skill for unrelated programming tasks.

---

# Routing Keywords

Trigger this skill if the request includes concepts such as:

* build a website
* create a webpage
* build a web app
* create a SaaS
* build a dashboard
* create an admin panel
* build an internal tool
* create a landing page
* build a browser game
* create a mini game
* build a native iOS app
* build a native Android app
* build a mobile app
* generate a web product
* make a snake game webpage
* build a todo web app
* create a blog site

---

# Example Requests

Examples that should route to this skill:

* "Create a todo list web app"
* "Build a personal blog website"
* "Make a dashboard for sales analytics"
* "Create a SaaS landing page"
* "Build an admin panel"
* "Write a snake game webpage"
* "Create a browser game"
* "Build a mini web game"
* "Build a native iOS habit-tracking app"
* "Make an Android app for expense tracking"
* "I want a mobile app that works on both iPhone and Android"
* "Modify my Miaoda project"
* "Publish this Miaoda app"

---

# Native Mobile Apps (iOS / Android)

Miaoda can generate **native iOS and Android mobile applications**, not just web
products. The output is a real mobile app project rather than a mobile-adapted
web page.

**How to request it:** state the target platform explicitly in the `chat` text.
There is no separate CLI command or flag — the platform decides the output form
from the natural-language description.

```bash
python scripts/miaoda_api.py chat --text "创建一个原生 iOS 记账 App，支持分类统计和月度报表"
python scripts/miaoda_api.py chat --text "创建一个安卓原生 App，用于扫码记录仓库出入库"
python scripts/miaoda_api.py chat --text "创建一个 iOS 和 Android 双端原生 App，功能是每日习惯打卡"
```

**Guidance for agents:**

* Say **原生 App / native app** plus the platform (**iOS**, **Android**, or both)
  in the first `chat` message. Vague wording like "做个 App" is often interpreted
  as a web app.
* Mention mobile-specific needs in the PRD stage — push notifications, camera /
  scanning, offline storage, location, biometric login — so they land in the
  generated project.
* If the user only says "手机上能用" or "移动端", that usually means a
  mobile-friendly **web** page. Confirm which one they want before committing:
  a native app and a responsive web app are different deliverables.
* The lifecycle is unchanged: `chat` → PRD refinement → `generate-app --watch`.
  Publishing is a separate, user-initiated step — do not auto-publish after
  generation; wait for the user to ask to deploy.
* Distribution differs from web. For a native app, check `app-detail` and the
  post-publish trajectory output for the download / distribution entry the
  platform returns; do not assume or construct a web URL.

---

# Stateless Execution Model

The CLI script is **stateless**.

It does not store workflow state between calls.

Application workflow state is maintained by the Miaoda platform and must be inferred from:

* `appId`
* `conversationId`
* application detail
* conversation trajectory events

Agents must pass the appropriate identifiers when continuing conversations or modifying applications.

---

# Application Lifecycle Rules

Miaoda applications follow a strict lifecycle.

Agents must follow these rules.

---

## Initial Creation

For a new application:

1. Start with a `chat` request describing the product.
2. The application enters the **PRD refinement stage**.
3. Continue chatting to refine the specification.
4. When the trajectory contains a **Generate App** button (`type":"button"` and `event":{"name":"generateApp"}` in `result.artifact.parts[].data.actions[]`), trigger application generation using `generate-app`.

Generation is required **only once** during the initial creation.

Generation is the final step of creation. **Do not publish automatically after
generation.** Publishing is a separate step triggered only by an explicit user
request (see *Publishing* below).

---

## Multi-Round Modification

After an application has already been generated:

* **Do not call `generate-app` again.**
* Continue using `chat` with the same `appId` and `conversationId`.

Normal chat messages modify the existing application.

---

## Publishing

Publishing is allowed **after the application has been generated at least once**.

**Publishing is user-initiated — never automatic.** `generate-app` is the terminal
step of application creation. Do **not** chain `publish` after a successful
`generate-app`. Only run `publish` when the user explicitly asks to publish /
deploy / 上线 / 发布 the application in conversation. After generation completes,
report that the app is generated and ready, and stop — wait for the user to
request deployment.

Rules:

* Publishing does **not require another generation step**
* Publishing may happen anytime after the first generation
* Publishing is triggered **only** by an explicit user request, not as a routine
  follow-up to `generate-app`
* Publishing must be followed by **status polling** (or use `--wait` flag)
* **Do not retry or repeat `publish` after a successful execution.** A publish is
  successful when the CLI exits successfully and the final status is `SUCCESS`.
  Missing or delayed downstream output, missing frontend events, an incomplete
  conversation reply, or any other display/transport issue is **not** a publish
  failure; investigate that separately instead of publishing again.
* Retry `publish` only when the command itself fails or the final deployment
  status is explicitly `FAILED`. Do not retry while the status is
  `PROCESSING`, `RUNNING`, or `UNDER_RELEASE`; keep polling.

Typical deployment flow:

```
publish → publish-status polling
```

Or use the `--wait` flag to auto-poll:

```
publish --wait
```

Stop polling when the status becomes:

* `SUCCESS`
* `FAILED`

---

## General Task (No Generation Required)

For general tasks such as research reports, PPT, or analysis documents, the
platform processes the request entirely in the chat stage.

Rules:

* There is **no PRD refinement stage**
* There is **no `generate-app` step**
* There is **no `publish` step**
* The task is complete when `chat` returns `{"needGenerateApp": false, "appType": "TASK"}`

Do **not** call `generate-app` for general tasks.

---

# Application URLs

Publishing returns the application's public URL in the platform response. Use
the value returned by the CLI; do not infer a URL from `appId`, because test and
production environments use different domains.

For a deployment that should wait for completion, use:

```bash
python scripts/miaoda_api.py publish --app-id <app_id> --wait
```

# Standard Workflow

## Create New Application

```
chat → PRD refinement → generate-app --watch → (stop; report app is ready)
```

Generation is the final automatic step. **Do not publish here.** Publishing
happens only when the user later asks to deploy (see *Deploy Application* below).

---

## Modify Existing Generated Application

```
chat → chat → chat
```

(no additional generation step required)

---

## Deploy Application

Run **only** when the user explicitly asks to publish / deploy / 上线 / 发布.

```
publish → publish-status polling
```

Or:

```
publish --wait
```

---

## General Task (Direct Completion)

```
chat → state:completed (needGenerateApp: false)
```

No generate-app or publish step required.

---

# Available Commands

All commands are executed via the CLI script.

**Authentication**:

* If `MIAODA_API_KEY` is set, the CLI uses it for direct Miaoda API access.
* When running inside qianfan-desk without a key, the CLI automatically uses
  the session-bound Miaoda proxy when `DUMATE_SESSION_ID` and the desktop
  gateway/scheduler environment are available.
* Outside qianfan-desk, set `MIAODA_API_KEY` explicitly before running commands.

Examples below show the explicit-key form for clarity.

```bash
export MIAODA_API_KEY="your_api_key_here"
```

---

## list-apps

List all applications belonging to the authenticated user.

**Usage:**

```bash
python scripts/miaoda_api.py list-apps [--brief]
```

**Optional Parameters:**
- `--brief`: Output only key fields: `appId`, `name`, `type`, `appFocus`, `host`, `updatedAt`. Recommended for agents to reduce token usage.
- `--name NAME`: Filter by app name (substring)
- `--page PAGE`: Page number (default: 1)
- `--size SIZE`: Page size (default: 12)

**Example:**

```bash
export MIAODA_API_KEY="sk_xxxxx"

# Brief mode (recommended for agents)
python scripts/miaoda_api.py list-apps --brief

# Full mode
python scripts/miaoda_api.py list-apps
```

**Returns:** JSON array of applications with `appId`, `name`, `type`, etc.

---

## app-detail

Get detailed information about a specific application. **Automatically injects `conversationId`** into the response by default — no need to call `get-context-id` separately.

**Usage:**

```bash
python scripts/miaoda_api.py app-detail --app-id <app_id> [--no-context]
```

**Required Parameters:**
- `--app-id APP_ID`: Application ID

**Optional Parameters:**
- `--no-context`: Skip auto-fetching `conversationId` from trajectory (faster, but response will not contain `conversationId`)

**Example:**

```bash
export MIAODA_API_KEY="sk_xxxxx"
python scripts/miaoda_api.py app-detail --app-id app-abc123xyz
```

**Returns:** JSON object with application details, configuration, and status. `data.conversationId` is automatically populated.

**appFocus — Publish Readiness Guide:**

After calling `app-detail`, check `data.appFocus` to determine whether publishing is allowed:

| `appFocus` | Meaning | Can Publish? |
|------------|---------|--------------|
| `NOT_GENERATE` | Not yet generated | No — call `generate-app` first |
| `WAITING` | Queued for generation | No — wait for generation to complete |
| `UNDER_CREATING` | Generation in progress | No — wait for generation to complete |
| `CREATE_FAILED` | Generation failed | No — retry `generate-app` |
| `DESIGNING` | Generated, ready to edit/deploy | **Yes** |
| `RELEASED` | Already published | **Yes** (only for an intentional new deployment after changes; not for retrying a successful publish) |
| `RELEASE_FAILED` | Last publish explicitly failed | **Yes** (retry allowed only after confirming the failed deployment) |
| `UNDER_RELEASE` | Publish currently in progress | Wait — do not call publish again |

**Rule:** Only proceed with `publish` when `appFocus` is `DESIGNING`, `RELEASED`, or `RELEASE_FAILED`.
When `appFocus` is `RELEASED`, do not publish again merely because downstream
UI output or frontend events are missing; check the existing publish result and
the event/rendering path first.

---

## get-context-id

Recover the `conversationId` for an existing app by reading its trajectory. Useful when the `conversationId` has been lost after a session reset.

**Usage:**

```bash
python scripts/miaoda_api.py get-context-id --app-id <app_id>
```

**Required Parameters:**
- `--app-id APP_ID`: Application ID

**Optional Parameters:**
- `--fetch-timeout SECONDS`: Request timeout in seconds (default: 10)

**Example:**

```bash
export MIAODA_API_KEY="sk_xxxxx"
python scripts/miaoda_api.py get-context-id --app-id app-abc123xyz
```

**Returns:** `{"appId": "app-abc123xyz", "conversationId": "conv-def456uvw"}`

**Use Cases:**
- Need to modify a previously created app in a new session but `conversationId` is lost
- Use the returned `conversationId` with `chat --app-id --context-id` to resume modification

---

## conversation-history

Show a human/agent-readable summary of past interactions for an app. More convenient than `trajectory` or `fetch-trajectory` for quickly understanding what happened in previous sessions.

**Usage:**

```bash
python scripts/miaoda_api.py conversation-history --app-id <app_id> [options]
```

**Required Parameters:**
- `--app-id APP_ID`: Application ID

**Optional Parameters:**
- `--full`: Show full content instead of truncated summaries (default: truncate at 200 chars)
- `--limit N`: Only show the last N conversation turns
- `--fetch-timeout SECONDS`: Request timeout in seconds (default: 10)

**Example:**

```bash
export MIAODA_API_KEY="sk_xxxxx"

# View conversation history summary
python scripts/miaoda_api.py conversation-history --app-id app-abc123xyz

# Only show the last 3 turns
python scripts/miaoda_api.py conversation-history --app-id app-abc123xyz --limit 3

# Show full content without truncation
python scripts/miaoda_api.py conversation-history --app-id app-abc123xyz --full
```

**Returns:** JSON Lines, one entry per meaningful turn:

```json
{"eventId": 5, "role": "user", "type": "message", "content": "创建一个待办事项应用..."}
{"eventId": 865, "role": "agent", "type": "file", "content": "[file: 需求文档.md]"}
{"eventId": 880, "role": "user", "type": "message", "content": "生成应用"}
```

**Use Cases:**
- Quickly understand what happened in previous sessions before resuming work
- Determine which phase the app is in (PRD refinement / generated / modified)
- Check for unfinished modifications or cancelled tasks

---

## chat

Start or continue a conversation to create or modify an application.

**Usage:**

```bash
python scripts/miaoda_api.py chat --text "description" [options]
```

**Required Parameters:**
- `--text TEXT`: The message/instruction to send

**Optional Parameters:**
- `--context-id CONTEXT_ID`: Conversation ID of an existing app.
- `--app-id APP_ID`: Application ID of an existing app.
- `--query-mode QUERY_MODE`: Query mode (default: deep_mode)
- `--input-field-type INPUT_FIELD_TYPE`: Input field type (default: web)
- `--poll-interval SECONDS`: Seconds between trajectory polls (default: 2.0)
- `--fetch-timeout SECONDS`: Per-request timeout for each trajectory fetch (default: 10)
- `--no-stream`: Return raw chat POST response without trajectory polling
- `--prompt-generate`: After polling, interactively ask whether to submit app generation if text was returned
- `--node-json JSON`: **LGUI mode** — pass a JSON string describing the currently-selected UI node (file path, line range, tag, current styles, etc.). When set, an extra `kind: "data"` part is appended to the request so the Agent can pinpoint the exact node instead of searching the codebase. See the **LGUI (Live-GUI) Node-Scoped Editing** section below.

> **⚠️ IMPORTANT — `--app-id` and `--context-id` must always be used together.**
>
> | Intent | `--app-id` | `--context-id` |
> |--------|-----------|----------------|
> | Create a brand-new app | omit | omit |
> | Continue / modify an existing app | required | required (conversationId) |
>
> Passing `--app-id` **without** `--context-id` will **NOT** modify the existing app.
> The platform will silently create a **new** app every time. The CLI will now raise an error in this case to prevent accidental app proliferation.

**Examples:**

**1. Create a new application:**

```bash
export MIAODA_API_KEY="sk_xxxxx"
python scripts/miaoda_api.py chat --text "创建一个待办事项管理应用"
```

Response includes `appId` and `contextId` for subsequent calls.

**2. Continue conversation (refine PRD):**

```bash
python scripts/miaoda_api.py chat \
  --text "添加优先级标记功能" \
  --app-id app-abc123xyz \
  --context-id conv-def456uvw
```

**3. Modify existing generated app:**

```bash
python scripts/miaoda_api.py chat \
  --text "把按钮颜色改成蓝色" \
  --app-id app-abc123xyz \
  --context-id conv-def456uvw
```

**4. LGUI mode — modify one specific UI node:**

```bash
python scripts/miaoda_api.py chat \
  --text "改成蓝底黑字" \
  --app-id app-abc123xyz \
  --context-id conv-def456uvw \
  --node-json '{"type":"node","node":{"id":"src/pages/HomePage.tsx:30:8","path":"src/pages/HomePage.tsx","line":"30","endLine":"35","tag":"H1","content":{"text":"HelloWorld"},"style":{"color":"rgb(46, 26, 15)","backgroundColor":"rgba(0, 0, 0, 0)"}}}'
```

**Important Notes:**
- Extract `appId` and `contextId` from the response and save them
- Use these IDs for all subsequent operations on the same app
- The first `chat` creates the app and starts PRD refinement
- After generation, `chat` directly modifies the app (no `generate-app` needed)

---

# LGUI (Live-GUI) Node-Scoped Editing

LGUI mode lets a `chat` message carry **the exact UI node the user is pointing
at**, so the platform edits that node directly instead of inferring the target
from natural language alone.

## Difference from a plain chat

A plain `chat` sends only text:

```json
"parts": [
  {"kind": "text", "text": "把整体配色换成暖色调的橙粉渐变风格"}
]
```

The Agent must search the codebase itself to work out what to change.

LGUI appends one extra `kind: "data"` part alongside the text:

```json
"parts": [
  {"kind": "text", "text": "改成蓝底黑字"},
  {
    "kind": "data",
    "data": {
      "type": "node",
      "node": {
        "id": "src/pages/HomePage.tsx:30:8",
        "path": "src/pages/HomePage.tsx",
        "line": "30",
        "endLine": "35",
        "isRoot": false,
        "tag": "H1",
        "content": {
          "text": "HelloWorld",
          "className": "gradient-text text-5xl font-bold",
          "allowLink": true
        },
        "customAttr": {"href": null, "target": null},
        "style": {
          "color": "rgb(46, 26, 15)",
          "fontSize": "72px",
          "fontFamily": "\"Space Grotesk\"",
          "margin": "0px",
          "radius": "0px",
          "backgroundColor": "rgba(0, 0, 0, 0)",
          "backgroundImage": "linear-gradient(135deg, rgb(249, 115, 22), rgb(236, 72, 153))",
          "borderColor": "rgb(245, 230, 214)",
          "borderWidth": "0px",
          "borderStyle": "solid"
        }
      }
    }
  }
]
```

Everything else in the request — `contextId`, `metadata`, `queryMode`, the
lifecycle, the trajectory polling — is identical to a plain `chat`. LGUI is
purely additive.

## Node fields

| Field | Meaning |
|-------|---------|
| `id` | Node identifier, conventionally `<path>:<line>:<column>` |
| `path` | Source file containing the node |
| `line` / `endLine` | Line range of the node in that file |
| `isRoot` | Whether this is the root node of the page |
| `tag` | HTML/JSX tag name (e.g. `H1`, `DIV`, `BUTTON`) |
| `content.text` | Current visible text |
| `content.className` | Current class list |
| `content.allowLink` | Whether the node may carry a link |
| `customAttr` | Element attributes such as `href` / `target` |
| `style` | Current computed styles (color, font, spacing, border, background…) |

Only `path` plus a line range is strictly needed to locate a node; the more
fields you supply, the less the Agent has to re-derive, and the more reliably a
relative instruction ("改成蓝底黑字", "字号再小一点") resolves.

## Usage

```bash
python scripts/miaoda_api.py chat \
  --text "改成蓝底黑字" \
  --app-id <app_id> \
  --context-id <conversation_id> \
  --node-json '<json>'
```

`--node-json` accepts either form:

* the wrapper — `{"type":"node","node":{...}}`
* the bare node object — `{"id":"...","path":"...","line":"30",...}` (the CLI
  wraps it automatically)

Invalid JSON, or JSON that is not an object, exits with an error before any
request is sent.

## When to use LGUI vs plain chat

| Situation | Use |
|-----------|-----|
| User selected/clicked a specific element and you have its node data | `--node-json` |
| Change is scoped to one element ("这个标题改成蓝底黑字") | `--node-json` |
| Global change ("整体配色换成暖色调") | plain `chat` |
| Change spans multiple pages or components | plain `chat` |
| Adding a feature or new page | plain `chat` |
| You do not have real node data | plain `chat` — **never fabricate a node** |

**Do not invent node data.** A wrong `path` or line range points the Agent at
the wrong code. Node data must come from an actual selection source (the Miaoda
editor's element picker, or a caller that captured it). Without it, send a plain
`chat` and let the platform locate the target.

**Also note:**
- LGUI applies to **generated** apps — it edits existing UI code, so there must
  already be code to point at. It is not for the PRD stage.
- `--node-json` carries **one** node. For several elements, send one `chat` per
  node, updating `conversationId` from each response, or describe the change in
  plain text.

---

## trajectory

Poll trajectory events until the task reaches a terminal state.

**Usage:**

```bash
python scripts/miaoda_api.py trajectory --app-id <app_id> [options]
```

**Required Parameters:**
- `--app-id APP_ID`: Application ID

**Optional Parameters:**
- `--last-event-id EVENT_ID`: Start eventId; -1 = all events from beginning (default: -1)
- `--poll-interval SECONDS`: Seconds between polls (default: 2.0)
- `--fetch-timeout SECONDS`: Per-request timeout in seconds (default: 10)
- `--sse`: Use legacy SSE streaming instead of polling

**Example:**

```bash
export MIAODA_API_KEY="sk_xxxxx"
python scripts/miaoda_api.py trajectory --app-id app-abc123xyz
```

**Use Cases:**
- Monitor conversation / generation progress
- Detect when PRD refinement is complete (look for Generate App button in `result.artifact.parts[].data.actions[]`)
- Verify generation has completed

---

## fetch-trajectory

Fetch one batch of trajectory events (single request, no polling loop).

**Usage:**

```bash
python scripts/miaoda_api.py fetch-trajectory --app-id <app_id> [options]
```

**Required Parameters:**
- `--app-id APP_ID`: Application ID

**Optional Parameters:**
- `--last-event-id EVENT_ID`: Fetch events after this eventId; -1 = all (default: -1)
- `--fetch-timeout SECONDS`: Request timeout in seconds (default: 10)

**Example:**

```bash
# First call — get all events (note maxEventId from stderr)
python scripts/miaoda_api.py fetch-trajectory --app-id app-abc123xyz

# Subsequent calls — incremental fetch
python scripts/miaoda_api.py fetch-trajectory --app-id app-abc123xyz --last-event-id 345
```

Events are printed to stdout as JSON lines; `{"maxEventId": N, "isTerminal": bool}` is printed to stderr.

**Generate App readiness:** Inspect `result.artifact.parts[].data.actions[]` for an action with `"type":"button"` and `"event":{"name":"generateApp"}`. Example:

```json
{"type":"button","label":"Generate App","value":"Generate App","event":{"name":"generateApp"}}
```

When this button appears, PRD is ready and `generate-app` may be called.

---

## generate-app

Submit app-generation confirmation and return immediately with `appId`/`conversationId` plus the app name (`appName`).

**Usage:**

```bash
python scripts/miaoda_api.py generate-app --app-id <app_id> --context-id <context_id> [options]
```

**Required Parameters:**
- `--app-id APP_ID`: Application ID

**Optional Parameters:**
- `--context-id CONTEXT_ID`: Conversation ID (default: "")
- `--query-mode QUERY_MODE`: Query mode (default: deep_mode)
- `--watch`: Block and poll trajectory until generation completes **(recommended)** (default: return immediately)
- `--poll-interval SECONDS`: Seconds between polls when `--watch` is set (default: 2.0)
- `--fetch-timeout SECONDS`: Per-request timeout in seconds when `--watch` is set (default: 10)

**Example:**

```bash
export MIAODA_API_KEY="sk_xxxxx"
# Recommended: submit and block until generation finishes
python scripts/miaoda_api.py generate-app \
  --app-id app-abc123xyz \
  --context-id conv-def456uvw \
  --watch

# Alternative: submit and return immediately — check status later with fetch-trajectory
python scripts/miaoda_api.py generate-app \
  --app-id app-abc123xyz \
  --context-id conv-def456uvw
```

**Returns:** A JSON line on stdout with `appId`, `conversationId` and `appName`:

```json
{"appId": "app-abc123xyz", "conversationId": "conv-def456uvw", "appName": "待办事项应用"}
```

- With `--watch`, trajectory events are streamed to stdout first and this result line is printed last; without `--watch` it is the only stdout output.
- `appName` is the app's `name`, fetched right after the confirmation (after
  polling when `--watch` is set, so it reflects the finished app); omitted if
  the name cannot be determined.
- The name lookup is best-effort: on failure a warning is printed to stderr
  and the command still succeeds with `appId`/`conversationId`.

**Important:**
- Only call this **once** during initial creation
- Call **only** when trajectory contains a Generate App button in `result.artifact.parts[].data.actions[]`: an action with `"type":"button"` and `"event":{"name":"generateApp"}` (label may vary by locale; use event name for the check). This indicates PRD is ready.
- Do **not** call again for modifications after the first generation
- After this command, use `chat` to modify the generated app

> * **Never** call this command when `chat` returns `"needGenerateApp": false`.
>   General tasks (reports, PPT, analysis) complete in the `chat` step and
>   do not have a generation stage.

---

## publish

Trigger deployment to production.

**Usage:**

```bash
python scripts/miaoda_api.py publish --app-id <app_id> [options]
```

**Required Parameters:**
- `--app-id APP_ID`: Application ID to publish

**Optional Parameters:**
- `--env ENV`: Target environment (default: PRODUCE)
- `--wait`: Auto-poll publish status until SUCCESS or FAILED

**Examples:**

**1. Publish and manually check status:**

```bash
export MIAODA_API_KEY="sk_xxxxx"
python scripts/miaoda_api.py publish --app-id app-abc123xyz
```

Returns `releaseId` immediately. Then poll with `publish-status`.

**2. Publish and auto-wait for completion (recommended):**

```bash
export MIAODA_API_KEY="sk_xxxxx"
python scripts/miaoda_api.py publish --app-id app-abc123xyz --wait
```

This polls automatically and exits when deployment succeeds or fails.

**Important:**
- Application must be generated at least once before publishing
- After successful publish, use the public URL returned by the platform. Do not
  construct it from `appId`.
- A final `SUCCESS` status is terminal for this publish attempt. Do not invoke
  `publish` again because downstream UI output or events were not observed.
  Retry only after a command error or an explicit final `FAILED` status.

---

## publish-status

Check the status of a deployment.

**Usage:**

```bash
python scripts/miaoda_api.py publish-status --release-id <release_id>
```

**Required Parameters:**
- `--release-id RELEASE_ID`: Release ID from `publish` command

**Example:**

```bash
export MIAODA_API_KEY="sk_xxxxx"
python scripts/miaoda_api.py publish-status --release-id app_release_record-xyz789abc
```

**Returns:** JSON with status: `PROCESSING`, `RUNNING`, `SUCCESS`, or `FAILED`

**Usage Pattern:**

```bash
# Get release ID from publish
RELEASE_ID=$(python scripts/miaoda_api.py publish --app-id app-abc123xyz | jq -r '.releaseId')

# Poll status
while true; do
  STATUS=$(python scripts/miaoda_api.py publish-status --release-id $RELEASE_ID | jq -r '.status')
  echo "Status: $STATUS"
  if [[ "$STATUS" == "SUCCESS" || "$STATUS" == "FAILED" ]]; then
    break
  fi
  sleep 5
done
```

**Tip:** Use `publish --wait` to avoid manual polling.

---

## download-source

Download the full generated application source ZIP.

Use this command when the user asks for the complete source code of a Miaoda application, a source ZIP, or a local copy of the generated app project.

**Usage:**

```bash
python scripts/miaoda_api.py download-source --app-id <app_id> [options]
```

**Required Parameters:**
- `--app-id APP_ID`: Application ID

**Optional Parameters:**
- `--env ENV`: Source environment (default: DEV)
- `--output PATH`: Save the ZIP to a specific local path
- `--print-url`: Print the download URL without saving the file

**Examples:**

```bash
export MIAODA_API_KEY="sk_xxxxx"

# Download to an inferred local filename
python scripts/miaoda_api.py download-source --app-id app-abc123xyz

# Download to a specific local path
python scripts/miaoda_api.py download-source --app-id app-abc123xyz --output ./source.zip

# Only print the source ZIP download URL
python scripts/miaoda_api.py download-source --app-id app-abc123xyz --print-url
```

**Returns:** JSON containing `appId`, `name`, `downloadUrl`, and `localPath` when a file is saved.

**Rule:** Use `download-source` for complete application source code. Do not use Agent workspace file commands for this purpose.

---

## list-task-files

List files in the Agent workspace task directory for an application.

Use this command before downloading a specific Agent task artifact, especially when the exact filename is unknown.

**Usage:**

```bash
python scripts/miaoda_api.py list-task-files --app-id <app_id> [--include-docs-dir]
```

**Required Parameters:**
- `--app-id APP_ID`: Application ID

**Optional Parameters:**
- `--include-docs-dir`: Include docs directory files in the listing

**Example:**

```bash
export MIAODA_API_KEY="sk_xxxxx"
python scripts/miaoda_api.py list-task-files --app-id app-abc123xyz
```

**Returns:** JSON containing Agent workspace files, paths, sizes, update times, and source labels.

---

## download-task-file

Download one file from the Agent workspace task directory.

Use this command when the user asks for a specific Agent-generated task artifact, such as a report, image, document, JSON file, or other file listed by `list-task-files`.

**Usage:**

```bash
python scripts/miaoda_api.py download-task-file --app-id <app_id> --filename <filename> [options]
```

**Required Parameters:**
- `--app-id APP_ID`: Application ID
- `--filename FILENAME`: File name or `/workspace/{appId}/tasks/...` path

**Optional Parameters:**
- `--output PATH`: Save the file to a specific local path
- `--print-url`: Print the download URL without saving the file

**Examples:**

```bash
export MIAODA_API_KEY="sk_xxxxx"

# Download by filename
python scripts/miaoda_api.py download-task-file --app-id app-abc123xyz --filename report.pdf --output ./report.pdf

# Download by task path returned from list-task-files
python scripts/miaoda_api.py download-task-file \
  --app-id app-abc123xyz \
  --filename /workspace/app-abc123xyz/tasks/report.pdf
```

**Returns:** JSON containing `appId`, `filename`, `downloadUrl`, `thumbnailUrl` for images, and `localPath` when a file is saved.

**Rule:** Use `list-task-files` first when the user asks for Agent workspace artifacts but does not provide an exact filename.

---

# Download Generated Artifacts

Agents must use these commands for generated artifact downloads:

- Use `download-source` when the user wants the complete generated application source ZIP.
- Use `list-task-files` and `download-task-file` when the user wants a specific Agent workspace artifact.
- Do not call platform HTTP APIs directly.
- Do not invent local paths. Only report a local file path after the CLI successfully saves the file and returns `localPath`.
- If a generation or modification is still running, wait for completion before downloading the latest source ZIP.

---

# Complete Workflow Examples

## Example 1: Create and Deploy a New App

```bash
export MIAODA_API_KEY="sk_xxxxx"
cd ~/.openclaw/skills/miaoda-app-builder

# Step 1: Create app via chat (returns appId + conversationId on first line)
FIRST=$(python scripts/miaoda_api.py chat --text "创建一个简单的计数器应用" | head -1)
APP_ID=$(echo $FIRST | jq -r '.appId')
CONTEXT_ID=$(echo $FIRST | jq -r '.conversationId')

# Step 2: Generate and wait for completion (recommended: --watch auto-polls until done)
python scripts/miaoda_api.py generate-app \
  --app-id $APP_ID \
  --context-id $CONTEXT_ID \
  --watch

# App is now generated and ready. STOP here and report to the user.
# Do NOT publish automatically — publish only when the user explicitly asks to deploy:
# python scripts/miaoda_api.py publish --app-id $APP_ID --wait

```

---

## Example 2: Modify an Existing App

> **IMPORTANT — Always update `CONTEXT_ID` from each `chat` response.**
>
> Each `chat` call prints a JSON header line `{"appId": "...", "conversationId": "..."}`.
> The platform may return an updated `conversationId` in this response.
> **Always capture it and use it for the next `chat` call**, or the next round will create a brand-new app.

```bash
export MIAODA_API_KEY="sk_xxxxx"
cd ~/.openclaw/skills/miaoda-app-builder

APP_ID="app-abc123xyz"

# Step 1: Get app detail — conversationId is auto-injected
DETAIL=$(python scripts/miaoda_api.py app-detail --app-id $APP_ID)
CONTEXT_ID=$(echo $DETAIL | jq -r '.data.conversationId')

# Abort early if conversationId is missing (app may have no history yet)
if [ -z "$CONTEXT_ID" ] || [ "$CONTEXT_ID" = "null" ]; then
  echo "Error: could not retrieve conversationId. Try: get-context-id --app-id $APP_ID"
  exit 1
fi

# Step 2 (optional): Review conversation history to understand previous work
python scripts/miaoda_api.py conversation-history --app-id $APP_ID

# Step 3a: First modification — capture the UPDATED conversationId from the response header
CHAT_RESULT=$(python scripts/miaoda_api.py chat \
  --text "把背景颜色改成深色模式" \
  --app-id $APP_ID \
  --context-id $CONTEXT_ID | head -1)
CONTEXT_ID=$(echo $CHAT_RESULT | jq -r '.conversationId')   # ← UPDATE for next round

# Step 3b: Second modification — uses the updated CONTEXT_ID
CHAT_RESULT=$(python scripts/miaoda_api.py chat \
  --text "添加暗黑模式切换按钮" \
  --app-id $APP_ID \
  --context-id $CONTEXT_ID | head -1)
CONTEXT_ID=$(echo $CHAT_RESULT | jq -r '.conversationId')   # ← UPDATE again

# Step 4: Re-publish ONLY when the user explicitly asks to deploy the changes.
# Do not publish automatically after a modification.
python scripts/miaoda_api.py publish --app-id $APP_ID --wait
```

---

# Command Semantics

## chat

Used to:

* create a new application
* refine PRD specifications
* modify an existing generated application

For a new application, `chat` creates the project and begins the PRD stage.

For an existing application, `chat` performs iterative modifications.

---

## trajectory

Streams conversation progress and system events.

Use this to determine:

* whether PRD generation is ongoing
* whether the app is ready for generation (see generate-app condition below)
* whether generation has completed

---

## generate-app

Triggers application generation.

Call **only** when trajectory contains a Generate App button in `result.artifact.parts[].data.actions[]`: an action with `"type":"button"` and `"event":{"name":"generateApp"}`. This indicates PRD is ready. Do **not** rely on text alone—the button structure is the authoritative signal.

Call **once** during initial creation. Do not call again for modifications.

---

## publish

Triggers application deployment.

Run **only** when the user explicitly requests publishing / deployment (e.g.
"发布/上线/部署这个应用"). Do **not** call it automatically after `generate-app`
or after a modification `chat`.

Use `--wait` flag to auto-poll status (recommended).

Treat `SUCCESS` as terminal. Missing or malformed downstream output is not
evidence that deployment failed and must not trigger another publish.

---

## publish-status

Polls deployment progress until the release completes.

Not needed if using `publish --wait`.

---

# Error Handling

## IAM AccessKey Validation Failed

**Symptom:**

```
IAM access key validation failed.
```

**Cause:**

The configured `MIAODA_API_KEY` is invalid or missing.

**Resolution:**

1. Go to the Miaoda(秒哒) official website:

   https://www.miaoda.cn

2. In the left navigation panel, apply for an available access key.

3. Set the key as the environment variable:

   ```bash
   export MIAODA_API_KEY="sk_xxxxx"
   ```

4. Or create a `.env` file in the skill directory:

   ```bash
   echo "MIAODA_API_KEY=sk_xxxxx" > ~/.openclaw/skills/miaoda-app-builder/.env
   ```

---

## NotOpenSSLWarning

**Symptom:**

```
NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+,
currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'
```

**Cause:**

macOS uses LibreSSL by default, but urllib3 v2 recommends OpenSSL.

**Impact:**

This is a **warning only**. API calls still work correctly.

**Resolution (optional):**

If you want to suppress the warning:

```bash
pip3 install 'urllib3<2'
```

Or ignore it - it doesn't affect functionality.

---

## 秒点不足 (Insufficient Credits)

**Symptom:**

```
[秒点不足] 您的秒点余额不足，无法继续操作。
请前往秒哒官网充值：https://www.miaoda.cn
```

Or within an error message:

```
秒点不足，您可明日再来，或邀请新人立即获得秒点奖励。
```

**Cause:**

Your Miaoda account does not have enough 秒点 (Credits) to perform this operation (e.g., generating or publishing an app).

**Resolution:**

Visit the official Miaoda website to recharge your credits:

**https://www.miaoda.cn**

Log in → navigate to the recharge page → complete payment. Credits are credited immediately.

---

# Error Handling Guidance

Agents should handle the following situations:

* generation requested before the platform indicates readiness
* publish requested before generation has completed
* missing `appId` or `conversationId` (use `get-context-id` to recover a lost `conversationId`)
* interrupted trajectory stream
* failed deployment status
* incorrect or missing parameter values

After a publish command returns successfully, do not republish solely because
downstream UI output or a frontend event is missing. Only a command-level
failure or an explicit final `FAILED` deployment status permits a retry.

If workflow state is unclear, inspect the trajectory or application detail before taking the next action.

**Pro Tips:**
- Always check command `--help` when unsure about parameters
- Use `--wait` flag with `publish` to simplify deployment
- Save `appId` and `contextId` from first `chat` response
- Only call `generate-app` once during initial creation
- After generation, use `chat` directly for modifications
- **Never publish automatically.** Treat `generate-app` as the end of creation
  and publish only when the user explicitly asks to deploy / 发布 / 上线

The final response rules are defined in **Final Output Contract** above. Do not
add a second sharing rule or expose editor/production URLs in ordinary text.
