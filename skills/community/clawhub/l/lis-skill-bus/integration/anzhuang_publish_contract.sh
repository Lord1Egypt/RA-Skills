#!/usr/bin/env bash
# 安装算量接线：把本技能输出契约包装成 cad-contract/v1 发布到 lis-skill-bus。
# 等价：scripts 下的 anzhuang_statesync.sh push。
# 用法: bash anzhuang_publish_contract.sh --project 项目 [--building 楼栋] [--floor 楼层] #          --entry-file <输出.json> [--specialty 安装算量]
set -euo pipefail
SKILL_ROOT="${SKILLS_DIR:-$HOME/.codex/skills}/anzhuang-suanliang"
SPEC="anzhuang"
STATESYNC="$SKILL_ROOT/scripts/${SPEC}_statesync.sh"
[[ -f "$STATESYNC" ]] || { echo "缺少 $STATESYNC（请先安装 安装算量 skill）" >&2; exit 127; }
exec bash "$STATESYNC" push "$@"
