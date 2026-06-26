# ObjectRemover Video Object Ops Reference

## What Users Get

- Remove unwanted objects from videos (watermarks, distractions, random passersby).
- Extract subjects with transparent background for reuse in CapCut, Premiere Pro, or DaVinci Resolve.
- Select targets with natural language (for example: "remove the yellow toy"), then get a downloadable result.
- Run both human-in-the-loop flow (upload -> select -> process) and OpenClaw/API-Key automation.

## Best Fit Scenarios

- Quick cleanup for short-form videos (TikTok/Reels/YouTube Shorts).
- Creator/editor workflow that needs fast cutout or clean plate output.
- Automated backend jobs that must run end-to-end via API and polling.

## End-to-End Outcome (Simple View)

1. Provide a video (upload file, URL download, or existing asset).
2. Tell AI what to remove or extract (`textPrompt` + `action`).
3. Start processing and poll progress.
4. Download/use the processed output URL.

---

## Endpoint Contract (browser / guest)

### 1) Guest session

- `POST /api/auth/guest-session`
- Purpose: issue signed session for unregistered users.
- Success: `{ "guestSessionId": "..." }`

### 2) Cost estimate

- `POST /api/processing/calculate-cost`
- Scope (API Key): `credits:read`
- Purpose: estimate required credits before start-task.

### 3) Generate mask

- `POST /api/processing/generate-mask`
- Guest header: `x-guest-session-id: <id>`
- Body includes `textPrompt` (what to segment; can be a weak default like `object`), `videoUrl`, `isSingleFrame`, etc.

### 4) Start task

- `POST /api/processing/start-task`
- Guest header: `x-guest-session-id: <id>`
- Body `action`: `remove` | `extract`

### 5) Poll status

- `GET /api/processing/task/:taskId`
- Guest header: `x-guest-session-id: <id>`
- Scope (API Key): `processing:read`
- Terminal states:
  - **extract**: often `completed` / `failed` from DB-backed status in API response.
  - **remove** (Replicate path): poll may surface Replicate-style `succeeded` / `failed` before normalization; treat **`completed`** or **`succeeded`** as success when integrating.

---

## OpenClaw / API Key (machine-to-machine)

Use this for no-UI automation with the same endpoint flow.

### Host rule

- Call the backend API domain: `https://apiobjectremover.tokenlens.ai`.
- Authentication mode depends on host policy (session, guest, or bearer-style auth).

### Assets

- `POST /api/assets/upload` — multipart `media`; optional headers `x-original-name`, `x-media-width`, `x-media-height`, `x-media-duration`.
- `GET /api/assets` — list assets for current identity.
- `GET /api/assets/:id` — metadata and playback URLs (`fullUrl`, `mediaUrlRemote`).

### Processing

Same endpoints as browser flow:

1. `POST /api/processing/calculate-cost`
2. `POST /api/processing/generate-mask`
3. `POST /api/processing/start-task`
4. `GET /api/processing/task/:taskId`

### Bundle scope note

- This skill bundle documents endpoint behavior only.
- It does not require local repository scripts or package-manager commands.

---

## Workers vs Ubuntu (single-skill troubleshooting)

ObjectRemover splits work between **Cloudflare Workers** (edge) and **Ubuntu backend** (heavy API). Users only need **this skill**; when something fails, check **where the request runs** and **which URL the client calls**.

### Who does what

| Location | Role |
|----------|------|
| **Workers** | SSR, static assets, lightweight APIs, **forwarding** heavy routes to backend API. |
| **Ubuntu backend** | Heavy APIs, DB, full auth, Replicate/FFmpeg, uploads, processing, task persistence. |

### Ground rules

1. **Heavy work** (files, FFmpeg, Replicate, long tasks, most `/api/processing/*`, asset upload/raw/trim): execute on **Ubuntu**; on Workers these routes should **forward** to backend API, not emulate DB/fs.
2. Workers must not depend on Node `pg` + local filesystem for heavy behavior.
3. Authentication checks happen on backend paths; automation clients should target backend API domain directly.

### Env highlights

- **Workers:** should forward heavy processing routes to backend domain.
- **Backend:** executes DB/auth/processing/storage operations.

### Production URL contract

- Frontend example: `https://objectremover.video`
- Heavy backend: `https://apiobjectremover.tokenlens.ai`
- Workers forward heavy APIs to backend; Ubuntu runs heavy routes locally when request arrives there.

### Routes often forwarded from Workers -> backend

- `POST /api/processing/generate-mask`
- `POST /api/processing/start-task`
- `GET /api/processing/task/:taskId`
- `POST /api/assets/upload`
- `POST /api/assets/download-url`

### Diagnostic heuristics

- **Works locally (backend) but fails via production URL** -> confirm forwarding and backend target domain.
- **401 / auth mismatch across domains** -> absolute API URL and host-side auth policy alignment.
- **Empty or fallback data from credits/tasks on Workers** -> may be DB-unavailable fallback; heavy writes should hit Ubuntu path.
- **Browser works but automation fails** -> verify automation is targeting backend API domain and using host-expected auth mode.

---

## User-State Handling

### Unregistered user

1. Call guest-session endpoint.
2. Attach `x-guest-session-id` to processing calls.
3. Apply rate-limit/quota behavior if backend returns related errors.

### Registered user with insufficient credits

1. Read cost estimate.
2. If insufficient, try low-trial path when allowed.
3. If trial unavailable, start checkout flow, then retry start-task.

### API Key clients

1. Ensure backend base URL and host-expected auth mode.
2. Create or reuse `assetId` via upload or API.
3. Set `action` and `textPrompt` explicitly.

---

## Runtime Rules

- Workers should forward heavy processing routes.
- Ubuntu backend executes Replicate/FFmpeg/task persistence.
- Production forwarding target should resolve to backend domain.

## Troubleshooting

- `401 Unauthorized`
  - Browser: missing/expired session, or missing guest header on processing.
  - Automation: wrong target host, missing/invalid auth, or backend policy mismatch.
- `400 credits insufficient`
  - downgrade to low trial or purchase credits.
- `403` on start-task / assets
  - asset not owned by authenticated user (wrong `assetId` or wrong key user).
- Polling stuck
  - inspect backend task updates and processor health.
- No output URL
  - inspect task terminal status and storage registration.
- **Prod vs local mismatch**
  - Re-read **Workers vs Ubuntu**: forwarding and whether the client targets the backend API hostname.

## Decision Checklist (Install or Not)

- Install this skill if you need at least one of:
  - AI object removal from videos.
  - AI object extraction with transparent-background output.
  - Natural-language object targeting.
  - OpenClaw automation from upload to final result.
- Skip this skill if your task is only generic video trim/compress without object-level AI editing.
