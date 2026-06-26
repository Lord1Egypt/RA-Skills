---
name: post-deployment-verifier
description: Verify deployments are healthy after release — check endpoints, compare response schemas, validate metrics, run smoke tests, verify database migrations, and produce a deployment confidence report.
---

# Post-Deployment Verifier

After deploying, verify everything works before calling it done. Checks health endpoints, validates response schemas match expectations, monitors error rates, verifies database state, and produces a confidence score.

Use when: "verify the deployment", "is the deploy healthy", "post-deploy checks", "deployment smoke test", "verify production", "deploy confidence check", or after any release.

## Commands

### 1. `verify` — Full Post-Deployment Verification

Run all checks and produce a deployment confidence report.

#### Check 1: Health Endpoints

```bash
echo "=== Health Check ==="

# Discover health endpoints from config
ENDPOINTS=""

# From environment variables
for var in $(env | grep -iE "URL|HOST|ENDPOINT|SERVICE" | cut -d= -f2); do
  if echo "$var" | grep -qE "^https?://"; then
    ENDPOINTS="$ENDPOINTS $var/health $var/healthz $var/ready $var/status"
  fi
done

# From docker-compose
if [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
  PORTS=$(grep -oP 'ports:\s*\n\s*-\s*"\K[0-9]+' docker-compose*.yml 2>/dev/null | head -5)
  for port in $PORTS; do
    ENDPOINTS="$ENDPOINTS http://localhost:$port/health http://localhost:$port/healthz"
  done
fi

# From kubernetes
rg -o "readinessProbe:.*path:\s*(\S+)" -g '*.yaml' -g '*.yml' 2>/dev/null | head -5

# Check each endpoint
for endpoint in $ENDPOINTS; do
  RESPONSE=$(curl -s -o /tmp/health_body -w "%{http_code} %{time_total}s" --connect-timeout 5 --max-time 10 "$endpoint" 2>/dev/null)
  HTTP_CODE=$(echo "$RESPONSE" | awk '{print $1}')
  TIME=$(echo "$RESPONSE" | awk '{print $2}')

  if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ $endpoint → $HTTP_CODE (${TIME})"
  elif [ "$HTTP_CODE" = "000" ]; then
    echo "❌ $endpoint → UNREACHABLE"
  else
    echo "⚠️  $endpoint → $HTTP_CODE (${TIME})"
    cat /tmp/health_body 2>/dev/null | head -3
  fi
done
```

#### Check 2: Response Validation

```bash
echo ""
echo "=== Response Validation ==="

# Check key API endpoints return expected structure
# Read endpoints from a .deploy-verify.json config file if it exists
if [ -f ".deploy-verify.json" ]; then
  python3 -c "
import json, urllib.request, sys

config = json.load(open('.deploy-verify.json'))
for check in config.get('endpoints', []):
    url = check['url']
    expected_status = check.get('status', 200)
    expected_fields = check.get('fields', [])
    method = check.get('method', 'GET')

    try:
        req = urllib.request.Request(url, method=method)
        for k, v in check.get('headers', {}).items():
            req.add_header(k, v)
        resp = urllib.request.urlopen(req, timeout=10)
        status = resp.status
        body = json.loads(resp.read())

        if status != expected_status:
            print(f'⚠️  {method} {url} → {status} (expected {expected_status})')
        else:
            missing = [f for f in expected_fields if f not in body]
            if missing:
                print(f'⚠️  {method} {url} → {status} OK but missing fields: {missing}')
            else:
                print(f'✅ {method} {url} → {status}, all expected fields present')
    except Exception as e:
        print(f'❌ {method} {url} → {e}')
" 2>/dev/null
else
  echo "No .deploy-verify.json config found. Create one for automated response validation."
  echo "Example:"
  echo '  {"endpoints": [{"url": "https://api.example.com/v1/status", "status": 200, "fields": ["version", "status"]}]}'
fi
```

#### Check 3: Version Verification

```bash
echo ""
echo "=== Version Check ==="

# Get expected version from package.json or git tag
EXPECTED_VERSION=""
if [ -f "package.json" ]; then
  EXPECTED_VERSION=$(python3 -c "import json; print(json.load(open('package.json')).get('version',''))" 2>/dev/null)
fi
[ -z "$EXPECTED_VERSION" ] && EXPECTED_VERSION=$(git describe --tags --abbrev=0 2>/dev/null | sed 's/^v//')
echo "Expected version: ${EXPECTED_VERSION:-unknown}"

# Check deployed version via health/status endpoint
for endpoint in $ENDPOINTS; do
  BODY=$(curl -s --connect-timeout 5 "$endpoint" 2>/dev/null)
  DEPLOYED=$(echo "$BODY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('version',d.get('app_version',d.get('build','?'))))" 2>/dev/null)
  if [ -n "$DEPLOYED" ] && [ "$DEPLOYED" != "?" ]; then
    if [ "$DEPLOYED" = "$EXPECTED_VERSION" ]; then
      echo "✅ Deployed version matches: $DEPLOYED"
    else
      echo "⚠️  Version mismatch: deployed=$DEPLOYED, expected=$EXPECTED_VERSION"
    fi
  fi
done
```

