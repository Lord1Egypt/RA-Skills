#!/usr/bin/env bash
# setup.sh — one-time setup for litmus
# Clones the autoresearch harness, builds the shared git lab repo,
# installs deps, prepares training data, and initialises knowledge dirs.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
BASE_DIR="${LITMUS_BASE:-$HOME/.litmus}"
HARNESS_DIR="$BASE_DIR/harness"
LAB_REPO="$BASE_DIR/repo"          # shared git repo — all agent worktrees branch from here
SHARED_DIR="$BASE_DIR/shared"

echo "=== litmus setup ==="
echo "Base directory: $BASE_DIR"

# --- Create directory structure ---
mkdir -p "$BASE_DIR/agents" "$SHARED_DIR" "$BASE_DIR/logs"

# --- Shared knowledge sub-directories ---
mkdir -p \
  "$SHARED_DIR/attempts" \
  "$SHARED_DIR/notes/discoveries/architecture" \
  "$SHARED_DIR/notes/discoveries/optimizer" \
  "$SHARED_DIR/notes/discoveries/regularization" \
  "$SHARED_DIR/notes/discoveries/training" \
  "$SHARED_DIR/notes/anomalies" \
  "$SHARED_DIR/notes/moonshots" \
  "$SHARED_DIR/notes/synthesis" \
  "$SHARED_DIR/skills" \
  "$SHARED_DIR/synthesis"

echo "Created shared knowledge directories under $SHARED_DIR"

# --- Clone autoresearch harness ---
if [ ! -d "$HARNESS_DIR/.git" ]; then
  echo "Cloning autoresearch harness..."
  git clone https://github.com/karpathy/autoresearch "$HARNESS_DIR"
else
  echo "Harness already cloned at $HARNESS_DIR — pulling latest..."
  git -C "$HARNESS_DIR" pull --ff-only || echo "(pull failed — continuing with existing)"
fi

# --- Install Python deps ---
echo "Installing Python dependencies..."
(cd "$HARNESS_DIR" && uv sync)

# --- Check GPU ---
if command -v nvidia-smi &>/dev/null; then
  GPU_COUNT=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | wc -l | tr -d ' ')
  echo "GPUs detected: $GPU_COUNT"
  nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader 2>/dev/null \
    | awk -F', ' '{printf "  GPU %s: %s (%s)\n", $1, $2, $3}'
else
  echo "Warning: nvidia-smi not found — GPU detection skipped. Ensure CUDA is available."
  GPU_COUNT=1
fi

# --- Build the shared lab git repo (all agents share this, each on its own branch) ---
if [ ! -d "$LAB_REPO/.git" ]; then
  echo "Building shared lab git repo at $LAB_REPO..."
  mkdir -p "$LAB_REPO"
  rsync -a --exclude='.git' --exclude='results.tsv' --exclude='run.log' \
    "$HARNESS_DIR/" "$LAB_REPO/"
  git -C "$LAB_REPO" init -q
  git -C "$LAB_REPO" -c user.email="litmus@lab" -c user.name="Litmus" add -A
  git -C "$LAB_REPO" -c user.email="litmus@lab" -c user.name="Litmus" \
    commit -q -m "baseline: autoresearch harness"
  git -C "$LAB_REPO" checkout -q -b main
  echo "Lab repo ready. All agent worktrees branch from here."
  echo "  Browse all experiments later: git -C $LAB_REPO log --all --oneline --graph"
else
  echo "Lab repo already exists at $LAB_REPO"
fi

# --- Prepare training data ---
echo "Preparing training data (downloads ~1 GB on first run)..."
echo "  This may take several minutes..."
(cd "$HARNESS_DIR" && uv run prepare.py --num-shards 10)

# --- Initialise shared knowledge files ---
echo "research" > "$SHARED_DIR/mode.txt"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$SHARED_DIR/mode.txt"
echo "Created $SHARED_DIR/mode.txt (research mode)"

# Flat discovery/anomaly/moonshot files — still kept for backward compat and
# quick human reads; the notes/ subdirs are the structured layer written by agents.
if [ ! -f "$SHARED_DIR/discoveries.md" ]; then
  cat > "$SHARED_DIR/discoveries.md" << 'EOF'
# Shared Discoveries

Cross-agent knowledge base. Agents append here on new global best val_bpb.
Structured versions of each discovery are in shared/notes/discoveries/.
Read this before every experiment to avoid duplicate work.

## Baseline
val_bpb: (run baseline to establish — see shared/attempts/ for structured records)

EOF
  echo "Created $SHARED_DIR/discoveries.md"
fi

for f in anomalies.md moonshot-ideas.md paper-ideas.md midnight-reflections.md \
          watchdog-log.md morning-queue.md leisure-handoff.md; do
  if [ ! -f "$SHARED_DIR/$f" ]; then
    echo "# $f" > "$SHARED_DIR/$f"
    echo "Created $SHARED_DIR/$f"
  fi
done

# Connections map and open questions — maintained by the Synthesizer
if [ ! -f "$SHARED_DIR/notes/_connections.md" ]; then
  cat > "$SHARED_DIR/notes/_connections.md" << 'EOF'
# Knowledge Connections

Cross-category insight patterns. Updated by the Synthesizer at 04:00.
Links techniques that interact, contradict, or build on each other.

(empty until first synthesis run)
EOF
  echo "Created $SHARED_DIR/notes/_connections.md"
fi

if [ ! -f "$SHARED_DIR/notes/_open-questions.md" ]; then
  cat > "$SHARED_DIR/notes/_open-questions.md" << 'EOF'
# Open Questions

Unresolved contradictions, knowledge gaps, and hypotheses pending validation.
Updated by the Synthesizer at 04:00. Mark items [RESOLVED] when answered.

## Unresolved Contradictions
(none yet)

## Knowledge Gaps (never tested)
(none yet)

## Hypotheses Pending Validation
(none yet)

## Abandoned Directions
(none yet)
EOF
  echo "Created $SHARED_DIR/notes/_open-questions.md"
fi

# Skills index — human-readable index of the skills library
if [ ! -f "$SHARED_DIR/skills/INDEX.md" ]; then
  cat > "$SHARED_DIR/skills/INDEX.md" << 'EOF'
# Skills Library

Reusable techniques validated by experiments. Each skill file contains:
- What the technique does mechanistically
- The exact code change
- Evidence (commit hashes, val_bpb improvement)
- Conditions under which it was validated

Read ALL skill files before forming your next hypothesis — don't rediscover known wins.

## Skills
(populated by agents and the Synthesizer)
EOF
  echo "Created $SHARED_DIR/skills/INDEX.md"
fi

# Global experiment counter (read by Synthesizer to decide when to run)
if [ ! -f "$SHARED_DIR/global-experiment-count.txt" ]; then
  echo "0" > "$SHARED_DIR/global-experiment-count.txt"
fi

echo "0" > "$SHARED_DIR/watchdog-full-check.txt"

# Worker count (set by prepare-agents.sh, read by watchdog)
echo "0" > "$SHARED_DIR/worker-count.txt"

# --- Done ---
echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Ask your OpenClaw agent to start research agents (see SKILL.md)"
echo "  2. Or manually: bash $SCRIPT_DIR/prepare-agents.sh --agents 2 --templates general,general"
echo ""
echo "GPU count for agent planning: $GPU_COUNT"
echo ""
echo "Key paths:"
echo "  Lab repo (all experiment history): $LAB_REPO"
echo "  Structured attempts:               $SHARED_DIR/attempts/"
echo "  Notes (structured):                $SHARED_DIR/notes/"
echo "  Skills library:                    $SHARED_DIR/skills/"
