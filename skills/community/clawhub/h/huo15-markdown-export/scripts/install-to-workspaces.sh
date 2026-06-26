#!/usr/bin/env bash
# install-to-workspaces.sh
#
# 把本 skill 装到 OpenClaw 所有 workspace 的真实双层 skills root,治本两个坑:
#
# 坑 1: ClawHub install 装到单层 workspace/skills/<slug>/,但 OpenClaw loader 实扫双层
#       workspace/skills/skills/<slug>/。装错位置 → skill list 看不见,info 报 not found。
# 坑 2: 多 wecom 群每群一个独立 workspace,group context 下默认看不到 default workspace
#       的 skill。需要 cp 实体到每个 workspace。
#
# 参考:cc-media-bridge/skill/install-to-workspaces.sh
# Memory: ~/.claude/projects/-Users-jobzhao/memory/feedback_openclaw_skill_install_pitfalls.md
#
# 关键差异 vs cc-media-bridge:本 skill 体积大(node_modules ≈ 200MB)。
# 策略:skill 文件实体 cp,**node_modules 用 symlink 指向 default workspace**。
#   - 30 workspace × 实体复制全 ≈ 6GB(不可接受)
#   - skill 文件 1MB × 30 + 一份 node_modules 200MB ≈ 230MB ✓
#   - OpenClaw safety filter 只检查 SKILL.md realpath,node_modules 不被扫,symlink 安全
#
# 用法:
#   bash scripts/install-to-workspaces.sh                    # 装到所有 workspace
#   bash scripts/install-to-workspaces.sh --dry-run          # 列出会装的位置不真做
#   bash scripts/install-to-workspaces.sh --skip-default     # 已装好 default 的话,只补其他 workspace

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$(dirname "$SCRIPT_DIR")"
SLUG="huo15-markdown-export"

DRY_RUN=0
SKIP_DEFAULT=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --skip-default) SKIP_DEFAULT=1; shift ;;
    -h|--help) sed -n '3,28p' "$0"; exit 0 ;;
    *) echo "未知选项: $1" >&2; exit 1 ;;
  esac
done

OPENCLAW_HOME="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
[[ -d "$OPENCLAW_HOME" ]] || { echo "× OpenClaw 未安装: $OPENCLAW_HOME 不存在" >&2; exit 1; }

[[ -f "$SKILL_SRC/SKILL.md" ]] || { echo "× $SKILL_SRC/SKILL.md 缺失" >&2; exit 1; }

VERSION=$(grep -E '^version:' "$SKILL_SRC/SKILL.md" | head -1 | awk '{print $2}')
NOW_MS=$(python3 -c "import time; print(int(time.time()*1000))")

DEFAULT_TARGET="$OPENCLAW_HOME/workspace/skills/skills/$SLUG"
DEFAULT_NM="$DEFAULT_TARGET/node_modules"

echo "→ skill 源:           $SKILL_SRC (v$VERSION)"
echo "→ default 目标:       $DEFAULT_TARGET"
echo "→ node_modules 主源:  $DEFAULT_NM"
[[ $DRY_RUN -eq 1 ]] && echo "→ DRY-RUN(只列目标,不写文件)"
echo

