# Changelog

## [2.0.2] - 2026-08-03

### Security and reliability

- Removed host-specific private-network endpoints from the public model registry and eliminated the DGX private-IP fallback.
- Made configuration redaction normalize common secret-key formats and fully replace sensitive values.
- Transfer the single legacy Copilot Redis subscription to another active meeting when its owner disconnects.
- Added regression coverage for public bundle safety, secret redaction, and Copilot legacy-owner transfer.

## [2.0.1] - 2026-08-03

### Security and compatibility

- Removed all query-string token handoffs; authentication now uses the login form, cookie, or Bearer header only.
- Require `OPENCLAW_AUTH_TOKEN` for every startup, including loopback-only use.
- Removed `keys.env`, absolute runtime paths, Spark SSH hosts, and backend base URLs from API responses.
- Added explicit participant-consent and cloud-audio confirmation before Copilot microphone streaming.
- Escaped remaining frontend error messages and added explicit Local API Hub alias routing.

## [2.0.0] - 2026-08-03

### OpenClaw 2026.7 design alignment

- Replaced the floating purple tab strip with an OpenClaw-style application shell: left navigation, sticky topbar, flat neutral cards, red primary accent, thin borders, and responsive bottom navigation.
- Added dark/light theme support, visible focus states, reduced-motion handling, and improved desktop/tablet/mobile breakpoints.
- Restyled the new Usage, Spark Monitor, Local API Hub, and Copilot surfaces without changing their existing route or `data-tab` contracts.

### Dashboard integration

- Preserved the modular backend/frontend architecture and integrated source analytics, Spark task history, PR Hunter output, and realtime Copilot into the shared navigation and visual system.
- Changed frontend API calls to same-origin so any `DASHBOARD_PORT`, reverse proxy, or Tailscale origin works.
- Added capability-aware Copilot setup states instead of exposing a Start action that fails silently.

### Security and release readiness

- Added authenticated Copilot WebSocket upgrades and fail-closed disabled/unconfigured behavior.
- Removed automatic secret-file scanning from Copilot; credentials are read only from the process environment.
- Refuse non-loopback binds when `OPENCLAW_AUTH_TOKEN` is missing.
- Limited URL-token authentication to an immediate server-side initial handoff; API routes require cookie or Bearer auth.
- Made cookie parsing resilient to malformed percent escapes and tokens containing `=`.
- Parse requests against a fixed internal URL base so an invalid or hostile `Host` header cannot terminate the server.
- Scoped Copilot Redis events by meeting ID while retaining single-meeting legacy worker compatibility.
- Removed task/file mutation code, restart/doctor routes, and the legacy backend proxy from the shipped server.
- Repaired the launcher to use `backend/server.js` and Node env-file parsing without hardcoded credentials or machine paths.
- Track the launcher and test harness in Git and in the explicit release manifest.
- Replaced the obsolete dashboard smoke script with startup, malformed-input, auth, read-only-boundary, design-contract, release-file, and public-safety tests.
- Upgraded `ws` to `8.21.1` to resolve the published memory-disclosure and fragmented-message memory-exhaustion advisories.
- Added a deterministic `?preview=1` mode for public screenshots so published images never expose local hostnames, sessions, or workspace details.
- Added verified desktop light, desktop dark, and mobile dark screenshots for the GitHub and ClawHub pages.
- Added a ClawHub-specific ignore manifest and `env.example.txt` compatibility mirror so the registry package excludes the old monolith while retaining a usable environment template.

## [1.7.6] - 2026-03-04

### 🐛 Bug Fixes — Model Registry & Matching

- **Case-insensitive model matching**: All model ID → registry lookups now normalize to lowercase + unify dots/hyphens to `-` before comparison. Fixes:
  - `claude-opus-4-6` now correctly matches key `opus-4.6` (dot vs hyphen mismatch was causing MISS)
  - `Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf` (DGX Spark, uppercase) now correctly matches `Qwen3.5-35B`
  - Same normalization applied to both `estimateCost` (backend) and `shortModel`/`getModelColor` (frontend)

