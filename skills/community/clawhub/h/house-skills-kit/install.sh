#!/usr/bin/env bash
# ============================================================
# house-skills-kit 安装器
# 用法: bash install.sh <SKILL_DIR> [AGENT_HOME]
#   SKILL_DIR  渲染产物目录(含 SKILL.md + manifest.json)
#   AGENT_HOME 可选；不传则自动探测常见 Agent 目录
# 特性(参照社区分发最佳实践):
#   - manifest.json 校验(完整性)
#   - 多 Agent 目录探测(Hermes/OpenClaw/自定义)
#   - 安装后 sha256 记录,便于升级比对
# ============================================================
set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="${1:-}"
AGENT_HOME="${2:-}"

if [[ -z "$SKILL_DIR" ]]; then
  echo "用法: bash install.sh <SKILL_DIR> [AGENT_HOME]"
  echo "  SKILL_DIR: 先运行 python3 render.py 生成,如 output/kunming-buy"
  exit 1
fi

if [[ ! -f "$SKILL_DIR/SKILL.md" || ! -f "$SKILL_DIR/manifest.json" ]]; then
  echo "[x] $SKILL_DIR 缺少 SKILL.md 或 manifest.json — 请先运行 render.py"
  exit 1
fi

# ---------- 路径护栏(安全:限定仓库内产物) ----------
SKILL_DIR_REAL="$(cd "$SKILL_DIR" && pwd)"
case "$SKILL_DIR_REAL" in
  "$KIT_DIR"|"$KIT_DIR"/*) : ;;  # 仓库内,放行
  *) echo "[x] 安全限制: SKILL_DIR 必须位于仓库目录内(如 output/*),不接受外部路径"; exit 1 ;;
esac

# ---------- 多 Agent 目录探测 ----------
detect_agent_home() {
  # 1) 显式传入(安全:仅接受 $HOME 下的路径)
  if [[ -n "$AGENT_HOME" ]]; then
    case "$AGENT_HOME" in
      "$HOME"|"$HOME"/*) echo "$AGENT_HOME"; return 0 ;;
      *) echo "[x] 安全限制: 安装目标仅允许 \$HOME 下的目录" >&2; return 1 ;;
    esac
  fi
  # 2) 环境变量(兼容常见约定;安全:仅接受 $HOME 下的路径)
  for v in HERMES_HOME OPENCLAW_HOME AGENT_HOME; do
    val="${!v:-}"
    if [[ -n "$val" && -d "$val" ]]; then
      case "$val" in
        "$HOME"|"$HOME"/*) echo "$val/skills"; return 0 ;;
        *) : ;;  # 非 $HOME 下的环境变量路径,跳过不采用
      esac
    fi
  done
  # 3) 常见路径探测
  local candidates=(
    "$HOME/.hermes/skills"
    "$HOME/.openclaw/skills"
    "$HOME/.claude/skills"
    "$HOME/.codex/skills"
  )
  for c in "${candidates[@]}"; do
    if [[ -d "$c" ]]; then echo "$c"; return 0; fi
  done
  # 4) 都没有 → 提示手动指定
  echo "" 
  return 1
}

TARGET_ROOT="$(detect_agent_home || true)"
if [[ -z "$TARGET_ROOT" ]]; then
  echo "[!] 未探测到 Agent 技能目录。请指定安装位置,例如:"
  echo "    bash install.sh $SKILL_DIR ~/.hermes/skills"
  exit 1
fi

SKILL_NAME="$(basename "$SKILL_DIR")"
TARGET_DIR="$TARGET_ROOT/$SKILL_NAME"

echo "[i] 安装 $SKILL_NAME → $TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -r "$SKILL_DIR/." "$TARGET_DIR/"

# ---------- 完整性校验 ----------
python3 - "$TARGET_DIR" <<'PYEOF'
import json, sys, os, hashlib
d = sys.argv[1]
m = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
required = ["name", "version", "entry"]
missing = [k for k in required if k not in m]
if missing:
    print(f"[x] manifest 缺字段: {missing}"); sys.exit(1)
skill_file = os.path.join(d, m["entry"])
h = hashlib.sha256(open(skill_file, "rb").read()).hexdigest()
rec = os.path.join(d, ".sha256")
open(rec, "w").write(h + "\n")
print(f"[ok] {m['name']} v{m['version']} 安装完成 (sha256 {h[:16]}...)")
PYEOF

echo "[i] 完成。重启你的 Agent 后,技能即可被识别。"
