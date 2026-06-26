#!/usr/bin/env bash
# prepare-agents.sh — create git worktrees for research subagents from the shared lab repo.
# Each agent gets its own branch in ~/.litmus/repo/ and a worktree at ~/.litmus/agents/<id>/.
# Agents can browse all branches, cherry-pick changes, and build on each other's commits.
#
# Usage:
#   bash prepare-agents.sh --agents 4 --templates architecture,optimizer,general,general
#   bash prepare-agents.sh --agents 2 --templates general,general --time-budget 300
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
BASE_DIR="${LITMUS_BASE:-$HOME/.litmus}"
LAB_REPO="$BASE_DIR/repo"
SHARED_DIR="$BASE_DIR/shared"
TEMPLATES_DIR="$REPO_DIR/references/templates"

NUM_AGENTS=2
TEMPLATES_CSV="general,general"
TIME_BUDGET=300

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agents)      NUM_AGENTS="$2";    shift 2 ;;
    --templates)   TEMPLATES_CSV="$2"; shift 2 ;;
    --time-budget) TIME_BUDGET="$2";   shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

IFS=',' read -ra TEMPLATES <<< "$TEMPLATES_CSV"

# Detect GPU count
if command -v nvidia-smi &>/dev/null; then
  GPU_COUNT=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | wc -l | tr -d ' ')
else
  GPU_COUNT=1
fi

# Verify the lab repo exists (setup.sh must run first)
if [ ! -d "$LAB_REPO/.git" ]; then
  echo "Error: lab repo not found at $LAB_REPO"
  echo "Run setup.sh first."
  exit 1
fi

echo "=== Preparing $NUM_AGENTS research agent worktree(s) ==="
echo "Templates:   ${TEMPLATES[*]}"
echo "Time budget: ${TIME_BUDGET}s per experiment"
echo "GPUs:        $GPU_COUNT"
echo "Lab repo:    $LAB_REPO"
echo ""

DATE_TAG=$(date +%Y%m%d)
AGENT_IDS=()

for i in $(seq 1 "$NUM_AGENTS"); do
  TEMPLATE_IDX=$(( (i - 1) % ${#TEMPLATES[@]} ))
  TEMPLATE="${TEMPLATES[$TEMPLATE_IDX]}"

  case "$TEMPLATE" in
    architecture)   SHORT="arch" ;;
    optimizer)      SHORT="opt"  ;;
    regularization) SHORT="reg"  ;;
    tokenization)   SHORT="tok"  ;;
    general)        SHORT="gen"  ;;
    *)              SHORT="$TEMPLATE" ;;
  esac

  AGENT_ID="${SHORT}-${i}"
  BRANCH="litmus/agent-${AGENT_ID}-${DATE_TAG}"
  AGENT_DIR="$BASE_DIR/agents/$AGENT_ID"
  GPU_ID=$(( (i - 1) % GPU_COUNT ))

  echo "Agent $i: id=$AGENT_ID  branch=$BRANCH  gpu=$GPU_ID"

  # Remove any existing worktree for this agent
  if [ -d "$AGENT_DIR" ]; then
    git -C "$LAB_REPO" worktree remove "$AGENT_DIR" --force 2>/dev/null || rm -rf "$AGENT_DIR"
    git -C "$LAB_REPO" branch -D "$BRANCH" 2>/dev/null || true
  fi

  # Create a fresh worktree on a new branch from main
  git -C "$LAB_REPO" worktree add "$AGENT_DIR" -b "$BRANCH" main -q
  git -C "$AGENT_DIR" config user.email "agent-${AGENT_ID}@litmus"
  git -C "$AGENT_DIR" config user.name "Agent ${AGENT_ID}"

  # Build program.md: inject config header + focus template + base program
  FOCUS_CONTENT=""
  if [ -f "$TEMPLATES_DIR/$TEMPLATE.md" ]; then
    FOCUS_CONTENT="$(cat "$TEMPLATES_DIR/$TEMPLATE.md")"
  fi

  CONFIG_HEADER="<!-- AGENT_ID: $i -->