- **New model IDs added to registry** (`models-registry.json`):
  - `gemini-3-pro` → Gemini 3 Pro (was showing $0 and no label)
  - `gpt-5.2` → GPT-5.2
  - `gpt-5.2-codex` → GPT-5.2 Codex  
  - `qwen3.5:35b` → Qwen3.5 35B 💻 (MacBook Pro Ollama)
  - `Qwen3.5-35B` → Qwen3.5 35B ⚡ (DGX Spark, distinguished by emoji)
  - Removed stale `qwen-35b-local` key that never matched any real model ID

- **Gemini Flash pricing corrected**: `costIO` was `[0.5, 3]`; corrected to actual rate `[0.075, 0.30]`


## [1.7.5] - 2026-03-04

### 🐛 Bug Fixes — Cost Calculation Overhaul

**Root cause 1: Orphan file scanning (alltime $184 bug)**
- `handleOpsAlltime` used `filter(f => f.includes('.jsonl'))` which matched `.jsonl.deleted.*` and `.jsonl.reset.*` backup files — historical session data counted multiple times
- Fixed: changed to `endsWith('.jsonl')` — only live session files scanned

**Root cause 2: Cron double-counting**
- Cron subagent sessions were counted in *both* session `.jsonl` files AND `cron/runs/*.jsonl` summaries
- Fixed: alltime now does one clean pass per source — session files for interactive sessions, cron/runs for completed cron sessions. No overlap.

**Root cause 3: `total_tokens` is unreliable in cron run records**
- In `cron/runs` finished records, `total_tokens` = cumulative context window size (grows with each turn), not actual tokens consumed per run. For Gemini Flash this could be 10–115× the real value.
- Fixed: cron run cost now uses `input_tokens + output_tokens` exclusively

**Root cause 4: Scan window too small for header stats**
- `scanSessionUsageToday` read only the last 500KB of each session file — high-volume sessions (Watchdog, jobs-intel) lost early-day messages
- Fixed: window increased to 25MB

**Root cause 5: Cache token pricing (10× overestimate)**
- `estimateCost` applied full input rate to `cacheRead`/`cacheWrite` tokens
- Fixed: per-model `cacheCosts` added to `models-registry.json`; correct rates applied (e.g. Sonnet cacheRead $0.30/1M vs $3.00/1M input)

### 🐛 Additional Fix — Opus Historical Data
- Opus (and other models from interactive sessions) was severely undercounted — `.reset` and `.deleted` session files that belonged to cron subagents were excluded (correct), but non-cron interactive sessions that were reset/deleted were also being excluded (wrong)
- Fixed: build a set of cron session UUIDs from `cron/runs/*.jsonl`; `.reset`/`.deleted` files are included if their UUID is NOT a known cron session
- Result: 85 additional archived interactive session files now correctly included in historical scan

### 📊 Verified Accuracy
- Mar 3 bar chart: **$75.97** (was $183.82 before fix)
- Finance/Cron tab: **$71.07**
- Delta ~7% — expected, two endpoints use slightly different session registries

## [1.7.4] - 2026-03-03

### 🐛 Bug Fixes
- **Critical: JS SyntaxError that broke entire dashboard** — `renderAgentMonitor()` used `await` without being declared `async`; entire inline script silently failed to execute, causing "Connecting…" state with no data loaded
- **Critical: Duplicate `let` declarations** — `globalDefaultModel`, `MODEL_OPTIONS`, `refreshModelOptions`, `getDefaultModelLabel` were all declared twice (copy-paste artifact), causing `Identifier already declared` SyntaxError
- **`/ops/channels` returned HTTP 500** — `handleOpsChannels` referenced `parsed` from outer scope but the parameter was never passed; fixed function signature

### ✨ Features & Improvements

**Model Mix (top header card):**
- Local/Ollama models (e.g. `qwen3.5:35b-a3b`) now appear in Model Mix — previously invisible because they run as cron subagents, not channel sessions
- `cronModelMix` is now computed per-run (accurate model×token counts from `cron/runs/*.jsonl`) instead of per-job-label — eliminates model misattribution when a cron job uses mixed models
- Cloud models (Gemini, Sonnet) remain authoritative from sessions; cron-only models are merged without double-counting
- Model names and colors now correctly resolve for Anthropic models: `claude-sonnet-4-6` (hyphen) now matches pattern `sonnet-4.6` (dot) via normalized matching
- Model labels updated: "Claude Sonnet 4" → **"Claude Sonnet 4.6"**, "Claude Opus 4" → **"Claude Opus 4.6"**

