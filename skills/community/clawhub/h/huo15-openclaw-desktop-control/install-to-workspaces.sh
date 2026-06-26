#!/usr/bin/env bash
# install-to-workspaces.sh
#
# 把 huo15-openclaw-desktop-control skill 装到 OpenClaw 所有 workspace 的
# 真正 skills root（双层 skills/skills/）。
#
# 这个 skill 没有 npm 依赖，只是 SKILL.md + _meta.json + .clawhub/origin.json，
# 走 cp 实体（不 symlink，因为 OpenClaw safety filter 拒绝 escape symlink）。
# 重跑可同步最新仓库内容。

set -euo pipefail

SKILL_SRC="$(cd "$(dirname "$0")" && pwd)"
SKILL_NAME="huo15-openclaw-desktop-control"

if [[ ! -f "$SKILL_SRC/SKILL.md" ]]; then
  echo "❌ 找不到 $SKILL_SRC/SKILL.md" >&2
  exit 1
fi
if [[ ! -f "$SKILL_SRC/_meta.json" ]]; then
  echo "❌ 找不到 $SKILL_SRC/_meta.json" >&2
  exit 1
fi

OPENCLAW_HOME="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
if [[ ! -d "$OPENCLAW_HOME" ]]; then
  echo "❌ OpenClaw 未安装：$OPENCLAW_HOME 不存在" >&2
  exit 1
fi

VERSION=$(grep -E '^version:' "$SKILL_SRC/SKILL.md" | head -1 | awk '{print $2}')
NOW_MS=$(python3 -c "import time; print(int(time.time()*1000))")

install_into_skills_root() {
  local ws="$1"
  local outer="$ws/skills"
  local inner="$ws/skills/skills"

  mkdir -p "$inner"
  local target="$inner/$SKILL_NAME"

  # 清掉错位置残留（outer/<slug>/，单层）
  if [[ -e "$outer/$SKILL_NAME" && "$outer/$SKILL_NAME" != "$inner" ]]; then
    rm -rf "$outer/$SKILL_NAME"
    echo "  🗑  cleared stale: $outer/$SKILL_NAME"
  fi

  rm -rf "$target"
  mkdir -p "$target/.clawhub"
  cp "$SKILL_SRC/SKILL.md" "$target/SKILL.md"
  cp "$SKILL_SRC/_meta.json" "$target/_meta.json"
  cat > "$target/.clawhub/origin.json" <<EOF
{"version":1,"registry":"local","slug":"$SKILL_NAME","installedVersion":"$VERSION","installedAt":$NOW_MS}
EOF
  chmod -R go-rwx "$target" 2>/dev/null || true
  echo "  ✅ installed: $target"
}

count=0
processed=()
shopt -s nullglob
echo "=== auto-discover OpenClaw workspaces ==="
for ws in "$OPENCLAW_HOME"/workspace "$OPENCLAW_HOME"/workspace-*/; do
  [[ -d "${ws%/}" ]] || continue
  ws="${ws%/}"
  if [[ " ${processed[*]:-} " == *" $ws "* ]]; then continue; fi
  processed+=("$ws")
  install_into_skills_root "$ws"
  count=$((count + 1))
done
shopt -u nullglob

echo ""
echo "✅ Installed $SKILL_NAME v$VERSION → $count workspaces"
echo ""
echo "下一步："
echo "  • 验证识别：openclaw skills info $SKILL_NAME"
echo "  • OpenClaw 新会话里说「火一五桌控 / 桌控 / 帮我点 / 看下屏幕」测试 trigger"
