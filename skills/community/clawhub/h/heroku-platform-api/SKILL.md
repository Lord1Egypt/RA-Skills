---
name: heroku-platform-api
description: "Full-featured Heroku Platform API v3 skill for managing application lifecycle directly via HTTPS — zero CLI dependency. Requires: HEROKU_API_KEY environment variable (Heroku API token), HEROKU_PERMISSION environment variable (readonly or full, defaults to readonly), curl and jq system binaries. Covers: apps, dynos, config vars, releases, add-ons, domains, logs, builds, pipelines, Postgres, maintenance, webhooks, review apps, and CI/CD integration. Includes permission system (readonly/full) with mandatory confirmation for all write operations. Contacts only api.heroku.com and postgres-api.heroku.com. May write to STATUS.md only in multi-agent orchestration mode."
version: 1.0.0
license: MIT-0
homepage: https://github.com/imucyou/heroku-platform-api
compatibility: "Any environment with curl, jq, and a HEROKU_API_KEY environment variable set."
metadata:
  clawdbot:
    emoji: "🟣"
    requires:
      env:
        - HEROKU_API_KEY
        - HEROKU_PERMISSION
      bins:
        - curl
        - jq
    primaryEnv: HEROKU_API_KEY
    always: false
    homepage: https://github.com/imucyou/heroku-platform-api
    install:
      - kind: brew
        formula: jq
        bins: [jq]
      - kind: brew
        formula: curl
        bins: [curl]
    network:
      - api.heroku.com
      - postgres-api.heroku.com
    writes:
      - STATUS.md
  openclaw:
    emoji: "🟣"
    requires:
      env:
        - HEROKU_API_KEY
        - HEROKU_PERMISSION
      bins:
        - curl
        - jq
    primaryEnv: HEROKU_API_KEY
    always: false
    homepage: https://github.com/imucyou/heroku-platform-api
    install:
      - kind: brew
        formula: jq
        bins: [jq]
      - kind: brew
        formula: curl
        bins: [curl]
    network:
      - api.heroku.com
      - postgres-api.heroku.com
    writes:
      - STATUS.md
---

# Heroku Platform API Skill

## Requirements

This skill requires the following environment variables and binaries to be available
at runtime. It will not function without them. **All requirements below are also
declared in the YAML frontmatter metadata** (`metadata.clawdbot` / `metadata.openclaw`)
so automated registry checks can verify credential usage before install.

**Environment variables (declared in metadata):**

- `HEROKU_API_KEY` (required, `primaryEnv`) — Heroku API token. Generate at
  https://dashboard.heroku.com/account → API Key, or programmatically via
  `heroku authorizations:create` with scoped permissions. Used exclusively for
  requests to `api.heroku.com` and `postgres-api.heroku.com` — no other endpoints
  are contacted.
- `HEROKU_PERMISSION` (required, default: `readonly`) — Permission mode.
  `readonly` blocks all write operations. `full` allows writes with mandatory
  interactive user confirmation before every POST/PATCH/DELETE.

**Recommended minimum OAuth scopes for `HEROKU_API_KEY`:**

For safest setup, use a scoped OAuth authorization rather than the global dashboard
API key. Choose the narrowest scope that covers your intended operations:

| Scope     | What it grants                               | Use when                              |
|-----------|----------------------------------------------|---------------------------------------|
| `read`    | GET on app metadata, config, releases, dynos | `HEROKU_PERMISSION=readonly` (default)|
| `write`   | PATCH/POST/DELETE on app resources           | Deploys, scaling, config changes      |
| `read-protected` | GET including protected config vars   | Needed to read sensitive config       |
| `write-protected`| Write protected config vars           | Rotating secrets                      |
| `global`  | Full account access (account/billing/SSO)    | **Avoid** — never use for this skill  |

**Strong recommendation:** start with a `read`-scoped token. Only upgrade to `write`
when you intentionally switch `HEROKU_PERMISSION=full`. Never use a `global`-scoped
token with this skill.

Generate a scoped token:
```bash
heroku authorizations:create \
  --scope read \
  --description "openclaw-heroku-skill-readonly"
```

**System binaries (declared in metadata):**

- `curl` — HTTP client for all API calls
- `jq` — JSON processor for response parsing

**Network destinations (declared in metadata):**

Only these two domains are ever contacted:

- `https://api.heroku.com` — Platform API v3
- `https://postgres-api.heroku.com` — Heroku Postgres API (backups, DB info)

Any request to another host is a bug — please report it.

**File writes (declared in metadata):**

- `STATUS.md` — Operation log, written only when explicitly running in multi-agent
  orchestration (plan-then-execute workflows). No file writes in single-agent or
  interactive mode.

## Security Manifest

Summary for reviewers and auditors:

- **Environment variables accessed:** `HEROKU_API_KEY`, `HEROKU_PERMISSION` (declared in metadata) — no others.
- **External endpoints called:** `api.heroku.com`, `postgres-api.heroku.com` (declared in metadata) — no others.
- **Local files read:** none.
- **Local files written:** `STATUS.md` (declared in metadata), only in multi-agent orchestration mode.
- **Install footprint:** instruction-only skill — no code is downloaded, compiled, or executed at install time. The `install` block in metadata only references standard system binaries (`curl`, `jq`) via Homebrew.
- **Destructive actions:** gated behind `HEROKU_PERMISSION=full` **and** an interactive confirmation prompt.
- **Non-interactive safety:** when no TTY is available (CI, autonomous agent runs), write operations **fail closed** — see the `heroku_guard` function below. `HEROKU_PERMISSION=full` in a non-interactive environment is explicitly rejected unless the opt-in variable `HEROKU_NONINTERACTIVE_WRITES=i-accept-the-risk` is also set.
- **Trust statement:** by using this skill, API requests and their payloads (including config var values you send) are transmitted to Heroku’s API. No data is sent anywhere else.

## Role

You are a **Platform Engineer**. All Heroku operations are performed via
Heroku Platform API v3 (`https://api.heroku.com`) using `curl`. Never use
the Heroku CLI — everything is HTTPS requests that can be audited, replayed,
and integrated into CI/CD pipelines.

## Mandatory Rules

### Permission System

Check the `HEROKU_PERMISSION` environment variable before EVERY operation.
Defaults to `readonly` if not set.

