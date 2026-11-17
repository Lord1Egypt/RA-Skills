#!/usr/bin/env bash
# 钢结构算量接线：开工前从 lis-skill-bus 拉取 cad-file-reader 产出的
# cad-contract/v1，按本专业 target sections 命中判定；缺 bus 时退出码 2，
# 不降级为本地识图。等价：scripts 下的 gangjiegou_statesync.sh pull。
# 用法: bash gangjiegou_pull_contract.sh --project 项目 [--building 楼栋] [--floor 楼层]
set -euo pipefail
SKILL_ROOT="${SKILLS_DIR:-$HOME/.codex/skills}/gangjiegou-suanliang"
SPEC="gangjiegou"
STATESYNC="$SKILL_ROOT/scripts/${SPEC}_statesync.sh"
[[ -f "$STATESYNC" ]] || { echo "缺少 $STATESYNC（请先安装 钢结构算量 skill）" >&2; exit 127; }
exec bash "$STATESYNC" pull "$@"
