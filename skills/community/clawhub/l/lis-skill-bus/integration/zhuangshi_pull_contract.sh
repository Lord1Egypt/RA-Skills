#!/usr/bin/env bash
# 装饰算量接线：开工前从 lis-skill-bus 拉取 cad-contract/v1，按本专业 target
# sections 命中判定；未命中/缺字段/无 bus 一律返回 hit=false / usable=false，
# 本技能正常解析。等价：scripts 下的 zhuangshi_statesync.sh pull。
# 用法: bash zhuangshi_pull_contract.sh --project 项目 [--building 楼栋] [--floor 楼层]
set -euo pipefail
SKILL_ROOT="${SKILLS_DIR:-$HOME/.codex/skills}/zhuangshi-suanliang"
SPEC="zhuangshi"
STATESYNC="$SKILL_ROOT/scripts/${SPEC}_statesync.sh"
[[ -f "$STATESYNC" ]] || { echo "缺少 $STATESYNC（请先安装 装饰算量 skill）" >&2; exit 127; }
exec bash "$STATESYNC" pull "$@"