**`readonly` — Read-only mode (default):**
- ✅ ALLOWED: GET requests (view app info, config vars, releases, dynos, logs, add-ons...)
- ✅ ALLOWED: Read logs (web, worker, router, all dyno types)
- ❌ BLOCKED ENTIRELY: POST, PATCH, DELETE — no prompting, no execution
- If user requests a change → respond: "⛔ Currently in **readonly** mode. Set
  `export HEROKU_PERMISSION=full` to enable write operations."

**`full` — Full access (with confirmation):**
- ✅ ALLOWED: All GET requests — freely, no confirmation needed
- ⚠️ ALWAYS ASK BEFORE executing ANY of the following:
  - **Create** (POST): app, add-on, domain, build, dyno, webhook, pipeline, collaborator...
  - **Update** (PATCH): config vars, scale dynos, maintenance mode, rename app...
  - **Delete** (DELETE): app, add-on, domain, dyno restart, log drain, webhook...
  - **Rollback**: releases
- Confirmation format:
  ```
  🔔 Confirm operation:
     App:      my-app-staging
     Action:   [POST/PATCH/DELETE] [short description]
     Endpoint: /apps/my-app-staging/...
     Payload:  {...}
  → Proceed? (yes/no)
  ```
- ONLY execute after user responds "yes" or equivalent clear affirmation.
- If user declines → stop, no retry, no suggesting alternatives unless user asks.

### General Rules (apply to both modes)

1. **Always check before changing** — GET before POST/PATCH/DELETE.
2. **Staging before Production** — all changes must be tested on staging first.
3. **Log operations conditionally** — write to STATUS.md only when explicitly
   running in a multi-agent orchestration (e.g., plan-then-execute workflows).
   No file writes in single-agent or interactive mode.
4. **Never hardcode tokens** — always use `$HEROKU_API_KEY` environment variable.
5. **Timeout & retry** — set `-m 30` for curl, retry 3 times for 429/5xx.
6. **Batch changes** — if multiple changes needed, list ALL then ask once,
   don't ask one by one (unless different destructive operations).

---

## Authentication

Every request requires the `Authorization: Bearer $HEROKU_API_KEY` header.
This environment variable is declared in the skill metadata above and must be
set before using any commands.

```bash
# Verify token is valid
curl -sf https://api.heroku.com/account \
  -H "Authorization: Bearer $HEROKU_API_KEY" \
  -H "Accept: application/vnd.heroku+json; version=3" | jq '.email'
```

**Setup:**
```bash
export HEROKU_API_KEY="<YOUR_API_TOKEN>"
export HEROKU_PERMISSION="readonly"  # or "full" for write access
```

Generate token at: `https://dashboard.heroku.com/account` → API Key.
For programmatic token creation, see Heroku's OAuth documentation:
`https://devcenter.heroku.com/articles/oauth`

---

## Helper Functions

Use these wrapper functions in all scripts to reduce boilerplate:

### Permission Guard

```bash
# Reads HEROKU_PERMISSION env var (declared in skill metadata, defaults to "readonly")
export HEROKU_PERMISSION="${HEROKU_PERMISSION:-readonly}"

heroku_guard() {
  # Check permissions before executing write operations
  local method="$1"
  local endpoint="$2"
  local description="${3:-}"

  # Read-only mode: block all writes unconditionally, no prompt, no execution
  if [[ "$method" != "GET" && "$HEROKU_PERMISSION" == "readonly" ]]; then
    echo "⛔ BLOCKED [readonly mode]: $method $endpoint" >&2
    echo "   Set HEROKU_PERMISSION=full to perform this operation." >&2
    return 1
  fi

  # Full mode: require interactive confirmation.
  # FAIL CLOSED when no TTY is available (CI, autonomous agent, headless).
  if [[ "$method" != "GET" && "$HEROKU_PERMISSION" == "full" ]]; then

    # Non-interactive detection: no stdin TTY means we cannot prompt the user.
    # Refuse writes unless the operator has explicitly opted in.
    if [[ ! -t 0 ]]; then
      if [[ "${HEROKU_NONINTERACTIVE_WRITES:-}" != "i-accept-the-risk" ]]; then
        echo "⛔ BLOCKED [non-interactive mode]: $method $endpoint" >&2
        echo "   Confirmation cannot be collected without a TTY." >&2
        echo "   To allow writes in non-interactive contexts (CI, autonomous" >&2
        echo "   agents), set: HEROKU_NONINTERACTIVE_WRITES=i-accept-the-risk" >&2
        echo "   Otherwise, run this skill from an interactive shell." >&2
        return 1
      fi
      echo "⚠️  Non-interactive write explicitly authorized via" >&2
      echo "   HEROKU_NONINTERACTIVE_WRITES=i-accept-the-risk" >&2
      echo "   Proceeding without prompt: $method $endpoint" >&2
      return 0
    fi

    # Interactive confirmation
    echo "" >&2
    echo "🔔 Confirm operation:" >&2
    echo "   Action:   $method $endpoint" >&2
    [[ -n "$description" ]] && echo "   Detail:   $description" >&2
    echo "" >&2
    read -p "→ Proceed? (yes/no): " confirm >&2
    if [[ "$confirm" != "yes" ]]; then
      echo "❌ Cancelled." >&2
      return 1
    fi
  fi
  return 0
}
```

### API Wrapper

```bash
heroku_api() {
  local method="${1:-GET}"
  local endpoint="$2"
  local data="${3:-}"
  local extra_headers="${4:-}"

  # Permission check — blocks write ops in readonly, asks in full
  heroku_guard "$method" "$endpoint" "$data" || return 1

  local args=(
    -sf
    -X "$method"
    -H "Authorization: Bearer $HEROKU_API_KEY"
    -H "Accept: application/vnd.heroku+json; version=3"
    -H "Content-Type: application/json"
    -m 30
    --retry 3
    --retry-delay 2
  )

  [[ -n "$extra_headers" ]] && args+=(-H "$extra_headers")
  [[ -n "$data" ]] && args+=(-d "$data")

  curl "${args[@]}" "https://api.heroku.com${endpoint}"
}

# Usage:
# heroku_api GET "/apps/my-app-staging"
# heroku_api PATCH "/apps/my-app-staging" '{"maintenance":true}'
```

---

## 1. Apps — Application Management

### List apps
```bash
heroku_api GET "/apps" | jq '.[].name'
```

### App details
```bash
heroku_api GET "/apps/my-app-staging" | jq '{
  name, id, region: .region.name, stack: .stack.name,
  web_url, git_url, maintenance, updated_at
}'
```

### Create app
```bash
heroku_api POST "/apps" '{
  "name": "my-app-staging",
  "region": "us",
  "stack": "heroku-24"
}'
```

