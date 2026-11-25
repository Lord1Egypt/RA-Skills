#!/bin/bash
# ============================================================
# hekouwang-terminal-skill — 更新到最新版
#
# 用法:
#   ./scripts/update.sh              拉更新 → 重新生成主题 → 重新部署当前主题
#   ./scripts/update.sh --check      只看有没有新版本和更了什么，不动任何东西
#
# 为什么要有这个脚本：以前「更新」= 群里发个新压缩包、你自己重下重装，
# 既不知道自己是不是最新版，也不知道这次更了啥。这个脚本两件事都回答。
#
# 它不碰你的 ~/.zshrc.local、不碰你自己改过的 GUI 设置；
# 只重新生成主题文件、重新部署当前正在用的那套。
# ============================================================
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/i18n.sh"
hkw_i18n_init update "$@"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/aliases.sh"
eval set -- "$HKW_ARGS"
RUNTIME="$HOME/.config/hekouwang-terminal"
CHECK=0
case "${1:-}" in
  --check|-c) CHECK=1 ;;
  -h|--help) blk_update_help; exit 0 ;;
esac

g='\033[1;32m'; y='\033[1;33m'; b='\033[1;34m'; d='\033[2m'; o='\033[0m'
say() { printf "\n${b}%s${o}\n" "$(t "$@")"; }

cd "$SCRIPT_DIR"

# 版本号真相源＝仓根的 VERSION（两档都发）。
# ⛔ 别改回读 SKILL.md：那份从 2.4.0 起归付费档（Claude Code Skill 是付费能力），
#    免费版根本没有这个文件 —— 读不到只会安静地打「版本未知」，零报错。
CUR_VER="$(tr -d '[:space:]' < VERSION 2>/dev/null)"
printf "${b}%s${o}\n" "$(t M_UP_HEAD)"
printf "${d}%s${o}\n" "$(t M_UP_CURRENT "${CUR_VER:-$(t M_UP_UNKNOWN)}")"

# ---- 1. 有没有新版本 ----
if [ ! -d .git ]; then
  printf "\n${y}%s${o}\n" "$(t M_UP_NOT_GIT)"
  printf "%s\n" "$(t M_UP_NOT_GIT_1)"
  printf "${d}%s${o}\n" "$(t M_UP_NOT_GIT_2)"
  exit 0
fi

say M_UP_S1
if ! git fetch --quiet 2>/dev/null; then
  printf "  ${y}%s${o}\n" "$(t M_UP_NO_NET)"
  exit 0
fi
LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse '@{u}' 2>/dev/null || echo "$LOCAL")"
if [ "$LOCAL" = "$REMOTE" ]; then
  printf "  ${g}%s${o}\n" "$(t M_UP_UP_TO_DATE)"
  exit 0
fi
N="$(git rev-list --count HEAD.."$REMOTE" 2>/dev/null || echo '?')"
printf "  ${y}%s${o}\n" "$(t M_UP_N_COMMITS "$N")"

say M_UP_S2
git log --oneline --no-decorate HEAD.."$REMOTE" 2>/dev/null | head -20 | sed 's/^/  /'
# CHANGELOG 的新增部分最直观，有就一并打出来
if git diff HEAD.."$REMOTE" -- CHANGELOG.md 2>/dev/null | grep -q '^+'; then
  printf "\n  ${d}%s${o}\n" "$(t M_UP_CHANGELOG)"
  git diff HEAD.."$REMOTE" -- CHANGELOG.md | grep '^+' | grep -v '^+++' \
    | sed 's/^+//' | head -25 | sed 's/^/  /'
fi

if [ "$CHECK" = "1" ]; then
  printf "\n${y}%s${o}\n" "$(t M_UP_CHECK_ONLY)"
  exit 0
fi

# ---- 3. 本地有没有改动会被冲掉 ----
say M_UP_S3
if ! git diff --quiet || ! git diff --cached --quiet; then
  printf "  ${y}%s${o}\n" "$(t M_UP_DIRTY)"
  git status --short | sed 's/^/    /'
  printf "  ${y}?${o} %s [Y/n] " "$(t M_UP_ASK_STASH)"
  read -r a </dev/tty || a="y"
  if [[ "${a:-y}" =~ ^[Nn] ]]; then
    printf "  %s\n" "$(t M_UP_ABORTED)"; exit 1
  fi
  git stash push -u -m "$(t M_UP_STASH_MSG "$(date '+%F %T')")" >/dev/null
  printf "  ${g}%s${o}\n" "$(t M_UP_STASHED)"
