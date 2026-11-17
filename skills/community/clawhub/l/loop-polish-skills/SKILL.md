---
name: "loop-polish"
description: "Fully automated iterative polishing: start project → full-stack integration verification → browser automation → scoring → auto-fix → loop until perfect → generate report. Invoke ONLY when user explicitly asks for loop polish, full verification with auto-fix loop, or automated acceptance with code changes. NOT for routine QA or quick reviews."
---

# Loop Polish

Start project → Full verification → Scoring → Auto-fix → Loop until perfect → Generate report. **Not perfect, don't ship.**

---

## 1. Core Flow

```
Step 1 Start → Step 2 Verify → Step 3 Score → Step 4 Fix → Step 5 Regression → Step 6 Report
                ↑                                                     │
                └──────────── loop if not perfect ─────────────────────┘

Preflight mode: Step 1 → Step 2 → Step 3 → Output issues → Stop (no fix, no loop)
```

> **When to use**: Explicitly requested loop polish, full integration verification with auto-fix, automated delivery acceptance.
> **When NOT to use**: Routine QA checks, simple bug reports, production environment validation, or when user only asked for a quick review.

---

## 2. Configuration `.loop-polish.json` (optional, defaults used if missing)

```json
{
  "mode": "full",
  "max_rounds": 10,
  "target_score": 100,
  "scope": "all",
  "auto_fix": { "enabled": true, "strategy": "conservative", "max_per_round": 3 },
  "browser": { "headless": true },
  "db_verify": true,
  "report": { "format": "markdown", "output_dir": "./polish-reports/" },
  "timeout_minutes": 120
}
```

| Config | Default | Description |
|--------|---------|-------------|
| `mode` | `full` | `full` / `preflight` (scan and score only, no fix) |
| `max_rounds` | `10` | Maximum number of iteration rounds |
| `target_score` | `100` | Target score. Stop when reached |
| `scope` | `all` | `all` / `frontend` / `backend` / `api` |
| `auto_fix.strategy` | `conservative` | `conservative` (compile/logic errors only) / `moderate` (+ data consistency) / `aggressive` (+ UX/performance) |
| `auto_fix.max_per_round` | `3` | Maximum fixes per round |
| `browser.headless` | `true` | Headless browser mode |
| `db_verify` | `true` | Verify database state after write operations. Set to `false` to skip credential access. |
| `report.format` | `markdown` | `markdown` / `html` |
| `report.output_dir` | `./polish-reports/` | Report output directory |
| `timeout_minutes` | `120` | Total timeout in minutes |

---

## 3. Execution Steps

### Step 1: Start Project

```
0. Detect project structure:
   - Backend: search pom.xml/build.gradle/package.json/go.mod/requirements.txt
   - Frontend: search package.json + vite.config/vue.config/next.config
   - Pure frontend/backend: skip what doesn't exist, only start what's present

1. Git safety (full mode only):
   - Check workspace: git status --porcelain, stash uncommitted changes if any
   - Create fix branch: git checkout -b loop-polish/round-{timestamp}
   - Record original branch name for step 6 checkout

2. Clean up old processes (cross-platform):
   - Check ports: backend 8080/3000/5000, frontend 5173/3000
   - First, check if the process on the port belongs to this project (match project path in process command line)
   - Only kill if confirmed as project-owned. If port is occupied by an unrelated process, output warning and ask user before killing.
   - Windows: netstat -ano | findstr :port → check process path → taskkill /PID {pid} /F only if project-owned
   - Linux/Mac: lsof -ti :port → check process path → kill -9 only if project-owned

3. Start backend (if project has backend, by type):
   Java:   mvn clean package -DskipTests -q ; java -jar target/*.jar
   Node:   npm install ; node server.js
   Python: pip install -r requirements.txt ; python app.py
   Go:     go build ; ./app
   After startup, poll /health or /actuator/health or GET root path, up to 60s
   If none reachable, poll process port (netstat/lsof to confirm port is listening)

4. Start frontend (if project has frontend):
   npm install (if no node_modules) ; npm run dev
   Poll dev server up to 60s

5. Failure handling:
   → Capture error logs, attempt repair (missing deps/port conflicts), retry 2x → abort if still failing
```

---

### Step 2: Full Verification

```
Scope control (by scope config):
  scope=all:      run 2.1 + 2.2 + 2.3
  scope=backend:  run 2.1 + 2.3
  scope=frontend: run 2.2
  scope=api:      run 2.1
  Pure frontend (no backend code): auto skip 2.1 and 2.3
  Pure backend (no frontend code): auto skip 2.2
```

#### 2.1 Backend API Verification