<!-- TOTAL_AGENTS: $NUM_AGENTS -->
<!-- RESEARCH_FOCUS: $TEMPLATE -->
<!-- SHARED_DIR: $SHARED_DIR -->
<!-- LAB_REPO: $LAB_REPO -->
<!-- BRANCH: $BRANCH -->
<!-- GPU_ID: $GPU_ID -->
<!-- TIME_BUDGET: $TIME_BUDGET -->"

  PROGRAM_BASE="$(cat "$REPO_DIR/references/program.md")"

  # Substitute config block placeholder
  PROGRAM_BASE="${PROGRAM_BASE//<!-- AGENT_ID: 1 -->/$CONFIG_HEADER}"
  PROGRAM_BASE="${PROGRAM_BASE//<!-- TOTAL_AGENTS: 4 -->}"
  PROGRAM_BASE="${PROGRAM_BASE//<!-- RESEARCH_FOCUS: general -->}"
  PROGRAM_BASE="${PROGRAM_BASE//<!-- SHARED_DIR: ~/.litmus\/shared -->}"
  PROGRAM_BASE="${PROGRAM_BASE//<!-- LAB_REPO: ~/.litmus\/repo -->}"
  PROGRAM_BASE="${PROGRAM_BASE//<!-- BRANCH: litmus\/agent-gen-1-20260101 -->}"
  PROGRAM_BASE="${PROGRAM_BASE//<!-- GPU_ID: 0 -->}"
  PROGRAM_BASE="${PROGRAM_BASE//<!-- TIME_BUDGET: 300 -->}"

  # Replace literal placeholder strings in program body
  PROGRAM_BASE="${PROGRAM_BASE//AGENT_ID/$i}"
  PROGRAM_BASE="${PROGRAM_BASE//GPU_ID/$GPU_ID}"
  PROGRAM_BASE="${PROGRAM_BASE//SHARED_DIR/$SHARED_DIR}"
  PROGRAM_BASE="${PROGRAM_BASE//LAB_REPO/$LAB_REPO}"
  PROGRAM_BASE="${PROGRAM_BASE//MY_BRANCH/$BRANCH}"
  PROGRAM_BASE="${PROGRAM_BASE//TIME_BUDGET/$TIME_BUDGET}"

  # Inject focus template
  PROGRAM_FINAL="${PROGRAM_BASE//<!-- FOCUS_INSTRUCTIONS injected here by prepare-agents.sh -->/$FOCUS_CONTENT}"

  echo "$PROGRAM_FINAL" > "$AGENT_DIR/program.md"

  # results.tsv is local to each worktree — not committed, not shared
  # (shared/attempts/ JSON is the cross-agent source of truth)
  echo -e "commit\tval_bpb\tpeak_vram_gb\tstatus\tdescription" > "$AGENT_DIR/results.tsv"
  echo "results.tsv" >> "$AGENT_DIR/.git/info/exclude" 2>/dev/null || true
  echo "run.log"     >> "$AGENT_DIR/.git/info/exclude" 2>/dev/null || true

  AGENT_IDS+=("$AGENT_ID")
  echo "  Worktree ready: $AGENT_DIR  (branch: $BRANCH)"
done

# Record worker count for watchdog
echo "$NUM_AGENTS" > "$SHARED_DIR/worker-count.txt"

echo ""
echo "=== Worktrees created. Git structure ==="
git -C "$LAB_REPO" worktree list
echo ""
echo "All experiment history visible via:"
echo "  git -C $LAB_REPO log --all --oneline --graph"
echo ""

echo "=== Spawn commands (OpenClaw native subagents) ==="
echo ""
for AGENT_ID in "${AGENT_IDS[@]}"; do
  AGENT_DIR="$BASE_DIR/agents/$AGENT_ID"
  echo "sessions_spawn  task:\"Read program.md in your current directory and run the research loop forever.\"  runtime:\"subagent\"  mode:\"session\"  agentId:\"litmus-worker-$AGENT_ID\"  cwd:\"$AGENT_DIR\""
done
echo ""
echo "Then: sessions_yield  message:\"Research agents started. I'll notify you on discoveries.\""