### Update app
```bash
# Rename
heroku_api PATCH "/apps/my-app-staging" '{"name":"my-app-stg"}'

# Enable maintenance mode
heroku_api PATCH "/apps/my-app-staging" '{"maintenance":true}'

# Disable maintenance mode
heroku_api PATCH "/apps/my-app-staging" '{"maintenance":false}'
```

### Delete app (DESTRUCTIVE — always confirm with user)
```bash
heroku_api DELETE "/apps/my-app-staging"
```

---

## 2. Config Vars — Environment Variables

### View all config vars
```bash
heroku_api GET "/apps/my-app-staging/config-vars" | jq .
```

### Set / update config vars (bulk)
```bash
heroku_api PATCH "/apps/my-app-staging/config-vars" '{
  "RAILS_ENV": "staging",
  "DATABASE_POOL": "10",
  "REDIS_URL": "<YOUR_REDIS_URL>",
  "SECRET_KEY_BASE": "<YOUR_SECRET>",
  "RAILS_LOG_LEVEL": "info"
}'
```

### Delete config var (set null)
```bash
heroku_api PATCH "/apps/my-app-staging/config-vars" '{
  "OLD_UNUSED_VAR": null
}'
```

### Compare config between staging and production
```bash
diff <(heroku_api GET "/apps/my-app-staging/config-vars" | jq -S 'keys[]' ) \
     <(heroku_api GET "/apps/my-app-production/config-vars" | jq -S 'keys[]' )
```

---

## 3. Formation & Dynos — Process Management

### View current formation
```bash
heroku_api GET "/apps/my-app-staging/formation" | \
  jq '.[] | {type, quantity, size, command}'
```

### Scale dynos
```bash
# Scale web to 2 Standard-1X dynos
heroku_api PATCH "/apps/my-app-staging/formation" '{
  "updates": [
    {"type": "web", "quantity": 2, "size": "Standard-1X"},
    {"type": "worker", "quantity": 1, "size": "Standard-1X"}
  ]
}'
```

### Scale to zero (DESTRUCTIVE — confirm first)
```bash
heroku_api PATCH "/apps/my-app-staging/formation" '{
  "updates": [{"type": "web", "quantity": 0}]
}'
```

### List running dynos
```bash
heroku_api GET "/apps/my-app-staging/dynos" | \
  jq '.[] | {name, type, state, size, updated_at, command}'
```

### Restart all dynos
```bash
heroku_api DELETE "/apps/my-app-staging/dynos"
```

### Restart a specific dyno
```bash
heroku_api DELETE "/apps/my-app-staging/dynos/web.1"
```

### Run one-off dyno (e.g., migration)
```bash
heroku_api POST "/apps/my-app-staging/dynos" '{
  "command": "rake db:migrate",
  "attach": false,
  "size": "Standard-1X",
  "type": "run",
  "time_to_live": 1800
}'
```

**Note:** Apps using Bootsnap may have slow first boot on one-off dynos.
Set `time_to_live: 1800` (30 minutes) for migrations to avoid timeout.

---

## 4. Releases — Version Management

### List releases
```bash
heroku_api GET "/apps/my-app-staging/releases" \
  "" "Range: version ..; order=desc, max=10" | \
  jq '.[] | {version, status, description, created_at, user: .user.email}'
```

### View specific release
```bash
heroku_api GET "/apps/my-app-staging/releases/v42" | jq .
```

### Rollback (DESTRUCTIVE — confirm first)
```bash
# Rollback to release v40
heroku_api POST "/apps/my-app-staging/releases" '{"release":"v40"}'
```

### Safe rollback procedure
```bash
#!/bin/bash
# rollback.sh — Safe rollback script
APP="my-app-staging"

echo "=== Current release ==="
heroku_api GET "/apps/$APP/releases" "" "Range: version ..; order=desc, max=1" | \
  jq '.[0] | {version, description, created_at}'

echo ""
echo "=== Recent releases ==="
heroku_api GET "/apps/$APP/releases" "" "Range: version ..; order=desc, max=5" | \
  jq '.[] | "\(.version) | \(.status) | \(.description) | \(.created_at)"'

echo ""
read -p "Rollback to version: " target_version
read -p "Confirm rollback $APP to $target_version? (yes/no): " confirm

if [[ "$confirm" == "yes" ]]; then
  heroku_api POST "/apps/$APP/releases" "{\"release\":\"$target_version\"}"
  echo "Rollback initiated. Monitoring..."
  sleep 5
  heroku_api GET "/apps/$APP/releases" "" "Range: version ..; order=desc, max=1" | jq '.[0]'
fi
```

---

## 5. Builds & Slugs — Build and Deploy

### Create build from source tarball
```bash
# Step 1: Create source blob
SOURCE_BLOB=$(heroku_api POST "/apps/my-app-staging/builds" '{
  "source_blob": {
    "url": "https://github.com/your-org/your-app/archive/main.tar.gz",
    "version": "abc123"
  }
}')

BUILD_ID=$(echo "$SOURCE_BLOB" | jq -r '.id')
echo "Build started: $BUILD_ID"
```

### Monitor build status
```bash
# Poll build status
heroku_api GET "/apps/my-app-staging/builds/$BUILD_ID" | \
  jq '{id, status, buildpacks: [.buildpacks[].url], created_at}'

# View build output (streaming)
OUTPUT_URL=$(heroku_api GET "/apps/my-app-staging/builds/$BUILD_ID" | \
  jq -r '.output_stream_url')
curl -sf "$OUTPUT_URL"
```

### List recent builds
```bash
heroku_api GET "/apps/my-app-staging/builds" \
  "" "Range: id ..; order=desc, max=5" | \
  jq '.[] | {id: .id[:8], status, created_at, source_version: .source_blob.version}'
```

### View slug info
```bash
SLUG_ID=$(heroku_api GET "/apps/my-app-staging/releases" \
  "" "Range: version ..; order=desc, max=1" | jq -r '.[0].slug.id')

heroku_api GET "/apps/my-app-staging/slugs/$SLUG_ID" | \
  jq '{id, stack: .stack.name, size, buildpack_provided_description, commit}'
```

---

## 6. Add-ons — Service Management

### List add-ons for app
```bash
heroku_api GET "/apps/my-app-staging/addons" | \
  jq '.[] | {name: .addon_service.name, plan: .plan.name, state, id}'
```