```
1. Scan API endpoints:
   Java:   Grep @RestController to locate Controller files → Grep @(Get|Post|Put|Delete)Mapping within them
   Node:   Grep router\.(get|post|put|delete)|app\.(get|post|put|delete)
   Python: Grep @(app|router)\.(route|get|post|put|delete)
   Extract: HTTP method, path, parameter names and types

2. Parse request body params (POST/PUT):
   @RequestBody or body param points to DTO class → Read the DTO source → extract field names and types
   No DTO → extract from @RequestParam / @PathVariable in method signature

3. Path parameter handling (GET /users/{id} etc.):
   If mode=preflight: use GET list endpoint to obtain existing IDs, skip all POST/PUT/DELETE entirely.
   If mode=full: Call the module's POST to create a record → get the returned id → use for GET/PUT/DELETE path params
   If POST unavailable, try GET list endpoint → take first item's id
   If POST request body depends on other resources (e.g. creating order needs user ID), try creating dependency first, skip endpoint on failure

4. Auth handling:
   Scan endpoints with login/auth/signin keywords → auto call to get Token
   Subsequent requests auto carry Authorization: Bearer {token}
   Skip auth if no login endpoint found

5. Verify each endpoint (max 2 retries per endpoint):
   If mode=preflight: only test GET endpoints, skip POST/PUT/DELETE.
   Normal: valid params, verify 200/201 + response is valid JSON + key fields not empty
   Boundary: empty string, 0, negative, very long string
   Missing required: remove required field, verify 400
   Permission: no Token → 401, regular user Token on admin endpoint → 403

6. On failure, collect diagnostics:
   - Last 50 lines of backend log (tail -50 or Get-Content -Tail 50)
   - Response body + request params + request headers
   - Before saving to report or state file, REDACT sensitive fields:
     Authorization header → [REDACTED]
     Cookie header → [REDACTED]
     password/token/secret in request/response body → [REDACTED]
     Keep only error type, status code, and redacted summary for diagnostics.
```

#### 2.2 Frontend Browser Verification

```
1. Scan frontend routes:
   Vue:  Grep "path:" to locate route file → extract all path values
   React: Grep "path:" or path: to locate route definitions → extract all paths
   Generate route list

2. Scan forms (from source, avoid blind operation):
   Grep "<el-form|<a-form|<t-form|<v-form|<form|<Form" to locate form components in each page
   Record which page each form is on, as interaction targets for browser verification

3. Invoke Skill: playwright-master, verify page by page per route list:
   - Page load: no white screen, no console.error
   - Form interaction (only forms scanned in step 2): fill → validate → submit
   - List operations (if present): pagination, search, delete
   - Modal/drawer (if present): open → operate → close
   - Navigation: menu click, tab switch
   - Skip form verification if page has no forms

4. On failure: screenshot + collect console.error + failed network request logs
```

#### 2.3 Database State Verification

```
For every write operation (POST/PUT/DELETE):

0. Safety notice: Before accessing database credentials, output "This step will read database credentials from config files. Continue?" Do NOT write database passwords or connection strings to reports, logs, or state files.
   If db_verify=false or mode=preflight: skip this entire step 2.3.

1. Get database connection info (search by priority):
   - application.yml / application.properties: spring.datasource.url
   - .env: DATABASE_URL, DB_HOST+DB_PORT+DB_NAME+DB_USER+DB_PASSWORD
   - config.json / config.js: search db, database, mysql, postgres keywords
   If none found, skip database verification and output notice

2. Detect database type (from connection string or driver):
   MySQL: jdbc:mysql:// or mysql://
   PostgreSQL: jdbc:postgresql:// or postgresql://
   SQLite: jdbc:sqlite: or sqlite:
   Choose corresponding CLI: mysql -e / psql -c / sqlite3

3. Verify data:
   POST create → direct query, confirm record written with correct field values
   PUT update → direct query, confirm fields updated
   DELETE → direct query, confirm record deleted or soft-delete flag set correctly
```

---

### Step 3: Scoring

```
Statistics rules:
  - Total feature points = number of API endpoints + number of frontend pages
  - Each API endpoint covers 2 dimensions: functional completeness (can it be called normally), error handling (are boundaries/permissions correctly rejected)
  - Each frontend page covers 2 dimensions: UX (can it be operated normally), data correctness (displayed data matches backend)
  - Performance: API response > 2s or page load > 3s deducts points

Scoring formula:
  dimension_score = 100 × (passed_in_dimension / total_in_dimension)
  final_score = completeness×0.40 + correctness×0.25 + UX×0.15 + error_handling×0.10 + performance×0.10

Deduction: single point failure deducts 100/total points, retry still fails deducts extra 5 points (max 15)
```

