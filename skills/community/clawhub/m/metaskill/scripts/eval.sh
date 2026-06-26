#!/bin/bash
# metaskill/eval.sh — Evaluate how well the metaskill system is working
# Usage: ./eval.sh [--report] [--save]
# Output: terminal summary + optional save to memory/metaskill-eval-YYYY-MM-DD.md

# Dynamic workspace detection — works for any OpenClaw user
WORKSPACE=$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null)
if [ -z "$WORKSPACE" ]; then
  WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
fi

# Try self-improving-agent first, fallback to metaskill's own learnings
if [ -f "$WORKSPACE/skills/self-improving-agent/.learnings/LEARNINGS.md" ]; then
  LEARNINGS="$WORKSPACE/skills/self-improving-agent/.learnings/LEARNINGS.md"
else
  # Fallback: use metaskill's own learnings dir
  mkdir -p "$WORKSPACE/skills/metaskill/.learnings"
  LEARNINGS="$WORKSPACE/skills/metaskill/.learnings/LEARNINGS.md"
  # Create file if not exists
  [ -f "$LEARNINGS" ] || echo -e "# Learnings Log\n\n---\n" > "$LEARNINGS"
fi

if [ -f "$WORKSPACE/skills/self-improving-agent/.learnings/ERRORS.md" ]; then
  ERRORS_FILE="$WORKSPACE/skills/self-improving-agent/.learnings/ERRORS.md"
else
  mkdir -p "$WORKSPACE/skills/metaskill/.learnings"
  ERRORS_FILE="$WORKSPACE/skills/metaskill/.learnings/ERRORS.md"
  [ -f "$ERRORS_FILE" ] || echo -e "# Errors Log\n\n---\n" > "$ERRORS_FILE"
fi

WINS="$WORKSPACE/skills/metaskill/.learnings/WINS.md"
EVAL_DIR="$WORKSPACE/memory/metaskill-evals"
DATE=$(date +%Y-%m-%d)
SAVE=false
[[ "$*" == *--save* ]] && SAVE=true

mkdir -p "$EVAL_DIR"

echo ""
echo "🧠 METASKILL EVAL — $DATE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "⚙️  SYSTEM STATUS"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROVIDER_STATUS=$(python3 -c "
import sys; sys.path.insert(0, '$SCRIPT_DIR')
from llm_provider import get_status
import json; print(json.dumps(get_status()))
" 2>/dev/null)

if [ -n "$PROVIDER_STATUS" ]; then
  FAST_PROVIDER=$(echo "$PROVIDER_STATUS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('fast',{}).get('provider','?'))")
  FAST_MODEL=$(echo "$PROVIDER_STATUS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('fast',{}).get('model','?'))")
  FAST_READY=$(echo "$PROVIDER_STATUS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('fast',{}).get('ready',False))")
  DEEP_PROVIDER=$(echo "$PROVIDER_STATUS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('deep',{}).get('provider','?'))")
  DEEP_MODEL=$(echo "$PROVIDER_STATUS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('deep',{}).get('model','?'))")
  DEEP_READY=$(echo "$PROVIDER_STATUS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('deep',{}).get('ready',False))")

  if [ "$FAST_READY" = "True" ] || [ "$DEEP_READY" = "True" ]; then
    echo "   Version: v1.2 (LLM-powered extraction active)"
    echo "   Fast provider : $FAST_PROVIDER / $FAST_MODEL $([ "$FAST_READY" = "True" ] && echo "✅" || echo "❌ missing key")"
    echo "   Deep provider : $DEEP_PROVIDER / $DEEP_MODEL $([ "$DEEP_READY" = "True" ] && echo "✅" || echo "❌ missing key")"
  else
    echo "   Version: v1.0 fallback (Manual extraction mode)"
    echo "   No LLM provider ready. Edit skills/metaskill/config.yaml and set the required env var."
    echo "   Fast: $FAST_PROVIDER → needs \$$(python3 -c "import sys; sys.path.insert(0,'$SCRIPT_DIR'); from llm_provider import _load_config; c=_load_config(); print(c['env_vars'].get(c['providers']['fast'],'?'))" 2>/dev/null)"
  fi
else
  echo "   Version: v1.0 fallback (llm_provider.py unavailable)"
fi