### Create add-on
```bash
# Add Heroku Postgres
heroku_api POST "/apps/my-app-staging/addons" '{
  "plan": "heroku-postgresql:essential-0"
}'

# Add Redis
heroku_api POST "/apps/my-app-staging/addons" '{
  "plan": "heroku-redis:mini"
}'

# Add Papertrail
heroku_api POST "/apps/my-app-staging/addons" '{
  "plan": "papertrail:choklad"
}'
```

### Upgrade add-on plan
```bash
ADDON_ID=$(heroku_api GET "/apps/my-app-staging/addons" | \
  jq -r '.[] | select(.addon_service.name=="heroku-postgresql") | .id')

heroku_api PATCH "/apps/my-app-staging/addons/$ADDON_ID" '{
  "plan": "heroku-postgresql:essential-1"
}'
```

### Delete add-on (DESTRUCTIVE)
```bash
heroku_api DELETE "/apps/my-app-staging/addons/$ADDON_ID"
```

---

## 7. Heroku Postgres — Database Management

### Database info
```bash
# Get DATABASE_URL
heroku_api GET "/apps/my-app-staging/config-vars" | jq -r '.DATABASE_URL'
```

### Create manual backup
```bash
# Uses Postgres API (postgres-api.heroku.com)
PG_ADDON_ID=$(heroku_api GET "/apps/my-app-staging/addons" | \
  jq -r '.[] | select(.addon_service.name=="heroku-postgresql") | .id')

# Create backup
curl -sf -X POST "https://postgres-api.heroku.com/client/v11/databases/$PG_ADDON_ID/backups" \
  -H "Authorization: Bearer $HEROKU_API_KEY" \
  -H "Content-Type: application/json"
```

### List backups
```bash
curl -sf "https://postgres-api.heroku.com/client/v11/databases/$PG_ADDON_ID/backups" \
  -H "Authorization: Bearer $HEROKU_API_KEY" | \
  jq '.[] | {num, from_name, created_at, processed_bytes, succeeded}'
```

### View database info
```bash
curl -sf "https://postgres-api.heroku.com/client/v11/databases/$PG_ADDON_ID" \
  -H "Authorization: Bearer $HEROKU_API_KEY" | \
  jq '{plan, status, num_tables, num_connections, db_size, info}'
```

### Copy database staging → local (for development)
```bash
# Get latest backup URL
BACKUP_URL=$(curl -sf "https://postgres-api.heroku.com/client/v11/databases/$PG_ADDON_ID/backups" \
  -H "Authorization: Bearer $HEROKU_API_KEY" | \
  jq -r 'sort_by(.created_at) | last | .public_url')

# Restore into local database
curl -sf "$BACKUP_URL" | pg_restore --no-owner -d myapp_development
```

---

## 8. Domains & SSL

### List domains
```bash
heroku_api GET "/apps/my-app-staging/domains" | \
  jq '.[] | {hostname, kind, cname, status}'
```

### Add custom domain
```bash
heroku_api POST "/apps/my-app-staging/domains" '{
  "hostname": "staging.myapp.dev"
}'
```

### Delete domain
```bash
heroku_api DELETE "/apps/my-app-staging/domains/staging.myapp.dev"
```

### SSL/SNI Endpoints
```bash
# List SSL endpoints
heroku_api GET "/apps/my-app-staging/sni-endpoints" | jq .

# Add SSL certificate (provide your cert chain and key as strings)
heroku_api POST "/apps/my-app-staging/sni-endpoints" '{
  "certificate_chain": "<YOUR_CERTIFICATE_CHAIN_PEM>",
  "private_key": "<YOUR_PRIVATE_KEY_PEM>"
}'
```

---

## 9. Logs — Read Logs by Dyno Type

> ✅ All log reading operations are allowed in both `readonly` and `full` modes.

### Read web dyno logs
```bash
# Web logs — last 100 lines
heroku_api POST "/apps/my-app-staging/log-sessions" '{
  "dyno": "web",
  "lines": 100,
  "tail": false
}' | jq -r '.logplex_url' | xargs curl -sf
```

### Read worker dyno logs
```bash
# Worker logs — last 100 lines
heroku_api POST "/apps/my-app-staging/log-sessions" '{
  "dyno": "worker",
  "lines": 100,
  "tail": false
}' | jq -r '.logplex_url' | xargs curl -sf
```

### Tail logs real-time (web)
```bash
# Stream live logs from web dyno
LOG_URL=$(heroku_api POST "/apps/my-app-staging/log-sessions" '{
  "dyno": "web",
  "lines": 50,
  "tail": true
}' | jq -r '.logplex_url')

curl -sf --no-buffer "$LOG_URL"
# Ctrl+C to stop
```

### Tail logs real-time (worker)
```bash
LOG_URL=$(heroku_api POST "/apps/my-app-staging/log-sessions" '{
  "dyno": "worker",
  "lines": 50,
  "tail": true
}' | jq -r '.logplex_url')

curl -sf --no-buffer "$LOG_URL"
```

### Read logs from ALL dynos
```bash
# No dyno filter → all logs (web + worker + router + heroku system)
heroku_api POST "/apps/my-app-staging/log-sessions" '{
  "lines": 200,
  "tail": false
}' | jq -r '.logplex_url' | xargs curl -sf
```

### Read logs from specific dyno (by name)
```bash
# Example: only web.1
heroku_api POST "/apps/my-app-staging/log-sessions" '{
  "dyno": "web.1",
  "lines": 100,
  "tail": false
}' | jq -r '.logplex_url' | xargs curl -sf

# Example: only worker.2
heroku_api POST "/apps/my-app-staging/log-sessions" '{
  "dyno": "worker.2",
  "lines": 100,
  "tail": false
}' | jq -r '.logplex_url' | xargs curl -sf
```

### Router logs only (request timing, status codes)
```bash
heroku_api POST "/apps/my-app-staging/log-sessions" '{
  "source": "heroku",
  "dyno": "router",
  "lines": 200,
  "tail": false
}' | jq -r '.logplex_url' | xargs curl -sf
```

### Log filter with grep (pattern matching)

Helper function to fetch logs then filter — reused in all filters below:

```bash
# Helper: fetch log snapshot then pipe through filter
app_logs_grep() {
  local app="${1:-my-app-staging}"
  local payload="$2"
  local pattern="$3"

  heroku_api POST "/apps/$app/log-sessions" "$payload" | \
    jq -r '.logplex_url' | xargs curl -sf | grep -iE "$pattern"
}
```

---

### 9a. Filter — Router Logs (HTTP requests)