#### Check 4: Error Rate Monitoring

```bash
echo ""
echo "=== Error Monitoring ==="

# Check recent application logs for errors
if command -v docker &>/dev/null; then
  echo "--- Docker container logs (last 5 min) ---"
  for container in $(docker ps --format "{{.Names}}" 2>/dev/null); do
    ERRORS=$(docker logs --since 5m "$container" 2>&1 | grep -ciE "error|exception|fatal|panic" 2>/dev/null)
    if [ "$ERRORS" -gt 0 ]; then
      echo "⚠️  $container: $ERRORS errors in last 5 minutes"
      docker logs --since 5m "$container" 2>&1 | grep -iE "error|exception|fatal|panic" | tail -3
    else
      echo "✅ $container: no errors"
    fi
  done
fi

# Check systemd service logs
if command -v journalctl &>/dev/null; then
  echo "--- Systemd service logs (last 5 min) ---"
  for svc in $(systemctl list-units --type=service --state=running --no-legend 2>/dev/null | awk '{print $1}' | grep -v systemd); do
    ERRORS=$(journalctl -u "$svc" --since "5 min ago" --no-pager -q 2>/dev/null | grep -ciE "error|exception|fatal" 2>/dev/null)
    [ "$ERRORS" -gt 0 ] && echo "⚠️  $svc: $ERRORS errors"
  done
fi
```

#### Check 5: Database Migration Verification

```bash
echo ""
echo "=== Database State ==="

# Check if migrations are up to date
if [ -f "package.json" ]; then
  # Prisma
  rg -q "prisma" package.json 2>/dev/null && echo "Prisma detected — run: npx prisma migrate status"
  # TypeORM
  rg -q "typeorm" package.json 2>/dev/null && echo "TypeORM detected — run: npx typeorm migration:show"
  # Sequelize
  rg -q "sequelize" package.json 2>/dev/null && echo "Sequelize detected — run: npx sequelize db:migrate:status"
fi

# Python/Django
[ -f "manage.py" ] && echo "Django detected — run: python manage.py showmigrations"

# Rails
[ -f "Gemfile" ] && grep -q "rails" Gemfile 2>/dev/null && echo "Rails detected — run: rails db:migrate:status"

# Check for pending migration files
PENDING=$(find . -path "*/migrations/*" -name "*.sql" -newer .last-deploy-timestamp 2>/dev/null | wc -l)
[ "$PENDING" -gt 0 ] && echo "⚠️  $PENDING migration files newer than last deploy"
```

#### Check 6: Resource Utilization

```bash
echo ""
echo "=== Resource Check ==="

# Docker resource usage
if command -v docker &>/dev/null; then
  docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" 2>/dev/null | head -10
fi

# System resources
echo "--- System ---"
free -h | head -2
df -h / | tail -1
uptime
```

### 2. `quick` — Quick Health Check

Run only health endpoint checks (Check 1) for fast verification. Use immediately after deploy.

### 3. `config` — Generate Verification Config

Create a `.deploy-verify.json` file with endpoints to check:

```json
{
  "endpoints": [
    {
      "url": "https://api.example.com/health",
      "status": 200,
      "fields": ["status", "version"]
    },
    {
      "url": "https://api.example.com/v1/users",
      "method": "GET",
      "status": 200,
      "headers": {"Authorization": "Bearer ${API_TOKEN}"},
      "fields": ["data", "pagination"]
    }
  ],
  "thresholds": {
    "max_response_time_ms": 500,
    "max_error_rate_percent": 1,
    "min_uptime_percent": 99.9
  }
}
```

### 4. `report` — Deployment Confidence Report

```markdown
# Deployment Verification Report
Date: [date] | Version: [version] | Environment: [env]

## Confidence Score: 92/100 🟢

| Check | Status | Details |
|-------|--------|---------|
| Health endpoints | ✅ Pass | 3/3 healthy |
| Response schema | ✅ Pass | All fields present |
| Version match | ✅ Pass | v1.5.0 deployed |
| Error rate | ⚠️ Warning | 2 errors in 5 min |
| Database | ✅ Pass | All migrations applied |
| Resources | ✅ Pass | CPU 12%, Mem 45% |

## Action Required
- Monitor error rate for next 30 minutes (currently elevated)

## Recommendation: KEEP (no rollback needed)
```

Confidence scoring:
- **95-100**: All clear, no action needed
- **80-94**: Minor warnings, monitor closely
- **60-79**: Issues found, consider rollback if degrading
- **<60**: Significant problems, recommend rollback

## Output Formats

- **text** (default): Human-readable with status icons
- **json**: `{confidence: 92, checks: [{name, status, details}], recommendation: "KEEP"}`
- **markdown**: Stakeholder-ready report
- **slack**: Formatted for Slack webhook delivery

## Notes

- Run immediately after deployment for maximum value
- Config file (`.deploy-verify.json`) enables consistent, repeatable verification
- Does not require access to monitoring systems — uses direct endpoint checks
- For production: run from a separate monitoring instance, not the deployed service itself
- Complement with Datadog/Grafana dashboards for continuous monitoring
- Supports environment variable substitution in config (`${VAR}` syntax)