**Sessions Panel:**
- **Dedup by channelId**: same Discord channel appearing under multiple session keys (e.g. `discord:channel:ID` vs `discord:direct:channel:ID` after key format change) is now merged into one row, with stats combined
- **"Hide Stale" toggle button** added to sessions panel — one click hides all stale (inactive) sessions, showing only active + idle channels; click again to show all

**Cron Job Model Labels:**
- Job model label now reflects the **most recent run's model** (JSONL appends newest last); previously stuck on first-ever run's model, causing jobs that migrated models to show stale labels

### 🔧 Technical
- Sessions cache keyed by query string (`?hideStale=1`, `?staleDays=N`) — filter variants no longer return stale cached results
- `cronModelMixByDay` accumulated inline during run-record iteration for O(1) per-run cost

## [1.7.3] - 2026-03-03
### Added
- Simplified installation instructions (Ask OpenClaw / CLI) to SKILL.md and README.md.

## [1.7.2] - 2026-03-03

### ✨ Features
- **Dynamic Model Registry**: Completely removed hardcoded models, display names, and costs from the Dashboard frontend (`agent-dashboard.html`) and backend (`api-server.js`).
- **Dynamic Pricing via `models-registry.json`**: Cost estimation logic (I/O) is now decoupled and driven entirely by `models-registry.json`. Updating prices (e.g., from Google/Anthropic pricing pages) or adding new models requires zero JS code changes.
- **Smart Color Theming**: Dashboard charts now automatically assign distinct colors to models based on their provider family (Google: Blues, Anthropic: Pinks/Reds, OpenAI: Greens, Local: Teals) using an intelligent palette hash algorithm, ensuring models never collide.


## [1.7.0] - 2026-03-01

### 🔒 Security (VirusTotal Review Round 2)
- **Removed hardcoded gateway restart token** from agent-dashboard.html; restart now proxied through authenticated `/ops/restart` API endpoint
- **Token no longer sent via URL query params** in API calls; switched to `Authorization: Bearer` header for all apiFetch requests
- **Token stripped from URL** immediately on page load via `history.replaceState` to prevent leakage in Referer/logs/history
- **Removed localStorage token storage** from server-monitor.html (was still present despite v1.6.0 claim)
- **Added DOMPurify** for all marked.js markdown rendering to prevent XSS via untrusted task content
- **Added `/ops/restart` server-side endpoint** that proxies to gateway hooks with env-sourced HOOK_TOKEN
- **Updated SECURITY.md** to accurately reflect auth flow, XSS mitigations, and restart architecture

## [2.1.0] - 2026-02-22

### 🎯 Dashboard UX and Information Architecture
- Added per-channel default model settings for sessions
- Added model selector dropdowns for both Sessions and Cron jobs
- Introduced task-model fit dashboard and redesigned Cron Runs view
- Added always-visible system info bar above active sessions
- Renamed product branding
- Added mobile display of `匹配` column and improved model/token visibility on smaller screens

### 💸 Cost Analytics Enhancements
- Added cron cost analysis with fixed vs variable cost trend view
- Updated card and breakdown calculations to use provider `cost.total`
- Included `cacheRead` and `cacheWrite` tokens in cost estimation
- Corrected header card totals by sourcing daily aggregates from `/ops/sessions`
- Improved model breakdown and token count consistency across panels

### ⏰ Cron and Operations Improvements
- Fixed Cron Runs panel field mapping (`name`, `last.startedAt`, `last.endedAt`)
- Improved cron/subagent naming with more user-friendly labels
- Removed duplicate cron entries and improved sorting/audit consistency

### 📱 Mobile and PWA
- Added `apple-touch-icon` PNG asset (180x180) for iOS home screen
- Added PWA icon + manifest support for Add to Home Screen flow
- Added iPhone 17 Pro targeted layout and spacing optimizations
- Added Chinese Discord channel naming support in UI lists

### 🔒 Security and Reliability Fixes
- Improved OpenClaw version detection (`2>&1` handling + `package.json` fallback)
- Ensured Discord channel names resolve fully in dashboard views
- Added API key masking improvements for `/ops/config` responses

