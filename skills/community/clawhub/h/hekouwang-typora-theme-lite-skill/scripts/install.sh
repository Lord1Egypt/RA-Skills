#!/usr/bin/env bash
#
# hekouwang · install themes to Typora themes folder
#
# Usage:
#   ./scripts/install.sh                          # free V2；本机有 edition + 付费 CSS 时顺带装付费
#   ./scripts/install.sh --paid                   # 强制尝试安装付费 12 套（缺文件则报错）
#   ./scripts/install.sh --free-only              # 只装免费 V2
#   ./scripts/install.sh --use-local-anthropic    # additionally link Anthropic fonts (see below)
#
# 公开仓买家无 edition：仍用 SkillPay zip：
#   ./scripts/unlock.sh ~/Downloads/hekouwang-typora-theme-skill-*-paid.zip
# 购买页见 scripts/links.sh → HKW_URL_BUY
#
# ---------------------------------------------------------------------------
# ABOUT --use-local-anthropic
#
# The theme ships with Inter (SIL OFL) and looks complete without this flag.
#
# Anthropic Sans / Serif are PROPRIETARY fonts owned by Anthropic PBC. They
# carry no open license and are NOT included in this repository. This flag only
# copies files that already exist on YOUR machine (from an app you installed)
# into the theme folder, for YOUR personal use.
#
# It is OFF by default and you should leave it off unless you understand this.
# Do not redistribute the copied files. If in doubt, don't use the flag —
# the Inter fallback is what everyone else sees and it looks good.
# ---------------------------------------------------------------------------
#
# Design notes (learned the hard way):
#   - No automatic backups: this installer overwrites in place. Keep your own
#     copy if you need one; never leave backup CSS in the themes root, because
#     Typora lists it as a selectable theme — including dotfiles.
#   - After the first destructive action, warn instead of aborting. Never leave
#     someone in a half-installed state.
#   - Idempotent: running it twice produces the same result.
#
set -uo pipefail

SLUG="hekouwang"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
. "$SRC_DIR/scripts/links.sh"
THEME_DIR="$HOME/Library/Application Support/abnerworks.Typora/themes"
USE_LOCAL_ANTHROPIC=0
MODE="auto"   # auto | paid | free-only

PAID_VARIANTS=(
  hekouwang-v1 hekouwang-v1-dark
  hekouwang-v2-pro hekouwang-v2-pro-dark
  hekouwang-v3 hekouwang-v3-dark
  hekouwang-v4 hekouwang-v4-dark
  hekouwang-v5 hekouwang-v5-dark
  hekouwang-v6 hekouwang-v6-dark
)

for arg in "$@"; do
  case "$arg" in
    --use-local-anthropic) USE_LOCAL_ANTHROPIC=1 ;;
    --paid) MODE="paid" ;;
    --free-only) MODE="free-only" ;;
    -h|--help) sed -n '2,30p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 1 ;;
  esac
done

ok()   { printf '  ✅ %s\n' "$*"; }
warn() { printf '  ⚠️  %s\n' "$*"; }

should_install_paid=0
case "$MODE" in
  paid) should_install_paid=1 ;;
  free-only) should_install_paid=0 ;;
  auto)
    if [ -d "$SRC_DIR/edition" ] && [ -f "$SRC_DIR/theme/hekouwang-v1.css" ]; then
      should_install_paid=1
    fi
    ;;
esac

if [ "$should_install_paid" -eq 1 ]; then
  echo "hekouwang · install (free V2 + paid V1–V6)"
else
  echo "hekouwang · install (free · V2)"
fi
echo "────────────────────────────────────────"

# ---- preflight (safe to abort: nothing touched yet) ----
if [ ! -d "$THEME_DIR" ]; then
  echo "Typora themes folder not found: $THEME_DIR" >&2
  echo "Install Typora first, or check the path via Preferences → Open Theme Folder." >&2
  exit 1
fi
if [ ! -f "$SRC_DIR/theme/$SLUG.css" ]; then
  echo "Missing $SRC_DIR/theme/$SLUG.css — run: python3 scripts/build.py --tier free" >&2
  exit 1