# ── GAP 1: Self-correction depth ────────────────────────────────────────────
echo ""
echo "📊 GAP 1: Self-Correction Depth"
echo "   (Are we extracting 3 levels, or just surface?)"
echo ""

# Count total learnings (## headers)
TOTAL_LEARNINGS=$(grep -c "^## " "$LEARNINGS" 2>/dev/null); TOTAL_LEARNINGS=${TOTAL_LEARNINGS:-0}

# Count deep corrections (entries that have Surface + Principle + Habit keywords)
DEEP=$(grep -c -i "habit:\|habit —\|\*\*habit\*\*" "$LEARNINGS" 2>/dev/null); DEEP=${DEEP:-0}
SURFACE_ONLY=$((TOTAL_LEARNINGS - DEEP))

if [ "$TOTAL_LEARNINGS" -gt 0 ]; then
  DEPTH_PCT=$((DEEP * 100 / TOTAL_LEARNINGS))
else
  DEPTH_PCT=0
fi

echo "   Total learnings:    $TOTAL_LEARNINGS"
echo "   3-level (deep):     $DEEP ($DEPTH_PCT%)"
echo "   Surface-only:       $SURFACE_ONLY"

if [ "$DEPTH_PCT" -lt 20 ]; then
  DEPTH_GRADE="🔴 Critical — most corrections are surface-only"
elif [ "$DEPTH_PCT" -lt 50 ]; then
  DEPTH_GRADE="🟡 Developing — some depth, but inconsistent"
elif [ "$DEPTH_PCT" -lt 80 ]; then
  DEPTH_GRADE="🟢 Good — majority are deep corrections"
else
  DEPTH_GRADE="✅ Excellent"
fi
echo "   Grade: $DEPTH_GRADE"

# Identify repeat offenders (same category/keyword appearing 3+ times)
echo ""
echo "   ⚠️  Repeat error patterns (category appearing 3x+):"
grep -i "category:\|**category**" "$LEARNINGS" 2>/dev/null | \
  sed 's/.*category.*: *//i' | tr '[:upper:]' '[:lower:]' | tr -d '**' | \
  sort | uniq -c | sort -rn | \
  awk '$1 >= 3 {printf "      %dx: %s\n", $1, $2}' | head -5
echo ""

# ── GAP 2: Transfer learning ─────────────────────────────────────────────────
echo "📊 GAP 2: Transfer Learning"
echo "   (Are principles crossing domains?)"
echo ""

# Heuristic: count learnings with cross-domain language ("also applies", "same pattern", "analogous")
TRANSFERS=$(grep -ci "also applies\|same pattern\|analogous\|similar to\|cross-domain\|generalize\|applies to all\|pattern:" "$LEARNINGS" 2>/dev/null); TRANSFERS=${TRANSFERS:-0}

# Check if transfer-check.sh has been used (look for invocations in daily notes)
TRANSFER_USES=$(grep -rl "transfer-check" "$WORKSPACE/memory/" 2>/dev/null | wc -l | tr -d ' '); TRANSFER_USES=${TRANSFER_USES:-0}

echo "   Cross-domain principles:  $TRANSFERS"
echo "   transfer-check.sh uses:   $TRANSFER_USES (in daily notes)"

if [ "$TRANSFERS" -lt 3 ]; then
  TRANSFER_GRADE="🔴 Critical — learnings are siloed, not transferring"
elif [ "$TRANSFERS" -lt 8 ]; then
  TRANSFER_GRADE="🟡 Developing — some transfer, mostly accidental"
else
  TRANSFER_GRADE="🟢 Good — principles are actively crossing domains"
fi
echo "   Grade: $TRANSFER_GRADE"
echo ""

# ── GAP 3: Proactive pattern recognition (win/error ratio) ───────────────────
echo "📊 GAP 3: Proactive Pattern Recognition"
echo "   (Win:Error ratio — are we learning from what works?)"
echo ""

WINS_COUNT=$(grep -c "^## " "$WINS" 2>/dev/null); WINS_COUNT=${WINS_COUNT:-0}
ERRORS_COUNT=$(grep -c "^## " "$ERRORS_FILE" 2>/dev/null); ERRORS_COUNT=${ERRORS_COUNT:-0}

echo "   Wins logged:    $WINS_COUNT"
echo "   Errors logged:  $ERRORS_COUNT"

