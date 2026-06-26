#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <docs_repo_root> <linux_repo_path>"
  exit 1
fi

DOCS_REPO_ROOT="$1"
LINUX_REPO_PATH="$2"
BASE="$DOCS_REPO_ROOT/kernel/openclaw"

mkdir -p "$BASE/config" "$BASE/state/run_history" "$BASE/plans" "$BASE/patches" "$BASE/logs"

WF="$BASE/config/workflow.yaml"
if [[ ! -f "$WF" ]]; then
  cat > "$WF" <<YAML
project:
  linux_repo: $LINUX_REPO_PATH
  docs_repo: $DOCS_REPO_ROOT
  kvm_lore_url: https://yhbt.net/lore/kvm/

agents:
  planner:
    runtime: acp
    agentId: claude-code
    model: hanbbq/gpt-5.3-codex
  implementer:
    runtime: acp
    agentId: codex
    model: hanbbq/gpt-5.3-codex

policy:
  max_parallel_issues: 3
  max_fix_iterations: 8
  require_human_gate:
    - gate_gap_triage
    - gate_plan_review
    - gate_patch_send

issue:
  repo: zcxGGmu/linux-riscv-docs
  assignee: zcxGGmu
  labels_default: ["riscv", "kvm-gap"]

mailing:
  target_lists:
    - kvm@vger.kernel.org
    - linux-riscv@lists.infradead.org
  dry_run: true
  use_b4: true
YAML
else
  echo "Skip existing: $WF"
fi

GAP="$BASE/state/gap_registry.yaml"
if [[ ! -f "$GAP" ]]; then
  cat > "$GAP" <<'YAML'
gaps: []
YAML
fi

MAP="$BASE/state/issue_map.yaml"
if [[ ! -f "$MAP" ]]; then
  cat > "$MAP" <<'YAML'
issue_map: {}
YAML
fi

echo "Bootstrap complete: $BASE"