fi
if [ "$should_install_paid" -eq 1 ]; then
  missing=0
  for variant in "${PAID_VARIANTS[@]}"; do
    if [ ! -f "$SRC_DIR/theme/$variant.css" ]; then
      warn "missing theme/$variant.css"
      missing=1
    fi
  done
  if [ "$missing" -ne 0 ]; then
    echo "付费 CSS 不齐 —— 先 python3 scripts/build.py（需 edition/），或改用 --free-only" >&2
    exit 1
  fi
fi

VARIANTS=(
  "$SLUG" "$SLUG-dark"
)
LEGACY_REMOVE=(
  "$SLUG-claude"
  "$SLUG-claude-dark"
)

# ---- theme css（免费 V2） ----
for variant in "${VARIANTS[@]}"; do
  src="$SRC_DIR/theme/$variant.css"
  [ -f "$src" ] || continue
  if cp "$src" "$THEME_DIR/$variant.css" 2>/dev/null; then
    ok "installed $variant.css"
  else
    warn "failed to copy $variant.css — check folder permissions"
  fi
done

# ---- paid V1–V6（本机 edition 或 --paid）----
if [ "$should_install_paid" -eq 1 ]; then
  for variant in "${PAID_VARIANTS[@]}"; do
    src="$SRC_DIR/theme/$variant.css"
    if cp "$src" "$THEME_DIR/$variant.css" 2>/dev/null; then
      ok "installed $variant.css"
    else
      warn "failed to copy $variant.css — check folder permissions"
    fi
  done
fi

for variant in "${LEGACY_REMOVE[@]}"; do
  if [ -f "$THEME_DIR/$variant.css" ]; then
    rm -f "$THEME_DIR/$variant.css" 2>/dev/null \
      && ok "removed legacy $variant.css from Themes menu" \
      || warn "could not remove legacy $variant.css"
  fi
done

# ---- bundled fonts (Inter, OFL — everyone gets these) ----
mkdir -p "$THEME_DIR/$SLUG/fonts" 2>/dev/null || warn "could not create resource folder"
n=0
for f in "$SRC_DIR/theme/$SLUG/fonts"/*; do
  [ -f "$f" ] || continue
  cp "$f" "$THEME_DIR/$SLUG/fonts/" 2>/dev/null && n=$((n+1))
done
[ "$n" -gt 0 ] && ok "installed $n bundled font files (Inter, SIL OFL)" \
               || warn "no bundled fonts copied — Latin text falls back to system fonts"

# ---- optional: local Anthropic fonts (opt-in, see header) ----
if [ "$USE_LOCAL_ANTHROPIC" -eq 1 ]; then
  FONT_SRC="/Applications/Claude.app/Contents/Resources/fonts"
  mkdir -p "$THEME_DIR/$SLUG/fonts-local" 2>/dev/null
  m=0
  if [ -d "$FONT_SRC" ]; then
    for f in "$FONT_SRC"/AnthropicSans-*.ttf \
             "$FONT_SRC"/AnthropicSerif-*.ttf; do
      [ -f "$f" ] || continue
      cp "$f" "$THEME_DIR/$SLUG/fonts-local/" 2>/dev/null && m=$((m+1))
    done
  fi
  if [ "$m" -gt 0 ]; then
    ok "linked $m local Anthropic font files (personal use only — do not redistribute)"
  else
    warn "Claude desktop app not found — skipping; the Inter fallback is used instead"
  fi
fi

echo "────────────────────────────────────────"
echo "  Done. Quit Typora completely (Cmd+Q) and reopen."
echo "  Themes menu · Free："
echo "    • Hekouwang / Hekouwang Dark   （skill V2 编辑）"
if [ "$should_install_paid" -eq 1 ]; then
  echo "  Themes menu · Paid："
  echo "    • Hekouwang V1–V6 / V2 Pro（浅 + 深，共 12 项）"
else
  echo
  echo "  Pack · V1 / V2 Pro / V3–V6（¥9.9）："
  echo "    ${HKW_URL_SKILLPAY:-$HKW_URL_BUY}"
  echo "    买完：./scripts/unlock.sh ~/Downloads/hekouwang-typora-theme-skill-*-paid.zip"
fi
echo
echo "  Note: switching themes does NOT reload a modified CSS file."
echo "  You must fully quit and relaunch Typora."
