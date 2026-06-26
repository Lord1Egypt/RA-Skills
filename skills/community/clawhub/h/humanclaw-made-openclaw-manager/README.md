# OpenClaw Manager

OpenClaw Manager is a standalone local control plane for OpenClaw.

It keeps work filesystem-first under `~/.openclaw/skills/manager/` and uses a shadow-first model:

- every thread starts as a lightweight `ThreadShadow`
- only meaningful threads are promoted into durable `Session` + `Run` state
- summaries, checkpoints, attention, snapshots, and capability facts stay local

It is not a cloud service. It is a local Node.js skill plus a local sidecar that runs on your machine.

## Security at a glance

- the sidecar binds to `127.0.0.1` by default
- the sidecar does not auto-start until you explicitly allow it once
- bootstrap only checks a local loopback health endpoint
- raw chat transcripts are not uploaded anywhere by default
- connectors do nothing externally until you explicitly configure them
- state is stored locally under `~/.openclaw/skills/manager/`

Read [SECURITY.md](SECURITY.md) for the exact environment variables, startup behavior, and connector boundaries.

## Who this is for

- OpenClaw users who want a local manager for real work threads
- developers and power users who are comfortable installing Node-based tools
- teams that want resumable local state without shipping raw logs elsewhere

## Who this is not for

- people looking for a zero-config browser SaaS
- users who do not want to install Node.js or run a local process
- anyone expecting a hosted multi-user dashboard out of the box

## What problem it solves

OpenClaw conversations often disappear into long threads. OpenClaw Manager fixes that by:

- observing every thread before it becomes durable work
- promoting only the threads that deserve a managed session
- keeping checkpoints and attention local
- making it fast to resume work without re-reading the whole thread
- turning closed work into reusable capability facts and reports

## Core model

- `ThreadShadow`: pre-session observation for chat and connector threads
- `Session`: promoted work thread with durable summary and state
- `Run`: one concrete execution attempt inside a session
- `Event`: append-only JSONL fact log
- `Checkpoint`: resumable state for the active run
- `AttentionUnit`: scored control-plane alert
- `CapabilityFact`: reusable closure fact derived from real work

## What is implemented

- standalone OpenClaw-native bootstrap with consent-gated sidecar autostart
- loopback-only local sidecar API by default
- shadow-first thread interception and promotion queue
- filesystem-first durable state
- resumable `session / run / event / checkpoint / spool` control plane
- attention queue plus `session map / focus / risk / drift` views
- source-specific connector normalization for Telegram, WeCom, Email, and GitHub
- redacted task snapshots, run evidence snapshots, and capability snapshots
- capability facts, graph summary, anonymized export, and markdown reports

## Repository layout

```text
openclaw-manager/
|- AGENTS.md
|- README.md
|- SECURITY.md
|- SKILL.md
|- skill.yaml
|- docs/
|- schemas/
|- scripts/
|- src/
|  |- api/
|  |- connectors/
|  |- control-plane/
|  |- exporters/
|  |- skill/
|  |- storage/
|  `- telemetry/
`- templates/
```

## Requirements

- Node.js 20+
- npm 10+

## Download

```bash
git clone https://github.com/ZephyrChen0754/openclaw-manager.git
cd openclaw-manager
```

## Fastest path

If you want the shortest safe path:

```bash
npm ci
npm run build
npm run dev
```

That starts the local sidecar manually at `http://127.0.0.1:4318`.

If you want future bootstrap runs to auto-start the local sidecar after explicit consent:

```bash
npm run consent:autostart
npm run bootstrap
```

## One-click install

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

