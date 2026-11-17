#!/usr/bin/env bash
# 钢结构算量接线：吨位估算带落盘后包装成 cad-contract/v1 发到 lis-skill-bus；
# 缺 bus 时退出码 2，不降级为本地状态。等价：scripts 下的 gangjiegou_statesync.sh push。
# 用法: bash gangjiegou_publish_contract.sh --entry-file 输出.json --project 项目 [--building 楼栋] [--floor 楼层]
set -euo pipefail
SKILL_ROOT="${SKILLS_DIR:-$HOME/.codex/skills}/gangjiegou-suanliang"
SPEC="gangjiegou"
STATESYNC="$SKILL_ROOT/scripts/${SPEC}_statesync.sh"
[[ -f "$STATESYNC" ]] || { echo "缺少 $STATESYNC（请先安装 钢结构算量 skill）" >&2; exit 127; }
exec bash "$STATESYNC" push "$@"
