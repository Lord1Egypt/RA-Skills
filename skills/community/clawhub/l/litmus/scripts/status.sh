#!/usr/bin/env bash
# status.sh — show experiment counts, best val_bpb per agent, and lab git tree.
# Agent liveness is tracked by OpenClaw (use `subagents action:list`).
set -euo pipefail

BASE_DIR="${LITMUS_BASE:-$HOME/.litmus}"
SHARED_DIR="$BASE_DIR/shared"
LAB_REPO="$BASE_DIR/repo"

if [ ! -d "$BASE_DIR/agents" ]; then
  echo "No agent workspaces found. Run setup.sh and prepare-agents.sh first."
  exit 1
fi

echo "=== Litmus Status ==="
echo "Base: $BASE_DIR"
echo "Time: $(date)"
echo ""

# --- Per-agent status from attempt records ---
echo "--- Agent Status (from shared/attempts/) ---"

python3 - "$SHARED_DIR" << 'EOF'
import json, glob, sys, os
from datetime import datetime, timezone, timedelta
from collections import defaultdict

shared_dir = sys.argv[1]
attempts_dir = os.path.join(shared_dir, 'attempts')

attempts = []
for f in glob.glob(os.path.join(attempts_dir, '*.json')):
    try:
        d = json.load(open(f))
        if d.get('val_bpb', 0) > 0:
            attempts.append(d)
    except: pass

if not attempts:
    print("  No attempt records yet.")
    sys.exit(0)

by_agent = defaultdict(list)
for a in attempts:
    by_agent[a['agent_id']].append(a)

now = datetime.now(timezone.utc)
print(f"  {'AGENT':<14} {'EXPS':<6} {'BEST':<10} {'WINS':<5} {'SINCE_WIN':<10} {'LAST_EXP':<8} {'STATUS'}")
print(f"  {'------':<14} {'----':<6} {'----':<10} {'----':<5} {'---------':<10} {'--------':<8} {'------'}")

for agent_id in sorted(by_agent):
    exps = sorted(by_agent[agent_id], key=lambda x: x['timestamp'])
    best = min(e['val_bpb'] for e in exps)
    wins = sum(1 for e in exps if e['status'] == 'improved')
    since_win = 0
    for e in reversed(exps):
        if e['status'] == 'improved': break
        since_win += 1
    last = exps[-1]
    last_ts = datetime.fromisoformat(last['timestamp'].replace('Z','+00:00'))
    mins_ago = int((now - last_ts).total_seconds() / 60)
    last_str = f"{mins_ago}m ago"
    stagnant = "STAGNANT" if since_win >= 12 else "active"
    slow = " SLOW" if mins_ago > 25 else ""
    print(f"  {agent_id:<14} {len(exps):<6} {best:<10.6f} {wins:<5} {since_win:<10} {last_str:<8} {stagnant}{slow}")

print()
global_best = min(a['val_bpb'] for a in attempts)
global_best_a = min(attempts, key=lambda x: x['val_bpb'])
total = len(attempts)
wins = sum(1 for a in attempts if a['status'] == 'improved')
print(f"  Global best: {global_best:.6f} by {global_best_a['agent_id']} (commit {global_best_a['commit']})")
print(f"  Total: {total} experiments, {wins} improvements ({wins/total*100:.1f}% success rate)")
EOF

echo ""

# --- Mode ---
MODE=$(cat "$SHARED_DIR/mode.txt" 2>/dev/null | head -1 || echo "unknown")
COUNT=$(cat "$SHARED_DIR/global-experiment-count.txt" 2>/dev/null || echo "?")
LAST_SYNTH=$(cat "$SHARED_DIR/last-synthesis-count.txt" 2>/dev/null || echo "?")
echo "--- System State ---"
echo "  Mode: $MODE"
echo "  Global experiment count: $COUNT"
echo "  Last synthesis at experiment: $LAST_SYNTH"
echo "  Skills in library: $(ls "$SHARED_DIR/skills/"*.md 2>/dev/null | grep -v INDEX | wc -l | tr -d ' ')"
echo "  Open anomalies: $(ls "$SHARED_DIR/notes/anomalies/"*.md 2>/dev/null | wc -l | tr -d ' ')"
echo ""

# --- Git lab tree ---
if [ -d "$LAB_REPO/.git" ]; then
  echo "--- Lab Git Tree (all agent branches) ---"
  git -C "$LAB_REPO" log --all --oneline --graph | head -30
  echo ""
  echo "  All worktrees:"
  git -C "$LAB_REPO" worktree list
fi

echo ""
echo "Tips:"
echo "  bash results.sh --top 20         — full leaderboard"
echo "  bash results.sh --agent arch-1   — single agent history"
echo "  subagents action:list             — check which agents are running (in OpenClaw)"