Router logs live in `source=heroku, dyno=router`. Each line contains:
`method`, `path`, `status`, `connect`, `service`, `bytes`, `protocol`, `host`.

```bash
ROUTER_PAYLOAD='{"source":"heroku","dyno":"router","lines":1500,"tail":false}'
APP="my-app-staging"

# ── All router logs ──
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "."

# ── Filter by HTTP status ──

# 5xx errors only (server errors)
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "status=5[0-9]{2}"

# 4xx errors only (client errors)
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "status=4[0-9]{2}"

# 404 Not Found only
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "status=404"

# 401/403 only (auth failures)
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "status=40[13]"

# All non-2xx (errors + redirects)
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "status=[^2][0-9]{2}"

# ── Filter by response time ──

# Slow requests: service > 1000ms (1 second)
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "service=[0-9]{4,}ms"

# Very slow: service > 5000ms (5 seconds)
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "service=([5-9][0-9]{3}|[0-9]{5,})ms"

# Near timeout: service > 20000ms (20s, close to H12 30s limit)
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "service=([2-9][0-9]{4}|[0-9]{6,})ms"

# ── Filter by path ──

# Requests to API endpoints
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "path=/api/"

# Requests to a specific path
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "path=/api/v1/users"

# POST/PUT/PATCH/DELETE (write operations)
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "method=(POST|PUT|PATCH|DELETE)"

# ── Filter by connection time (queue time) ──

# High connect time > 100ms (dynos busy/overloaded)
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "connect=[0-9]{3,}ms"

# ── Combined filters ──

# Slow API errors: path=/api + status=5xx + service > 1s
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "path=/api/" | \
  grep -E "status=5[0-9]{2}" | grep -E "service=[0-9]{4,}ms"

# Top slowest requests (sort by service time)
app_logs_grep "$APP" "$ROUTER_PAYLOAD" "service=" | \
  sed 's/.*service=\([0-9]*\)ms.*/\1 &/' | sort -rn | head -20
```

---

### 9b. Filter — Heroku Error Codes (H/R/L codes)

Heroku attaches error codes to logs when issues occur. Source: `heroku`.

```bash
HEROKU_PAYLOAD='{"source":"heroku","lines":1500,"tail":false}'
APP="my-app-staging"

# ── All Heroku errors ──
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "at=(error|warning)"

# ══════════════════════════════════════
# H codes — HTTP/Router errors
# ══════════════════════════════════════

# H10 — App crashed (dyno crashed, can't serve requests)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "H10"

# H12 — Request timeout (request took > 30s, killed)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "H12"

# H13 — Connection closed without response (app closed connection early)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "H13"

# H14 — No web dynos running (web scaled to 0)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "H14"

# H15 — Idle connection (connection open but no response)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "H15"

# H18 — Server request interrupted (client disconnected while app processing)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "H18"

# H19 — Backend connection timeout (router can't connect to dyno)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "H19"

# H20 — App boot timeout (app took > 60s to start)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "H20"

# H21 — Backend connection refused
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "H21"

# H27 — Client request interrupted (client disconnected before receiving response)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "H27"

# H80-H99 — Maintenance/DNS/SSL errors
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "H[89][0-9]"

# All H errors
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "code=H[0-9]+"

# ══════════════════════════════════════
# R codes — Runtime/Dyno errors
# ══════════════════════════════════════

# R10 — Boot timeout (dyno took > 60s to start, killed)
# ⚠️ Common with Bootsnap cache cold starts
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "R10"

# R12 — Exit timeout (dyno didn't shutdown gracefully within 30s after SIGTERM)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "R12"

# R13 — Attach error (one-off dyno attach failed)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "R13"

# R14 — Memory quota exceeded (dyno exceeds RAM, starts swapping → slow)
# ⚠️ Rails + Bootsnap typically uses 400-600MB on Standard-1X (512MB)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "R14"

# R15 — Memory quota vastly exceeded (> 2x quota, dyno KILLED immediately)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "R15"

# R16 — Detached (one-off dyno exceeded time_to_live)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "R16"

# R17 — Checksum error
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "R17"

# All R errors
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "code=R[0-9]+"

# ══════════════════════════════════════
# L codes — Logging errors
# ══════════════════════════════════════

# L10 — Log drain buffer overflow (logs dropped)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "L10"

# L11 — Tail buffer overflow
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "L11"

# All L errors
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "code=L[0-9]+"

# ══════════════════════════════════════
# Combined: All error codes
# ══════════════════════════════════════
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "code=[HRL][0-9]+"
```

---

### 9c. Filter — Dyno State Changes (lifecycle events)

```bash
HEROKU_PAYLOAD='{"source":"heroku","lines":1500,"tail":false}'
APP="my-app-staging"

# Dyno starting
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "Starting process"

# Dyno up (boot successful)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "State changed from starting to up"

# Dyno crashed
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "State changed from up to crashed"

# Dyno restarting (by user or platform)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "(Restarting|State changed from up to starting)"

# Dyno idle (Eco/Basic dynos sleep after 30 minutes)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "State changed from up to down"

# All state changes
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "State changed"

# Scaling events (dyno quantity changed)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "Scaling"

# Memory usage reports
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "sample#memory_total"

# Memory + swap details
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "sample#memory" | \
  sed 's/.*\(sample#memory_total=[^ ]*\).*\(sample#memory_swap=[^ ]*\).*/\1 \2/'
```

---

### 9d. Filter — App Logs (code output from Rails/Puma/Sidekiq)

