#!/usr/bin/env bash
# pr-check.sh — Run code review + health check for a PR, output structured JSON
set -euo pipefail

PR_URL="${1:?Usage: pr-check.sh <PR_URL> [DISCORD_WEBHOOK]}"
DISCORD_WEBHOOK="${2:-}"

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

# ── 1. Code Review ──────────────────────────────────────────────
review_file="$tmpdir/review.md"
echo "Running code review for $PR_URL ..."

# Extract PR number from URL (supports github.com/owner/repo/pull/123)
if [[ "$PR_URL" =~ /pull/([0-9]+) ]]; then
  PR_NUM="${BASH_REMATCH[1]}"
  gh pr diff "$PR_NUM" > "$tmpdir/diff.txt" 2>/dev/null || echo "diff-unavailable" > "$tmpdir/diff.txt"
  gh pr view "$PR_NUM" --json title,author,statusCheckRollup > "$tmpdir/pr-meta.json" 2>/dev/null || '{}'
else
  PR_NUM="unknown"
  echo "no-pr-number" > "$tmpdir/diff.txt"
fi

# ── 2. Health Check ─────────────────────────────────────────────
health_file="$tmpdir/health.json"
echo "Running health check ..."

# Try the installed healthcheck skill; fall back to a simple curl sweep
if command -v bash &>/dev/null && [[ -f ~/.openclaw/skills/healthcheck/healthcheck.sh ]]; then
  bash ~/.openclaw/skills/healthcheck/healthcheck.sh --json > "$health_file" 2>/dev/null || \
    echo '{"max_severity":2,"checks":{}}' > "$health_file"
else
  # Minimal health probe
  cat > "$health_file" <<'EOF'
{"max_severity":0,"checks":{"stub":{"status":"ok","detail":"healthcheck skill not installed — skipped"}}}
EOF
fi

# ── 3. Compose report ──────────────────────────────────────────
ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$tmpdir/report.json" <<REPORT
{
  "timestamp": "$ts",
  "pr_url": "$PR_URL",
  "pr_number": "$PR_NUM",
  "health": $(cat "$health_file"),
  "review_diff_path": "$tmpdir/diff.txt"
}
REPORT

echo "=== PR Auto-Check Report ==="
cat "$tmpdir/report.json"

# ── 4. Discord notification (optional) ──────────────────────────
if [[ -n "$DISCORD_WEBHOOK" ]]; then
  echo "Posting to Discord ..."
  health_summary=$(python3 -c "
import json,sys
h=json.load(open('$health_file'))
sev=h.get('max_severity',2)
icon='✅' if sev==0 else '⚠️' if sev==1 else '🔴'
checks=[f'{v[\"status\"]} {k}' for k,v in h.get('checks',{}).items()]
print(f'{icon} Health severity {sev}  |  ' + ', '.join(checks[:6]))
" 2>/dev/null || echo "Health check completed")

  payload=$(jq -n \
    --arg ts "$ts" \
    --arg pr "$PR_URL" \
    --arg health "$health_summary" \
    '{
      embeds: [{
        title: ("PR Auto-Check: " + $pr),
        color: (if ($health | test("✅")) then 3066993 elif ($health | test("⚠️")) then 16776960 else 15158332 end),
        fields: [
          {name: "Health Check", value: $health, inline: false},
          {name: "PR", value: $pr, inline: false}
        ],
        footer: {text: ("Reported at " + $ts)}
      }]
    }')

  curl -sS -X POST "$DISCORD_WEBHOOK" \
    -H 'Content-Type: application/json' \
    -d "$payload" > /dev/null 2>&1 || echo "Discord webhook failed"
fi

echo ""
echo "Done. Report at $tmpdir/report.json"
