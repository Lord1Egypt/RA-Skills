#!/usr/bin/env bash
# results.sh — cross-agent experiment leaderboard from shared/attempts/ JSON records.
set -euo pipefail

BASE_DIR="${LITMUS_BASE:-$HOME/.litmus}"
SHARED_DIR="$BASE_DIR/shared"
TOP_N=10
FILTER_AGENT=""
FILTER_FOCUS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --top)    TOP_N="$2";       shift 2 ;;
    --agent)  FILTER_AGENT="$2"; shift 2 ;;
    --focus)  FILTER_FOCUS="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

ATTEMPTS_DIR="$SHARED_DIR/attempts"

if [ ! -d "$ATTEMPTS_DIR" ] || [ -z "$(ls -A "$ATTEMPTS_DIR" 2>/dev/null)" ]; then
  echo "No attempt records yet. Agents write to $ATTEMPTS_DIR after each experiment."
  echo "(Tip: run setup.sh and prepare-agents.sh first)"
  exit 0
fi

python3 - "$ATTEMPTS_DIR" "$TOP_N" "$FILTER_AGENT" "$FILTER_FOCUS" << 'EOF'
import json, glob, sys, os
from datetime import datetime, timezone, timedelta

attempts_dir, top_n_str, filter_agent, filter_focus = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
top_n = int(top_n_str)

attempts = []
for f in glob.glob(os.path.join(attempts_dir, '*.json')):
    try:
        d = json.load(open(f))
        if d.get('val_bpb', 0) > 0:
            if filter_agent and d.get('agent_id') != filter_agent:
                continue
            if filter_focus and d.get('focus_area') != filter_focus:
                continue
            attempts.append(d)
    except:
        pass

if not attempts:
    print("No completed experiments match the filter.")
    sys.exit(0)

# Sort by val_bpb ascending (lower is better)
attempts.sort(key=lambda x: x['val_bpb'])

print(f"=== Litmus Leaderboard (top {top_n}) ===")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
if filter_agent: print(f"Filter: agent={filter_agent}")
if filter_focus: print(f"Filter: focus={filter_focus}")
print()

print(f"{'RANK':<4}  {'AGENT':<12}  {'COMMIT':<8}  {'val_bpb':<10}  {'STATUS':<14}  {'MFU%':<5}  TITLE")
print(f"{'----':<4}  {'------------':<12}  {'--------':<8}  {'----------':<10}  {'--------------':<14}  {'-----':<5}  -----")

for i, a in enumerate(attempts[:top_n], 1):
    mfu = f"{a.get('mfu_percent', 0):.1f}" if a.get('mfu_percent') else "-"
    title = a.get('title', '')[:45]
    print(f"{i:<4}  {a['agent_id']:<12}  {a['commit']:<8}  {a['val_bpb']:<10.6f}  {a['status']:<14}  {mfu:<5}  {title}")

print()

# Statistics
now = datetime.now(timezone.utc)
last_24h = now - timedelta(hours=24)
recent = [a for a in attempts
          if datetime.fromisoformat(a['timestamp'].replace('Z','+00:00')) > last_24h]

total = len(attempts)
improved = sum(1 for a in attempts if a['status'] == 'improved')
agents = set(a['agent_id'] for a in attempts)

print(f"Total experiments: {total}  |  Improvements: {improved} ({improved/total*100:.1f}%)  |  Agents: {len(agents)}")
if recent:
    r_improved = sum(1 for a in recent if a['status'] == 'improved')
    print(f"Last 24h: {len(recent)} experiments, {r_improved} improvements ({r_improved/len(recent)*100:.1f}% rate)")

print()

# Per-agent summary
print("=== Per-Agent Summary ===")
from collections import defaultdict
by_agent = defaultdict(list)
for a in attempts:
    by_agent[a['agent_id']].append(a)

for agent_id in sorted(by_agent):
    exps = by_agent[agent_id]
    best = min(e['val_bpb'] for e in exps)
    imp = sum(1 for e in exps if e['status'] == 'improved')
    since_imp = 0
    for e in sorted(exps, key=lambda x: x['timestamp'], reverse=True):
        if e['status'] == 'improved':
            break
        since_imp += 1
    focus = exps[-1].get('focus_area', '?') if exps else '?'
    stagnant = ' [STAGNANT]' if since_imp >= 12 else ''
    print(f"  {agent_id:<12}  best={best:.6f}  {len(exps)} exps  {imp} wins  {since_imp} since last win  focus={focus}{stagnant}")

print()

# Skills library summary
skills_dir = os.path.join(os.path.dirname(attempts_dir), 'skills')
if os.path.exists(skills_dir):
    skill_files = [f for f in os.listdir(skills_dir) if f.endswith('.md') and f != 'INDEX.md']
    print(f"Skills library: {len(skill_files)} validated technique(s)")
    for sf in sorted(skill_files):
        print(f"  - {sf}")
EOF