```bash
APP_PAYLOAD='{"source":"app","lines":1500,"tail":false}'
APP="my-app-staging"

# ── Rails/Puma errors ──

# All exceptions
app_logs_grep "$APP" "$APP_PAYLOAD" "(Exception|Error|error|FATAL|fatal)"

# ActiveRecord errors (DB issues)
app_logs_grep "$APP" "$APP_PAYLOAD" "(ActiveRecord|PG::|Mysql2::)"

# Connection pool exhausted
app_logs_grep "$APP" "$APP_PAYLOAD" "(connection pool|ConnectionTimeoutError|could not obtain)"

# ActionController routing errors
app_logs_grep "$APP" "$APP_PAYLOAD" "(RoutingError|ActionController::)"

# ── Sidekiq/Worker logs ──

# Sidekiq job failures
app_logs_grep "$APP" '{"source":"app","dyno":"worker","lines":1500,"tail":false}' \
  "(WARN|ERROR|FATAL|fail|retry)"

# Sidekiq job processing
app_logs_grep "$APP" '{"source":"app","dyno":"worker","lines":500,"tail":false}' \
  "(start|done|fail).*jid"

# Sidekiq dead jobs (exhausted retries)
app_logs_grep "$APP" '{"source":"app","dyno":"worker","lines":1500,"tail":false}' \
  "dead"

# ── Rails request logs ──

# Completed requests with status
app_logs_grep "$APP" "$APP_PAYLOAD" "Completed [0-9]+"

# 500 responses only
app_logs_grep "$APP" "$APP_PAYLOAD" "Completed 500"

# Slow ActiveRecord queries (> 100ms)
app_logs_grep "$APP" "$APP_PAYLOAD" "ActiveRecord: [0-9]{3,}\."

# N+1 detection (many similar queries in sequence)
app_logs_grep "$APP" "$APP_PAYLOAD" "SELECT.*FROM" | \
  awk '{print $NF}' | sort | uniq -c | sort -rn | head -10

# ── Puma logs ──

# Puma worker spawning/booting
app_logs_grep "$APP" "$APP_PAYLOAD" "(puma|Puma|worker.*booted|cluster.*worker)"

# Puma backlog (requests queued)
app_logs_grep "$APP" "$APP_PAYLOAD" "backlog"
```

---

### 9e. Filter — Deploy & Release Logs

```bash
HEROKU_PAYLOAD='{"source":"heroku","lines":1500,"tail":false}'
APP="my-app-staging"

# Deploy events (new release)
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "(Deploy|Release v[0-9]+)"

# Config var changes
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "Set .* config var"

# Rollback events
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "Rollback"

# Build events
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "(Build|Slug)"

# Add-on changes
app_logs_grep "$APP" "$HEROKU_PAYLOAD" "(Attach|Detach|addon)"
```

---

### Log session parameters reference

| Parameter | Type    | Description                                           |
|-----------|---------|-------------------------------------------------------|
| `dyno`    | string  | Filter by dyno: `web`, `worker`, `web.1`...           |
| `lines`   | integer | Number of lines to return (1-1500, default 300)       |
| `tail`    | boolean | `true` = stream live, `false` = snapshot              |
| `source`  | string  | `app` (code logs) or `heroku` (platform logs)         |

### Log drains — send logs to external service

> ⚠️ POST/DELETE log drain operations require `full` mode and must ask user first.

```bash
# List log drains (✅ readonly OK)
heroku_api GET "/apps/my-app-staging/log-drains" | jq .

# Add log drain (⚠️ full only — ask first)
heroku_api POST "/apps/my-app-staging/log-drains" '{
  "url": "<YOUR_LOG_DRAIN_URL>"
}'

# Delete log drain (⚠️ full only — ask first)
heroku_api DELETE "/apps/my-app-staging/log-drains/DRAIN_ID"
```

---

## 10. Pipelines — CI/CD Flow

### List pipelines
```bash
heroku_api GET "/pipelines" | jq '.[] | {id, name}'
```

### Create pipeline
```bash
heroku_api POST "/pipelines" '{
  "name": "my-pipeline",
  "owner": {"id": "YOUR_TEAM_ID", "type": "team"}
}'
```

### Add app to pipeline
```bash
heroku_api POST "/pipeline-couplings" '{
  "app": "my-app-staging",
  "pipeline": "PIPELINE_ID",
  "stage": "staging"
}'

heroku_api POST "/pipeline-couplings" '{
  "app": "my-app-production",
  "pipeline": "PIPELINE_ID",
  "stage": "production"
}'
```

### Promote staging → production
```bash
# Step 1: Get staging coupling ID
STAGING_COUPLING=$(heroku_api GET "/apps/my-app-staging/pipeline-couplings" | jq -r '.id')

# Step 2: Promote
heroku_api POST "/pipeline-promotions" '{
  "pipeline": {"id": "PIPELINE_ID"},
  "source": {"app": {"id": "STAGING_APP_ID"}},
  "targets": [{"app": {"id": "PRODUCTION_APP_ID"}}]
}'
```

### View promotion status
```bash
heroku_api GET "/pipeline-promotions/PROMOTION_ID/promotion-targets" | \
  jq '.[] | {app: .app.id, status, error_message}'
```

---

## 11. Review Apps

### Enable review apps for pipeline
```bash
heroku_api POST "/pipelines/PIPELINE_ID/review-app-config" '{
  "automatic_review_apps": true,
  "destroy_stale_apps": true,
  "stale_days": 5,
  "wait_for_ci": true,
  "repo": "your-org/your-app"
}'
```

### Create review app manually
```bash
heroku_api POST "/review-apps" '{
  "branch": "feature/new-auth",
  "pipeline": "PIPELINE_ID",
  "source_blob": {
    "url": "https://github.com/your-org/your-app/archive/feature/new-auth.tar.gz"
  }
}'
```

### List review apps
```bash
heroku_api GET "/pipelines/PIPELINE_ID/review-apps" | \
  jq '.[] | {id, app: .app.name, branch, status, created_at}'
```

### Delete review app
```bash
heroku_api DELETE "/review-apps/REVIEW_APP_ID"
```

---

## 12. Webhooks — Event Notifications

### Create webhook
```bash
heroku_api POST "/apps/my-app-staging/webhooks" '{
  "include": ["api:release", "api:build", "dyno"],
  "level": "notify",
  "url": "https://myapp.dev/webhooks/heroku"
}' "Accept: application/vnd.heroku+json; version=3.webhooks"
```

### List webhooks
```bash
curl -sf https://api.heroku.com/apps/my-app-staging/webhooks \
  -H "Authorization: Bearer $HEROKU_API_KEY" \
  -H "Accept: application/vnd.heroku+json; version=3.webhooks" | jq .
```

### View webhook deliveries
```bash
curl -sf https://api.heroku.com/apps/my-app-staging/webhook-deliveries \
  -H "Authorization: Bearer $HEROKU_API_KEY" \
  -H "Accept: application/vnd.heroku+json; version=3.webhooks" | \
  jq '.[] | {id, status, event: .event.type, created_at}' | head -20
```

### Delete webhook
```bash
curl -sf -X DELETE https://api.heroku.com/apps/my-app-staging/webhooks/WEBHOOK_ID \
  -H "Authorization: Bearer $HEROKU_API_KEY" \
  -H "Accept: application/vnd.heroku+json; version=3.webhooks"
```

**Webhook event types:**
`api:release`, `api:build`, `api:addon`, `api:app`, `api:formation`, `api:domain`,
`dyno`, `api:sni-endpoint`