if [ "$((WINS_COUNT + ERRORS_COUNT))" -gt 0 ]; then
  WIN_PCT=$((WINS_COUNT * 100 / (WINS_COUNT + ERRORS_COUNT)))
else
  WIN_PCT=0
fi
echo "   Win ratio:      $WIN_PCT%  (target: ≥40%)"

if [ "$WIN_PCT" -lt 10 ]; then
  WIN_GRADE="🔴 Critical — almost entirely reactive, no wins captured"
elif [ "$WIN_PCT" -lt 30 ]; then
  WIN_GRADE="🟡 Developing — starting to capture wins"
elif [ "$WIN_PCT" -lt 50 ]; then
  WIN_GRADE="🟢 Good — balanced learning"
else
  WIN_GRADE="✅ Excellent — proactive learner"
fi
echo "   Grade: $WIN_GRADE"
echo ""

# ── OVERALL SCORE ─────────────────────────────────────────────────────────────
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📈 OVERALL METASKILL SCORE"
echo ""

SCORE=$((DEPTH_PCT / 3 + TRANSFERS * 5 + WIN_PCT / 3))
# cap at 100
[ $SCORE -gt 100 ] && SCORE=100

echo "   Score: $SCORE / 100"

if [ $SCORE -lt 25 ]; then
  echo "   Status: 🔴 Early stage — foundational work needed"
elif [ $SCORE -lt 50 ]; then
  echo "   Status: 🟡 Developing — patterns emerging but inconsistent"
elif [ $SCORE -lt 75 ]; then
  echo "   Status: 🟢 Functional — metaskill working, room to grow"
else
  echo "   Status: ✅ Advanced — strong learning system"
fi

# ── RECOMMENDATIONS ───────────────────────────────────────────────────────────
echo ""
echo "💡 TOP RECOMMENDATIONS:"
echo ""

REC_COUNT=0

if [ "$DEPTH_PCT" -lt 50 ]; then
  echo "   1. Run deep-correct.sh on the last 5 surface-only learnings"
  echo "      → Convert them to 3-level (surface/principle/habit)"
  REC_COUNT=$((REC_COUNT+1))
fi

if [ "$TRANSFER_USES" -lt 3 ]; then
  echo "   2. Wire transfer-check.sh into pre-task routine"
  echo "      → Add to AGENTS.md: before any non-trivial task, run it"
  REC_COUNT=$((REC_COUNT+1))
fi

if [ "$WIN_PCT" -lt 20 ]; then
  echo "   3. Log at least 1 win this week via success-capture.sh"
  echo "      → Start small: what worked today?"
  REC_COUNT=$((REC_COUNT+1))
fi

if [ $SCORE -gt 60 ]; then
  echo "   ✅ System healthy — keep the cadence"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── SAVE TO FILE ──────────────────────────────────────────────────────────────
if [ "$SAVE" = true ]; then
  OUTFILE="$EVAL_DIR/$DATE.md"
  cat > "$OUTFILE" << INEOF
# Metaskill Eval — $DATE

## Scores
| Gap | Metric | Grade |
|-----|--------|-------|
| Self-correction depth | $DEPTH_PCT% deep (${DEEP}/${TOTAL_LEARNINGS}) | $DEPTH_GRADE |
| Transfer learning | $TRANSFERS cross-domain principles | $TRANSFER_GRADE |
| Proactive recognition | $WIN_PCT% win ratio (${WINS_COUNT} wins / ${ERRORS_COUNT} errors) | $WIN_GRADE |

**Overall: $SCORE/100**

## Recommendations
$([ "$DEPTH_PCT" -lt 50 ] && echo "- Run deep-correct.sh on last 5 surface-only learnings")
$([ "$TRANSFER_USES" -lt 3 ] && echo "- Wire transfer-check.sh into pre-task routine in AGENTS.md")
$([ "$WIN_PCT" -lt 20 ] && echo "- Log at least 1 win this week via success-capture.sh")

## Raw counts
- Total learnings: $TOTAL_LEARNINGS
- Deep (3-level): $DEEP
- Surface-only: $SURFACE_ONLY
- Wins: $WINS_COUNT
- Errors: $ERRORS_COUNT
- Transfer uses: $TRANSFER_USES
INEOF
  echo "   Saved → $OUTFILE"
fi
