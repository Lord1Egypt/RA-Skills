#!/usr/bin/env bash
# bootstrap-budget-check.sh — Monitor AGENTS.md size against bootstrap limit
# Pattern: Resource-Aware Optimization (16)
# Called by nightly consolidation cron. Also usable standalone.
set -uo pipefail

AGENTS_MD="$HOME/.openclaw/workspace/AGENTS.md"
BOOTSTRAP_LIMIT=20000
WARN_PCT=75
ALERT_PCT=85
CRIT_PCT=95

if [[ ! -f "$AGENTS_MD" ]]; then
  echo "ERROR: AGENTS.md not found at $AGENTS_MD"
  exit 1
fi

SIZE=$(wc -c < "$AGENTS_MD" | tr -d ' ')
PCT=$(( SIZE * 100 / BOOTSTRAP_LIMIT ))
HEADROOM=$(( BOOTSTRAP_LIMIT - SIZE ))

# Section-by-section breakdown
echo "=== AGENTS.md Bootstrap Budget ==="
echo "Size: ${SIZE} / ${BOOTSTRAP_LIMIT} chars (${PCT}%)"
echo "Headroom: ${HEADROOM} chars"
echo ""
# Show top sections by size
echo "Section breakdown:"
python3 -c "
content = open('$AGENTS_MD').read()
sections = content.split('\n## ')
for i, s in enumerate(sections):
    title = s.split('\n')[0][:50]
    size = len(s)
    pct = size * 100 // len(content)
    bar = '█' * (pct // 2) + '░' * (50 - pct // 2)
    print(f'  {size:5d} ({pct:2d}%) {title}')
" 2>/dev/null

echo ""

# Threshold checks
if [[ "$PCT" -ge "$CRIT_PCT" ]]; then
  echo "CRITICAL: ${PCT}% of limit — bootstrap WILL truncate. Trim immediately."
  echo "   Action: Move verbose sections to AGENTS-REFERENCE.md"
  exit 2
elif [[ "$PCT" -ge "$ALERT_PCT" ]]; then
  echo "ALERT: ${PCT}% of limit — approaching truncation zone."
  echo "   Action: Review sections >1000 chars for consolidation opportunities"
  exit 1
elif [[ "$PCT" -ge "$WARN_PCT" ]]; then
  echo "NOTE: ${PCT}% of limit — healthy but watch growth."
  exit 0
else
  echo "Healthy: ${PCT}% of limit — plenty of headroom."
  exit 0
fi