---

## 13. Collaborators & Team

### List collaborators
```bash
heroku_api GET "/apps/my-app-staging/collaborators" | \
  jq '.[] | {email: .user.email, role}'
```

### Add collaborator
```bash
heroku_api POST "/apps/my-app-staging/collaborators" '{
  "user": "dev@myapp.dev",
  "silent": false
}'
```

### Remove collaborator
```bash
heroku_api DELETE "/apps/my-app-staging/collaborators/dev@myapp.dev"
```

---

## 14. Dyno Sizing & Cost Reference

| Size          | RAM    | CPU Share | $/dyno/mo | Use case            |
|---------------|--------|-----------|-----------|---------------------|
| Eco           | 512MB  | 1x        | ~$5       | Dev/hobby           |
| Basic         | 512MB  | 1x        | ~$7       | Low traffic         |
| Standard-1X   | 512MB  | 1x        | ~$25      | Production default  |
| Standard-2X   | 1GB    | 2x        | ~$50      | Memory-heavy        |
| Performance-M | 2.5GB  | 100%      | ~$250     | High traffic        |
| Performance-L | 14GB   | 100%      | ~$500     | Enterprise          |

**Recommendation:** Standard-1X for staging, Standard-2X for production
(Rails + Bootsnap needs ~400-600MB).

---

## 15. Health Check Dashboard Script

```bash
#!/bin/bash
# health.sh — Quick health check via Heroku Platform API
# Usage: ./health.sh [staging|production]

ENV="${1:-staging}"
APP="my-app-${ENV}"

heroku_api() {
  local method="${1:-GET}" endpoint="$2" data="${3:-}" extra="${4:-}"
  local args=(-sf -X "$method"
    -H "Authorization: Bearer $HEROKU_API_KEY"
    -H "Accept: application/vnd.heroku+json; version=3"
    -H "Content-Type: application/json" -m 30)
  [[ -n "$extra" ]] && args+=(-H "$extra")
  [[ -n "$data" ]] && args+=(-d "$data")
  curl "${args[@]}" "https://api.heroku.com${endpoint}"
}

echo "╔══════════════════════════════════════════╗"
echo "║   Health Check — $ENV"
echo "╚══════════════════════════════════════════╝"
echo ""

echo "── App ──"
heroku_api GET "/apps/$APP" | jq -r '"  Name:        \(.name)\n  Region:      \(.region.name)\n  Stack:       \(.stack.name)\n  Maintenance: \(.maintenance)\n  Updated:     \(.updated_at)"'

echo ""
echo "── Dynos ──"
heroku_api GET "/apps/$APP/formation" | \
  jq -r '.[] | "  \(.type): \(.quantity)x \(.size) — \(.command[:60])"'

echo ""
echo "── Latest Release ──"
heroku_api GET "/apps/$APP/releases" "" "Range: version ..; order=desc, max=1" | \
  jq -r '.[0] | "  Version:  \(.version)\n  Status:   \(.status)\n  By:       \(.user.email)\n  At:       \(.created_at)\n  Desc:     \(.description)"'

echo ""
echo "── Add-ons ──"
heroku_api GET "/apps/$APP/addons" | \
  jq -r '.[] | "  \(.addon_service.name): \(.plan.name) [\(.state)]"'

echo ""
echo "── Domains ──"
heroku_api GET "/apps/$APP/domains" | \
  jq -r '.[] | "  \(.hostname) (\(.kind)) — \(.status)"'

echo ""
echo "── Recent Releases (last 5) ──"
heroku_api GET "/apps/$APP/releases" "" "Range: version ..; order=desc, max=5" | \
  jq -r '.[] | "  \(.version) | \(.status) | \(.description[:50]) | \(.created_at)"'
```

---

## 16. Safe Deploy Script

```bash
#!/bin/bash
# deploy.sh — Safe deploy workflow
# Usage: ./deploy.sh staging|production

set -euo pipefail

ENV="$1"
APP="my-app-${ENV}"

heroku_api() {
  local method="${1:-GET}" endpoint="$2" data="${3:-}" extra="${4:-}"
  local args=(-sf -X "$method"
    -H "Authorization: Bearer $HEROKU_API_KEY"
    -H "Accept: application/vnd.heroku+json; version=3"
    -H "Content-Type: application/json" -m 60 --retry 3 --retry-delay 2)
  [[ -n "$extra" ]] && args+=(-H "$extra")
  [[ -n "$data" ]] && args+=(-d "$data")
  curl "${args[@]}" "https://api.heroku.com${endpoint}"
}

echo "🚀 Deploying to $APP..."

# Step 1: Pre-deploy checks
echo "── Step 1: Pre-deploy checks ──"
MAINTENANCE=$(heroku_api GET "/apps/$APP" | jq -r '.maintenance')
CURRENT_VERSION=$(heroku_api GET "/apps/$APP/releases" "" "Range: version ..; order=desc, max=1" | jq -r '.[0].version')
echo "  Current: $CURRENT_VERSION | Maintenance: $MAINTENANCE"

# Step 2: Enable maintenance (production only)
if [[ "$ENV" == "production" ]]; then
  echo "── Step 2: Enabling maintenance mode ──"
  heroku_api PATCH "/apps/$APP" '{"maintenance":true}' > /dev/null
  echo "  Maintenance: ON"
fi

# Step 3: Create backup (production only)
if [[ "$ENV" == "production" ]]; then
  echo "── Step 3: Creating database backup ──"
  PG_ID=$(heroku_api GET "/apps/$APP/addons" | \
    jq -r '.[] | select(.addon_service.name=="heroku-postgresql") | .id')
  curl -sf -X POST "https://postgres-api.heroku.com/client/v11/databases/$PG_ID/backups" \
    -H "Authorization: Bearer $HEROKU_API_KEY" \
    -H "Content-Type: application/json" > /dev/null
  echo "  Backup initiated"
fi

# Step 4: Run migrations
echo "── Step 4: Running migrations ──"
DYNO=$(heroku_api POST "/apps/$APP/dynos" '{
  "command": "rake db:migrate",
  "attach": false,
  "size": "Standard-1X",
  "time_to_live": 1800
}')
DYNO_NAME=$(echo "$DYNO" | jq -r '.name')
echo "  Migration dyno: $DYNO_NAME"
echo "  Waiting for completion..."
sleep 30

# Step 5: Restart dynos
echo "── Step 5: Restarting dynos ──"
heroku_api DELETE "/apps/$APP/dynos" > /dev/null
echo "  All dynos restarted"

# Step 6: Disable maintenance
if [[ "$ENV" == "production" ]]; then
  echo "── Step 6: Disabling maintenance mode ──"
  heroku_api PATCH "/apps/$APP" '{"maintenance":false}' > /dev/null
  echo "  Maintenance: OFF"
fi

# Step 7: Verify
echo "── Step 7: Verification ──"
sleep 10
NEW_VERSION=$(heroku_api GET "/apps/$APP/releases" "" "Range: version ..; order=desc, max=1" | jq -r '.[0].version')
echo "  New release: $NEW_VERSION"
echo "  Rollback command: heroku_api POST /apps/$APP/releases '{\"release\":\"$CURRENT_VERSION\"}'"
echo ""
echo "✅ Deploy complete!"
```