**Output format**:
```
📊 Round 1: 76.8/100 [Not passed]
   Completeness:80%  Correctness:72%  UX:80%  Error:60%  Performance:90% | Passed:85/120  Failed:35
```

---

### Step 4: Auto-fix

```
If auto_fix.enabled=false or mode=preflight: skip this step, go directly to step 6 to generate report

1. Fix priority (P1→P3):
   P1 Compile/syntax errors: missing import, type mismatch, null pointer
   P2 Logic/data errors: wrong query logic, wrong condition, frontend-backend mismatch
   P3 UX/performance: missing loading state, unfriendly messages (aggressive strategy only)

2. Strategy scope:
   conservative: P1~P2 | single file | ≤ 3 per round
   moderate:     P1~P2 | ≤ 2 files | ≤ 5 per round
   aggressive:   P1~P3 | cross-module | ≤ 10 per round

3. Fix flow:
   a. Read failed case diagnostic logs + screenshots → locate root cause → read source
   b. Generate fix plan (prefer minimal change)
   c. AskUserQuestion before high-risk changes (Schema change, auth logic, delete >10 lines)
   d. Save original code snippet before fix (for precise rollback on failure)
   e. Apply fix with Edit tool → record diff
   f. Local regression (only test this function point, not full run)
   g. Pass → mark fixed; Fail → restore original with Edit, mark "unfixable"

4. Exit strategy:
   - Same problem fails 2x → skip
   - 3 consecutive rounds with no score improvement → output "auto-fix limit reached", stop loop
   - Already conservative and 3 consecutive rounds with no improvement → stop immediately
```

**Output format**:
```
🔧 Round 1 fix (conservative):
  ✅ [P1] UserController.java:45 - missing @Valid
  ✅ [P1] order.ts:23 - path typo
  ⚠️ Skipped 2 need human confirmation | Fixed:2  Remaining:31
```

---

### Step 5: Regression Verification

```
1. Retest only failed cases from previous round
2. git diff --name-only to detect changed files → only retest affected modules
3. Skip passed and unchanged modules
4. Run steps 2~3 → compare current round vs previous round score
```

**Output format**:
```
🔄 Round 2 regression: Retested 35 → Passed 31 Failed 4 | Score: 92.50 (+15.70 ↑)
```

---

### Step 6: Termination & Report & Cleanup

```
Termination conditions (any one met):
  1. score >= target_score  → ✅ Passed
  2. rounds >= max_rounds   → ⏰ Max rounds reached
  3. 3 consecutive rounds score change < 1 → 📉 Score stagnated
  4. total time > timeout   → ⏱️ Timeout
  5. User interrupt

Report generation (output to report.output_dir):
  Do NOT include raw request/response bodies, auth tokens, or database credentials in reports.
  # Loop Polish Report
  ## Summary
  Final Score | Rounds | Total Time | Passed | Fixed | Remaining

  ## Score Trend
  | Round | Comp | Corr | UX | Err | Perf | Score | Change |

  ## Fix Details
  Per-round fix list + diff + outcome

  ## Remaining Issues + Recommendations
  Unfixed items + reasons + suggestions (add unit tests, add validation, add logging, etc.)

Cleanup:
  - Stop frontend and backend services (kill launched processes)
  - git checkout original branch
  - git stash pop (if stashed in step 1)
  - Output report path
```

---

## 4. Interrupt Recovery

Auto-save `.loop-polish-state.json` on interrupt:

```json
{
  "round": 2, "step": "verify",
  "passed": ["api:GET:/users", "ui:login"], "failed": ["api:PUT:/orders"],
  "fixed": ["UserController.java:45"], "unfixable": [],
  "scores": [{"round":1,"score":76.8,"fixes":2}]
}
```

On resume: read state file → skip completed steps → continue from breakpoint. Delete this file to reset.

---

## 5. Usage Examples

```
Run loop polish                                    # Full polish
Loop polish preflight: API only                    # Quick scan
Loop polish: 5 rounds, 95 score, aggressive, HTML report  # Custom
Run loop polish on user module and order module, target 100  # Specific modules
```

---

## 6. Prerequisites

- Project is buildable and runnable
- `npx playwright install chromium` (auto-install on first run if missing)
- Database is connectable with initial data

---

## 7. Notes

- All fixes happen on isolated Git branches during the loop. After cleanup, review git status — stash pop may restore pre-existing uncommitted changes.
- Recommended `strategy=conservative` for first use, increase when comfortable
- Preflight mode is read-only (no data mutation), suitable for CI usage
- This skill terminates processes on target ports, reads database credentials, and modifies source code. Use in dev/staging environments only.
- Reports saved to `polish-reports/` directory
- Auto checkout original branch and cleanup temp files when done