# 1) 装 default workspace —— 它持有真实 node_modules,后续 workspace 用 symlink 指它
install_default_workspace() {
  local target="$DEFAULT_TARGET"
  local outer="$OPENCLAW_HOME/workspace/skills"

  echo "=== default workspace ==="
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "  [dry] 会装:$target"
    return 0
  fi

  # 清单层幽灵(workspace/skills/<slug>)
  if [[ -e "$outer/$SLUG" && "$outer/$SLUG" != "$target" ]]; then
    rm -rf "$outer/$SLUG"
    echo "  🗑 cleared stale single-layer: $outer/$SLUG"
  fi

  mkdir -p "$target"
  # 用 rsync 增量更新(保留已存在的 node_modules)
  rsync -a --delete \
    --exclude='node_modules' --exclude='.git' --exclude='.gitignore' \
    --exclude='examples/*.pdf' --exclude='examples/*.png' \
    --exclude='examples/*.html' --exclude='examples/*.docx' \
    --exclude='examples/*.wechat.html' \
    "$SKILL_SRC/" "$target/"

  mkdir -p "$target/.clawhub"
  cat > "$target/.clawhub/origin.json" <<EOF
{"version":1,"registry":"https://clawhub.ai","slug":"$SLUG","installedVersion":"$VERSION","installedAt":$NOW_MS}
EOF

  # node_modules 必须实体存在;不存在则提示装
  if [[ ! -d "$DEFAULT_NM" ]]; then
    echo "  ⚠ node_modules 不存在,跑 install-deps.sh 装齐..."
    ( cd "$target" && bash scripts/install-deps.sh >&2 )
  fi

  echo "  ✓ installed: $target"
}

# 2) 其他 workspace —— skill 文件实体 cp,node_modules symlink 指向 default
install_into_workspace() {
  local ws="$1"
  local outer="$ws/skills"
  local inner="$ws/skills/skills"
  local target="$inner/$SLUG"

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "  [dry] 会装:$target"
    return 0
  fi

  mkdir -p "$inner"

  # 清单层幽灵
  if [[ -e "$outer/$SLUG" && "$outer/$SLUG" != "$target" ]]; then
    rm -rf "$outer/$SLUG"
    echo "  🗑 cleared stale: $outer/$SLUG"
  fi

  # 实体复制 skill 文件(不含 node_modules)
  rm -rf "$target"
  mkdir -p "$target"
  rsync -a \
    --exclude='node_modules' --exclude='.git' --exclude='.gitignore' \
    --exclude='examples/*.pdf' --exclude='examples/*.png' \
    --exclude='examples/*.html' --exclude='examples/*.docx' \
    --exclude='examples/*.wechat.html' \
    "$SKILL_SRC/" "$target/"

  mkdir -p "$target/.clawhub"
  cat > "$target/.clawhub/origin.json" <<EOF
{"version":1,"registry":"https://clawhub.ai","slug":"$SLUG","installedVersion":"$VERSION","installedAt":$NOW_MS}
EOF

  # node_modules 用 symlink 指向 default workspace —— 节省磁盘 6GB → 230MB
  ln -sf "$DEFAULT_NM" "$target/node_modules"

  echo "  ✓ installed: $target  (nm → default)"
}

count=0

if [[ $SKIP_DEFAULT -eq 0 ]]; then
  install_default_workspace
  count=$((count + 1))
else
  echo "=== 跳过 default workspace(--skip-default)"
fi

echo
echo "=== wecom 群 workspaces ==="
shopt -s nullglob
for ws in "$OPENCLAW_HOME"/workspace-wecom-*/; do
  [[ -d "$ws" ]] || continue
  install_into_workspace "${ws%/}"
  count=$((count + 1))
done

echo
echo "=== 其他 workspace-* / agents/wecom-* ==="
for ws in "$OPENCLAW_HOME"/workspace-agent-*/ "$OPENCLAW_HOME"/agents/wecom-*/; do
  [[ -d "$ws" ]] || continue
  case "$ws" in
    */workspace/|*/workspace-wecom-*) continue ;;  # 已处理
  esac
  install_into_workspace "${ws%/}"
  count=$((count + 1))
done
shopt -u nullglob

echo
echo "✓ Installed $SLUG v$VERSION → $count workspaces"
echo
echo "下一步:"
echo "  • 验证识别:  openclaw skills info $SLUG"
echo "  • 在 wecom 群对话说: '把这份 md 导出 PDF 发我' 测试 trigger"
[[ $DRY_RUN -eq 1 ]] && echo "  ⚠ 这次是 dry-run,实际未写;去掉 --dry-run 重跑"
