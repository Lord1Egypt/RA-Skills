#!/usr/bin/env bash
set -euo pipefail

WS="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"

"$WS/scripts/memory_consolidate.py"

SNAP="$WS/MEMORY_SNAPSHOT.md"
RULE_SNAP="$WS/MEMORY_SNAPSHOT.rule.md"
SEM_SNAP="$WS/MEMORY_SNAPSHOT.semantic.md"
FACTS="$WS/memory/structured/facts.jsonl"
BELIEFS="$WS/memory/structured/beliefs.jsonl"
SUM="$WS/memory/structured/summaries.jsonl"
EVENTS="$WS/memory/structured/events.jsonl"
HEALTH="$WS/memory/structured/health.json"
CANDIDATES="$WS/memory/structured/candidates/latest.json"
SEMANTIC="$WS/memory/structured/semantic/latest.json"
SEM_PIPELINE="$WS/memory/structured/semantic/pipeline_status.json"

bytes=$(wc -c < "$SNAP" | tr -d ' ')
rule_bytes=0
sem_bytes=0
if [ -f "$RULE_SNAP" ]; then
  rule_bytes=$(wc -c < "$RULE_SNAP" | tr -d ' ')
fi
if [ -f "$SEM_SNAP" ]; then
  sem_bytes=$(wc -c < "$SEM_SNAP" | tr -d ' ')
fi
fc=$(grep -c '^{' "$FACTS" 2>/dev/null || true)
bc=$(grep -c '^{' "$BELIEFS" 2>/dev/null || true)
sc=$(grep -c '^{' "$SUM" 2>/dev/null || true)
ec=$(grep -c '^{' "$EVENTS" 2>/dev/null || true)

echo "MEMORY_SNAPSHOT.md (default): ${bytes} bytes"
if [ -f "$RULE_SNAP" ]; then
  echo "MEMORY_SNAPSHOT.rule.md (rule backup): ${rule_bytes} bytes"
fi
if [ -f "$SEM_SNAP" ]; then
  echo "MEMORY_SNAPSHOT.semantic.md (semantic alias): ${sem_bytes} bytes"
  if cmp -s "$SNAP" "$SEM_SNAP"; then
    echo "default_vs_semantic: identical"
  else
    echo "default_vs_semantic: different"
  fi
fi
if [ -f "$RULE_SNAP" ]; then
  if cmp -s "$SNAP" "$RULE_SNAP"; then
    echo "default_vs_rule: identical"
  else
    echo "default_vs_rule: different"
  fi
fi
echo "facts: ${fc}"
echo "beliefs: ${bc}"
echo "summaries: ${sc}"
echo "events: ${ec}"

if [ -f "$CANDIDATES" ] || [ -f "$SEMANTIC" ] || [ -f "$SEM_PIPELINE" ]; then
  python3 - "$CANDIDATES" "$SEMANTIC" "$SEM_PIPELINE" <<'PY'
import json, os, sys
cand_path, semantic_path, pipeline_path = sys.argv[1:4]
if cand_path and cand_path != '-' and os.path.exists(cand_path):
    with open(cand_path, 'r', encoding='utf-8') as f:
        cand = json.load(f)
    print('semantic_candidates:')
    for key, value in (cand.get('counts') or {}).items():
        print(f'  {key}: {int(value)}')
if semantic_path and semantic_path != '-' and os.path.exists(semantic_path):
    with open(semantic_path, 'r', encoding='utf-8') as f:
        sem = json.load(f)
    print('semantic_output:')
    for key, value in (sem.get('counts') or {}).items():
        print(f'  {key}: {int(value)}')
if pipeline_path and pipeline_path != '-' and os.path.exists(pipeline_path):
    with open(pipeline_path, 'r', encoding='utf-8') as f:
        status = json.load(f)
    print(f"semantic_pipeline_status: {status.get('status', 'unknown')}")
    print(f"semantic_default_source: {status.get('default_source', 'unknown')}")
    print(f"semantic_snapshots_ready: default={bool(status.get('default_ready'))}, rule={bool(status.get('rule_ready'))}, semantic={bool(status.get('semantic_ready'))}")
PY
fi

if [ -f "$HEALTH" ]; then
  python3 - "$HEALTH" <<'PY'
import json, sys
p = sys.argv[1]
with open(p, 'r', encoding='utf-8') as f:
    h = json.load(f)
print("memory_health:")
print(f"  active_total: {int(h.get('active_total', 0))}")
print(f"  archived_total: {int(h.get('archived_total', 0))}")
print(f"  archive_ratio: {float(h.get('archive_ratio', 0.0)):.4f}")
print(f"  temperature: hot={int(h.get('hot', 0))}, warm={int(h.get('warm', 0))}, cold={int(h.get('cold', 0))}")
print(f"  reinforced_count: {int(h.get('reinforced_count', 0))}")
print(f"  distilled_count: {int(h.get('distilled_count', 0))}")
print(f"  signal_noise_ratio: {float(h.get('signal_noise_ratio', 0.0)):.3f}")
PY
fi

python3 "$WS/scripts/memory_consolidate_observe.py"