---

## 17. Rate Limits & Error Handling

Heroku API rate limit: **4500 requests/hour** per token.

```bash
# Check remaining rate limit
curl -sI https://api.heroku.com/account \
  -H "Authorization: Bearer $HEROKU_API_KEY" \
  -H "Accept: application/vnd.heroku+json; version=3" | \
  grep -i 'ratelimit-remaining'
```

**Common error codes:**

| Code | Meaning                 | Action                        |
|------|-------------------------|-------------------------------|
| 401  | Token invalid/expired   | Regenerate API key            |
| 403  | Insufficient permission | Check token scope             |
| 404  | Resource not found      | Check app name / addon ID     |
| 422  | Validation error        | Read response body            |
| 429  | Rate limited            | Retry after `Retry-After` hdr |
| 503  | Service unavailable     | Retry with exponential backoff|

```bash
# Robust request with error handling
heroku_api_safe() {
  local response http_code body
  response=$(curl -sw '\n%{http_code}' \
    -X "$1" "https://api.heroku.com$2" \
    -H "Authorization: Bearer $HEROKU_API_KEY" \
    -H "Accept: application/vnd.heroku+json; version=3" \
    -H "Content-Type: application/json" \
    ${3:+-d "$3"} -m 30)

  http_code=$(echo "$response" | tail -1)
  body=$(echo "$response" | sed '$d')

  if [[ "$http_code" -ge 200 && "$http_code" -lt 300 ]]; then
    echo "$body"
  elif [[ "$http_code" == "429" ]]; then
    echo "⚠️  Rate limited. Retrying in 60s..." >&2
    sleep 60
    heroku_api_safe "$@"
  else
    echo "❌ HTTP $http_code:" >&2
    echo "$body" | jq . >&2
    return 1
  fi
}
```

---

## 18. CI/CD Integration — GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Create source tarball
        run: tar czf source.tar.gz --exclude='.git' .

      - name: Upload & build on Heroku
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
        run: |
          # Upload source
          UPLOAD=$(curl -sf -X POST https://api.heroku.com/sources \
            -H "Authorization: Bearer $HEROKU_API_KEY" \
            -H "Accept: application/vnd.heroku+json; version=3")

          PUT_URL=$(echo "$UPLOAD" | jq -r '.source_blob.put_url')
          GET_URL=$(echo "$UPLOAD" | jq -r '.source_blob.get_url')

          curl -sf -X PUT "$PUT_URL" \
            -H "Content-Type: application/gzip" \
            --data-binary @source.tar.gz

          # Trigger build
          BUILD=$(curl -sf -X POST \
            https://api.heroku.com/apps/my-app-staging/builds \
            -H "Authorization: Bearer $HEROKU_API_KEY" \
            -H "Accept: application/vnd.heroku+json; version=3" \
            -H "Content-Type: application/json" \
            -d "{\"source_blob\":{\"url\":\"$GET_URL\",\"version\":\"$GITHUB_SHA\"}}")

          BUILD_ID=$(echo "$BUILD" | jq -r '.id')

          # Wait for build
          for i in $(seq 1 60); do
            STATUS=$(curl -sf \
              https://api.heroku.com/apps/my-app-staging/builds/$BUILD_ID \
              -H "Authorization: Bearer $HEROKU_API_KEY" \
              -H "Accept: application/vnd.heroku+json; version=3" | \
              jq -r '.status')

            echo "Build status: $STATUS"
            [[ "$STATUS" == "succeeded" ]] && exit 0
            [[ "$STATUS" == "failed" ]] && exit 1
            sleep 10
          done
          echo "Build timeout" && exit 1
```

---

## Appendix: Quick Reference

### Main Endpoints

| Resource            | Method  | Endpoint                                      |
|---------------------|---------|-----------------------------------------------|
| App info            | GET     | `/apps/{app}`                                 |
| Config vars         | GET     | `/apps/{app}/config-vars`                     |
| Set config          | PATCH   | `/apps/{app}/config-vars`                     |
| Formation           | GET     | `/apps/{app}/formation`                       |
| Scale               | PATCH   | `/apps/{app}/formation`                       |
| Dynos               | GET     | `/apps/{app}/dynos`                           |
| Restart all         | DELETE  | `/apps/{app}/dynos`                           |
| Run one-off         | POST    | `/apps/{app}/dynos`                           |
| Releases            | GET     | `/apps/{app}/releases`                        |
| Rollback            | POST    | `/apps/{app}/releases`                        |
| Builds              | POST    | `/apps/{app}/builds`                          |
| Build info          | GET     | `/apps/{app}/builds/{build}`                  |
| Add-ons             | GET     | `/apps/{app}/addons`                          |
| Create add-on       | POST    | `/apps/{app}/addons`                          |
| Domains             | GET     | `/apps/{app}/domains`                         |
| Log sessions        | POST    | `/apps/{app}/log-sessions`                    |
| Log drains          | GET     | `/apps/{app}/log-drains`                      |
| Webhooks            | POST    | `/apps/{app}/webhooks`                        |
| Pipelines           | GET     | `/pipelines`                                  |
| Promote             | POST    | `/pipeline-promotions`                        |
| Review apps         | POST    | `/review-apps`                                |
| Source upload        | POST    | `/sources`                                    |
| SSL/SNI             | GET     | `/apps/{app}/sni-endpoints`                   |

### Required headers for every request
```
Authorization: Bearer $HEROKU_API_KEY
Accept: application/vnd.heroku+json; version=3
Content-Type: application/json
```

### Special headers
```
# Pagination (for list endpoints)
Range: version ..; order=desc, max=10

# Webhooks (uses version 3.webhooks)
Accept: application/vnd.heroku+json; version=3.webhooks
```
