#!/usr/bin/env bash
# scaffold.sh — goal-agent workspace generator
# Generates GOAL.md, STRATEGY.md, LEARNINGS.md, HEARTBEAT.md, evaluate.sh
# from templates, substituting all provided values.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATES_DIR="$SKILL_DIR/templates"

# ── Defaults ──────────────────────────────────────────────────────────────────
GOAL=""
METRIC=""
TARGET=""
DIRECTION="up"
CONSTRAINTS="None specified."
MAX_ITERATIONS="50"
OUTPUT_DIR="$(pwd)"

# ── Usage ─────────────────────────────────────────────────────────────────────
usage() {
  cat <<EOF
Usage: scaffold.sh --goal "..." --metric "..." --target NUMBER [OPTIONS]

Required:
  --goal "description"      What the agent is trying to achieve
  --metric "shell command"  Command that outputs a single number (the metric)
  --target NUMBER           Success threshold value

Optional:
  --direction up|down       Whether metric should increase (up) or decrease (down) [default: up]
  --constraints "text"      Safety constraints the agent must respect [default: none]
  --max-iterations N        Maximum heartbeat iterations [default: 50]
  --output-dir PATH         Where to write generated files [default: current directory]

Example:
  scaffold.sh \\
    --goal "Increase test coverage to 80%" \\
    --metric "npx jest --coverage 2>/dev/null | grep Statements | grep -oP '\d+\.\d+(?=%)'" \\
    --target 80 \\
    --direction up \\
    --constraints "Do not delete any tests." \\
    --max-iterations 20 \\
    --output-dir ~/clawd/goals/test-coverage
EOF
  exit 1
}

# ── Arg parsing ───────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --goal)           GOAL="$2";           shift 2 ;;
    --metric)         METRIC="$2";         shift 2 ;;
    --target)         TARGET="$2";         shift 2 ;;
    --direction)      DIRECTION="$2";      shift 2 ;;
    --constraints)    CONSTRAINTS="$2";    shift 2 ;;
    --max-iterations) MAX_ITERATIONS="$2"; shift 2 ;;
    --output-dir)     OUTPUT_DIR="$2";     shift 2 ;;
    -h|--help)        usage ;;
    *) echo "Unknown argument: $1"; usage ;;
  esac
done

# ── Validate required args ────────────────────────────────────────────────────
errors=()
[[ -z "$GOAL" ]]   && errors+=("--goal is required")
[[ -z "$METRIC" ]] && errors+=("--metric is required")
[[ -z "$TARGET" ]] && errors+=("--target is required")
[[ "$DIRECTION" != "up" && "$DIRECTION" != "down" ]] && errors+=("--direction must be 'up' or 'down'")
if ! [[ "$TARGET" =~ ^-?[0-9]+(\.[0-9]+)?$ ]]; then
  errors+=("--target must be a number")
fi
if ! [[ "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  errors+=("--max-iterations must be a positive integer")
fi

if [[ ${#errors[@]} -gt 0 ]]; then
  echo "Error(s):"
  for e in "${errors[@]}"; do echo "  • $e"; done
  echo ""
  usage
fi

# ── Derived values ────────────────────────────────────────────────────────────
if [[ "$DIRECTION" == "up" ]]; then
  DIRECTION_VERB="increase"
else
  DIRECTION_VERB="decrease"
fi

# ── Prepare output dir ────────────────────────────────────────────────────────
mkdir -p "$OUTPUT_DIR"

# ── Render helper: apply sed substitutions to a template ─────────────────────
render_template() {
  local tmpl="$1"
  local out="$2"

  # Use @ as separator to avoid conflicts with / in paths and commands
  sed \
    -e "s@{{GOAL_DESCRIPTION}}@${GOAL}@g" \
    -e "s@{{METRIC_COMMAND}}@${METRIC}@g" \
    -e "s@{{TARGET_VALUE}}@${TARGET}@g" \
    -e "s@{{DIRECTION}}@${DIRECTION}@g" \
    -e "s@{{DIRECTION_VERB}}@${DIRECTION_VERB}@g" \
    -e "s@{{CONSTRAINTS}}@${CONSTRAINTS}@g" \
    -e "s@{{MAX_ITERATIONS}}@${MAX_ITERATIONS}@g" \
    "$tmpl" > "$out"
}

# ── Render templates ──────────────────────────────────────────────────────────
echo "Generating goal-agent workspace in: $OUTPUT_DIR"

render_template "$TEMPLATES_DIR/GOAL.md.tmpl"        "$OUTPUT_DIR/GOAL.md"
echo "  ✓ GOAL.md"

render_template "$TEMPLATES_DIR/STRATEGY.md.tmpl"    "$OUTPUT_DIR/STRATEGY.md"
echo "  ✓ STRATEGY.md"

render_template "$TEMPLATES_DIR/LEARNINGS.md.tmpl"   "$OUTPUT_DIR/LEARNINGS.md"
echo "  ✓ LEARNINGS.md"

render_template "$TEMPLATES_DIR/HEARTBEAT.md.tmpl"   "$OUTPUT_DIR/HEARTBEAT.md"
echo "  ✓ HEARTBEAT.md"

render_template "$TEMPLATES_DIR/evaluate.sh.tmpl"    "$OUTPUT_DIR/evaluate.sh"
chmod +x "$OUTPUT_DIR/evaluate.sh"
echo "  ✓ evaluate.sh (chmod +x)"

# ── Summary ───────────────────────────────────────────────────────────────────
cat <<EOF

✅ Goal-agent workspace ready!

  Goal:    $GOAL
  Metric:  $METRIC
  Target:  $DIRECTION $TARGET
  Budget:  $MAX_ITERATIONS iterations

To activate, copy HEARTBEAT.md to your agent workspace:
  cp $OUTPUT_DIR/HEARTBEAT.md ~/clawd/HEARTBEAT.md

The agent will iterate toward the goal on every heartbeat.
EOF