fi

# ⚠️ palettes/brand.py 是付费包、在开源仓的 .gitignore 里，pull 不会动它。
#    这里显式确认一下，免得用户以为更新把品牌主题弄丢了。
HAS_BRAND=0
[ -f config/themes/palettes/brand.py ] && HAS_BRAND=1

say M_UP_S4
if git pull --ff-only 2>&1 | sed 's/^/  /'; then
  printf "  ${g}%s${o}\n" "$(t M_UP_PULLED)"
else
  printf "  ${y}%s${o}\n" "$(t M_UP_PULL_FAIL)"; exit 1
fi
if [ "$HAS_BRAND" = "1" ] && [ ! -f config/themes/palettes/brand.py ]; then
  printf "  ${y}%s${o}\n" "$(t M_UP_BRAND_GONE)"
fi

say M_UP_S5
(cd config/themes && python3 _generate.py 2>&1 | sed 's/^/  /')

say M_UP_S6
# ⚠️ 这一步以前是漏的：update 只重生成主题、重跑 theme.sh，
#    但 ~/.config/starship.toml 是 install.sh **拷**过去的一份副本，不是软链。
#    结果是提示符版式改了多少版，已经装过的人一版都收不到（改了等于没改）。
#    这里补上，但不闷声覆盖：内容一样就不动，不一样先备份再拷、并把备份路径说出来。
SS_SRC="config/starship.toml"; SS_DST="$HOME/.config/starship.toml"
if [ ! -f "$SS_DST" ]; then
  mkdir -p "$(dirname "$SS_DST")"; cp "$SS_SRC" "$SS_DST"
  printf "  ${g}%s${o}\n" "$(t M_UP_SS_NEW)"
elif cmp -s "$SS_SRC" "$SS_DST"; then
  printf "  ${d}%s${o}\n" "$(t M_UP_SS_SAME)"
else
  _ss_bak="$SS_DST.bak.$(date +%Y%m%d%H%M%S)"
  cp "$SS_DST" "$_ss_bak"
  cp "$SS_SRC" "$SS_DST"
  printf "  ${g}%s${o}  ${d}%s${o}\n" "$(t M_UP_SS_UPDATED)" "$(t M_UP_SS_BAK "$_ss_bak")"
  printf "    ${d}%s${o}\n" "$(t M_UP_SS_NOTE)"
fi

say M_UP_S7
CUR_THEME="$(hkw_resolve_theme "$(cat "$RUNTIME/theme" 2>/dev/null || echo '')")"
if [ -n "$CUR_THEME" ] && [ -f "config/themes/$CUR_THEME.json" ]; then
  if [ -f "$HOME/.config/hekouwang-terminal/p3" ]; then
    bash ./scripts/theme.sh "$CUR_THEME" --p3 | sed 's/^/  /'
  else
    bash ./scripts/theme.sh "$CUR_THEME" | sed 's/^/  /'
  fi
else
  printf "  ${d}%s${o}\n" "$(t M_UP_NO_THEME)"
fi

# bat 主题内容可能变了，重建一次缓存
if command -v bat >/dev/null 2>&1; then
  BT="$(bat --config-dir)/themes"
  if [ -d "$BT" ]; then
    for eco in config/themes/ecosystem/*/; do
      [ -f "$eco/bat.tmTheme" ] && cp "$eco/bat.tmTheme" "$BT/hekouwang-$(basename "$eco").tmTheme"
    done
    bat cache --build >/dev/null 2>&1 && printf "  ${g}%s${o}\n" "$(t M_UP_BAT)"
  fi
fi

NEW_VER="$(tr -d '[:space:]' < VERSION 2>/dev/null)"
printf "\n${g}%s${o}  ${d}%s → %s${o}\n" "$(t M_UP_DONE)" "${CUR_VER:-?}" "${NEW_VER:-?}"
printf "${d}%s${o}\n" "$(t M_UP_DONE_NOTE)"