### 🧹 Maintenance
- Removed `README-JONY.md` from repository

## [2.0.0] - 2026-02-22

### 🏗️ Architecture Overhaul
- **Session-centric design**: Replaced original 5-tab layout (Ops/Documents/APIs/Logs) with 6 operational tabs (Sessions/Cost/Cron/Quality/Audit/Config)
- **Unified pricing engine**: All cost estimates use official per-token pricing with input/output split (Claude Opus $15/$75, Gemini 3 Pro $2/$12, etc.)
- **Unified PST timezone**: Shared `getTodayPstStartIso()` helper across all endpoints
- **Auto-load keys**: Server reads `~/.openclaw/keys.env` at startup (no env vars needed in LaunchAgent)

### 📊 New: Sessions Tab (Default)
- Per-session table: model, thinking level, messages (effective/total), tokens, cost, idle rate, last active
- Real-time alerts: session errors, model waste detection, stale session warnings
- Header cards: Today Cost / Tokens / Cron Jobs / Active Sessions / Primary Model

### 💰 New: Cost Analytics
- Today's channel breakdown with model distribution bar
- All-time model breakdown with per-model cost cards
- Daily token chart (stacked by model, color-coded)
- Daily cost chart (stacked by model, dollar labels)
- Cost heatmap: model × day matrix with heat coloring
- Provider audit: OpenAI Admin API (7-day usage) + Anthropic org verification

### 📈 New: Quality Panel
- Per-session idle rate visualization (NO_REPLY + HEARTBEAT_OK percentage)
- Color-coded progress bars (green/yellow/red thresholds)
- Effective vs silent message breakdown

### 🔍 New: Config Audit Panel
- Auto-detect: Opus on high-idle channels → suggest downgrade to Sonnet
- Missing thinking level warnings
- Cost-saving recommendations with estimated savings
- Provider verification status

### ⚙️ New: Config Viewer
- Browse openclaw.json, SOUL*.md, AGENTS.md, USER.md, TOOLS.md, IDENTITY.md, HEARTBEAT.md, MEMORY.md
- API keys from keys.env with automatic masking (first 8 + last 4 chars)
- Click-to-expand accordion UI
- File size and modification time

### ⏰ Enhanced: Cron Tab
- Visual card layout replacing timeline view
- Chinese descriptions for each job (🔍 监控 OpenClaw 生态动态, 💼 AI 求职机会扫描, etc.)
- Human-readable schedules (每天 9:00, 每 2 小时, 每周五 9:00)
- Last run: time ago, duration, tokens, model
- Enable/disable status with visual indicators

### 🔐 Security
- Cookie-based auth: HttpOnly, SameSite=Strict, 30-day expiry
- Login page at `/login`, logout at `/logout`
- Key masking in config viewer (never expose full keys)

### 📱 Mobile
- PWA meta tags (apple-mobile-web-app-capable, theme-color, viewport-fit=cover)
- Safe-area padding for notched devices
- Touch targets ≥ 44px
- Responsive tab bar

### 🐛 Bug Fixes
- Fixed PST timezone calculation (was double-converting offsets)
- Fixed model distribution bar gaps (0-token models, legend inside flex container)
- Fixed cost discrepancy between endpoints (unified estimator, removed cron from channels total)
- Filtered `delivery-mirror` model from all views

### API Endpoints Added
- `GET /ops/sessions` — per-session overview with today's usage + alerts
- `GET /ops/channels` — per-channel cost/token breakdown
- `GET /ops/alltime` — historical usage with daily model breakdown
- `GET /ops/audit` — OpenAI/Anthropic official API verification
- `GET /ops/config` — config file viewer with key masking
- `GET /ops/cron` — enhanced cron job list

---

## [1.0.0] - 2026-02-21

### Initial Fork
- Forked from [karem505/openclaw-agent-dashboard](https://github.com/karem505/openclaw-agent-dashboard)
- Added cookie-based auth (login/logout)
- Added system + workspace skills scan (56 skills)
- Added mobile PWA support
- Added Cron Timeline + Vision Ingestion panels
- Added macOS LaunchAgent plist example
- Replaced Kanban tasks with operational monitoring