Install the runtime and also copy the skill into `$CODEX_HOME\skills\openclaw-manager`:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -InstallSkill
```

### macOS / Linux

```bash
bash scripts/install.sh
```

Install the runtime and also copy the skill into `$CODEX_HOME/skills/openclaw-manager`:

```bash
bash scripts/install.sh --install-skill
```

The installer uses the official npm registry and `npm ci`. It does not use global `npm -g` installation.

## Install modes

### 1. Run the sidecar only

Use this when you only want the local API and durable state:

```bash
npm ci
npm run build
npm run dev
```

### 2. Install as a local skill

Use this when you want the repo copied into `$CODEX_HOME/skills/openclaw-manager`:

- Windows: `powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -InstallSkill`
- macOS/Linux: `bash scripts/install.sh --install-skill`

### 3. Local development

Use this when you want to edit code, rebuild often, and run checks:

```bash
npm ci
npm run check
npm run build
npm run dev
```

## Configure

Copy `.env.example` to `.env.local`.

Typical values:

```env
OPENCLAW_MANAGER_STATE_ROOT=
OPENCLAW_MANAGER_NODE_ID=local-node-01
OPENCLAW_MANAGER_BIND_HOST=127.0.0.1
OPENCLAW_MANAGER_SIDECAR_URL=http://127.0.0.1:4318
OPENCLAW_MANAGER_NO_AUTOSTART=0
OPENCLAW_MANAGER_ALLOW_REMOTE_SIDECAR=0
PORT=4318
```

Defaults:

- state root: `~/.openclaw/skills/manager/`
- bind host: `127.0.0.1`
- port: `4318`
- autostart: disabled until you explicitly allow it once

## Local commands

- `/tasks`
- `/threads`
- `/resume <session>`
- `/share <session>`
- `/bind <channel>`
- `/focus`
- `/graph`
- `/digest`
- `/checkpoint`
- `/close`
- `/adopt`
- `/promote <shadow>`
- `/archive-thread <shadow>`

## 3-minute quickstart

Once the sidecar is running, the shortest useful flow is:

1. inspect observed work with `/threads`
2. promote the right thread with `/promote <shadow>`
3. review priorities with `/focus`
4. read the working digest with `/digest`

That lets you move from observation to managed work without turning every chat into a full session too early.

## Shadow-first behavior

Inbound messages first update a `ThreadShadow`.

A shadow is promoted into a session when any of these conditions is met:

- explicit `/adopt`
- explicit `/promote <shadow>`
- `tool_called`
- `artifact_created`
- `skill_invoked`
- `blocked`
- `waiting_human`
- at least two effective turns plus a promotion score of three or higher

Promotion scoring is conservative by default:

- `task_intent` adds `+2`
- `context_payload` adds `+1`
- manual priority markers add `+2`
- connector follow-up adds `+1`
- low-value chatter adds `+0`

This means:

- three greetings still stay shadowed
- a task request plus useful context promotes
- a task request plus a short acknowledgement reply stays shadowed
- connector follow-up alone becomes a candidate shadow, not a promoted session

Otherwise the manager still tracks the thread locally and exposes it through `/threads`, `/tasks`, and `/focus`.

## Sidecar API

Default local address:

```text
http://127.0.0.1:4318
```

The sidecar is loopback-only by default and is not exposed to LAN or the public internet unless you explicitly reconfigure the bind host.

- `GET /health`
- `GET /sessions`
- `GET /sessions/map`
- `GET /sessions/digest`
- `GET /sessions/:id`
- `POST /sessions/adopt`
- `POST /sessions/:id/resume`
- `POST /sessions/:id/checkpoint`
- `POST /sessions/:id/close`
- `GET /threads`
- `GET /threads/:id`
- `POST /threads/:id/promote`
- `POST /threads/:id/archive`
- `GET /attention`
- `GET /attention/focus`
- `GET /attention/risk`
- `GET /attention/drift`
- `POST /inbound-message`
- `GET /connectors`
- `POST /connectors/:name/config`
- `POST /connectors/:name/ingest`
- `POST /connectors/:name/poll`
- `POST /share/:sessionId`
- `GET /graph`
- `GET /exports/capability-facts`
- `GET /exports/capability-facts/anonymized`

## Connector model

Each external source is normalized before it reaches the control plane.

Currently implemented source adapters:

- Telegram
- WeCom
- Email
- GitHub

Connector configs are stored locally in `connectors/configs.json`. Real secrets stay in local environment variables or private config files, not in git.

Important boundary:

- bootstrap networking: loopback-only health checks
- connector networking: only happens after you explicitly configure the relevant connector

## Capability facts and exports

Closed work produces:

- closure metrics
- skill traces
- scenario signatures
- capability facts
- capability graph summaries
- anonymized fact export payloads

Markdown and HTML exports are generated locally and remain redacted by default.

## Troubleshooting

### `node` or `npm` not found

Install Node.js 20+ and make sure both `node` and `npm` are available in your shell.

### Port `4318` already in use

Set a different `PORT` value in `.env.local`, then start the sidecar again.

### Wrong or missing state root

Set `OPENCLAW_MANAGER_STATE_ROOT` in `.env.local` if you do not want the default:

```text
~/.openclaw/skills/manager/
```

### Bootstrap says `consent_required`

That means you have not yet allowed future automatic sidecar startup.

Either:

```bash
npm run dev
```

or:

```bash
npm run consent:autostart
npm run bootstrap
```

### Sidecar did not start

Run:

```bash
npm ci
npm run build
npm run dev
```

Then check:

```text
http://127.0.0.1:4318/health
```

### Skill installed but not visible

Confirm that `$CODEX_HOME/skills/openclaw-manager` exists and contains `SKILL.md`, `skill.yaml`, and the `src/` tree.

## Documentation

- architecture: [docs/architecture.md](docs/architecture.md)
- session model: [docs/session-model.md](docs/session-model.md)
- event schema: [docs/event-schema.md](docs/event-schema.md)
- connector protocol: [docs/connector-protocol.md](docs/connector-protocol.md)
- capability facts: [docs/capability-facts.md](docs/capability-facts.md)
- audit response: [docs/security-audit-response.md](docs/security-audit-response.md)

## Verify before publishing changes

```bash
npm run check
npm run build
node scripts/smoke-test.cjs
node scripts/security-smoke.cjs
```

## License

MIT
