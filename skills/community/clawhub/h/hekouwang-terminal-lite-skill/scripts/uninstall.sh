#!/bin/bash
# ============================================================
# hekouwang-terminal-skill — 卸载 / 还原
#
# 用法:
#   ./scripts/uninstall.sh              交互式：逐项问，默认只删本套装的东西
#   ./scripts/uninstall.sh --dry-run    只打印会干什么，一个字节都不动
#   ./scripts/uninstall.sh --yes        不问，执行「默认档」（不卸 brew 包、不删 oh-my-zsh）
#
# 设计底线（和 install.sh 是一对，别单独改其中一个）：
#   1. 只删本套装自己装的东西。Homebrew 本体、oh-my-zsh、你自己的
#      ~/.zshrc.local、你 git 里的配置，一律不碰（除非你显式勾）。
#   2. ~/.zshrc 从 ~/.hekouwang-terminal-backups/ 里最新备份还原（兼容家目录根旧 .bak）。
#      找不到备份就明说找不到，不假装成功。
#   3. iTerm2 的 GUI 设置用 defaults delete 还原成「iTerm2 出厂默认」，
#      不是写一个我们以为的默认值 —— 那样只是换一种方式改你的配置。
#   4. 删之前先打印清单。--dry-run 跑完能看到一模一样的清单。
# ============================================================
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/i18n.sh"
hkw_i18n_init uninstall "$@"
eval set -- "$HKW_ARGS"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/bak.sh"
DOMAIN="com.googlecode.iterm2"
GUID="catppuccin-mocha-dynamic-2026"
DP_DIR="$HOME/Library/Application Support/iTerm2/DynamicProfiles"
RUNTIME="$HOME/.config/hekouwang-terminal"

DRY=0; ASSUME_YES=0
for a in "$@"; do
  case "$a" in
    --dry-run|-n) DRY=1 ;;
    --yes|-y)     ASSUME_YES=1 ;;
    -h|--help)    blk_uninstall_help; exit 0 ;;
  esac
done

r='\033[1;31m'; g='\033[1;32m'; y='\033[1;33m'; b='\033[1;34m'; d='\033[2m'; o='\033[0m'
head() { printf "\n${b}%s${o}\n" "$(t "$@")"; }
act()  { printf "  ${g}·${o} %s\n" "$(t "$@")"; }
skip() { printf "  ${d}· %s${o}\n" "$(t "$@")"; }
warn() { printf "  ${y}⚠${o} %s\n" "$(t "$@")"; }

# run <词条key|现成文字> [词条参数…] -- 命令...
# ⚠️ 描述可能自带 printf 参数（"%s"），所以用 `--` 把「描述那几个词」和「要跑的命令」分开，
#    不能再靠「第一个参数是描述、其余全是命令」—— 那样带参数的词条就没处放了。
run() {
  local desc=()
  while [ $# -gt 0 ] && [ "$1" != "--" ]; do desc[${#desc[@]}]="$1"; shift; done
  [ "${1:-}" = "--" ] && shift
  local text; text="$(t ${desc+"${desc[@]}"})"
  if [ "$DRY" = "1" ]; then printf "  ${d}[dry-run]${o} %s\n" "$text"; return 0; fi
  # 交互模式逐项确认；--yes 才跳过
  if [ "$ASSUME_YES" != "1" ]; then
    local ans
    printf "  ${y}?${o} %s [y/N] " "$(t M_UN_ASK_ITEM "$text")"
    read -r ans </dev/tty || ans=""
    [[ "$ans" =~ ^[Yy] ]] || { skip M_UN_KEEP_ITEM; return 0; }
  fi
  printf "  ${g}·${o} %s\n" "$text"
  "$@" >/dev/null 2>&1 || true
}

run_ok() {   # 已经在上层 ask 过的项，不再二次询问
  local desc=()
  while [ $# -gt 0 ] && [ "$1" != "--" ]; do desc[${#desc[@]}]="$1"; shift; done
  [ "${1:-}" = "--" ] && shift
  local text; text="$(t ${desc+"${desc[@]}"})"
  if [ "$DRY" = "1" ]; then printf "  ${d}[dry-run]${o} %s\n" "$text"; return 0; fi
  printf "  ${g}·${o} %s\n" "$text"
  "$@" >/dev/null 2>&1 || true
}

ask_text() {  # ask_text <问题文本> [默认]
  local q="$1" def="${2:-n}"
  [ "$ASSUME_YES" = "1" ] && { [ "$def" = "y" ]; return; }
  [ "$DRY" = "1" ] && { [ "$def" = "y" ]; return; }
  local hint="[y/N]"; [ "$def" = "y" ] && hint="[Y/n]"
  printf "  ${y}?${o} %s %s " "$q" "$hint"
  local ans; read -r ans </dev/tty || ans=""
  ans="${ans:-$def}"
  [[ "$ans" =~ ^[Yy] ]]
}

ask() {   # ask <词条key> 默认(y/n) → 返回 0=做
  local q; q="$(t "$1")"; local def="${2:-n}"
  [ "$ASSUME_YES" = "1" ] && { [ "$def" = "y" ]; return; }
  [ "$DRY" = "1" ] && { [ "$def" = "y" ]; return; }
  local hint="[y/N]"; [ "$def" = "y" ] && hint="[Y/n]"
  printf "  ${y}?${o} %s %s " "$q" "$hint"
  read -r ans </dev/tty || ans=""
  ans="${ans:-$def}"
  [[ "$ans" =~ ^[Yy] ]]
}

printf "${b}%s${o}\n" "$(t M_UN_HEAD)"
[ "$DRY" = "1" ] && printf "${y}%s${o}\n" "$(t M_UN_DRY)"

# ---- 1. ~/.zshrc 还原 --------------------------------------
head M_UN_S1
# 取最新一个 install/migrate 留下的备份。优先新目录 backups/，兼容家目录根散落的旧文件。
# ls 在这里不可靠（可能被 eza 之类接管），用 find。
hkw_bak_sweep_legacy
LATEST_BAK="$(hkw_bak_latest_zshrc)"
if [ -n "$LATEST_BAK" ]; then
  printf "  %s${d}%s${o}\n" "$(t M_UN_BAK_FOUND)" "$LATEST_BAK"
  if ask M_UN_ASK_RESTORE y; then
    if [ "$DRY" = "0" ]; then
      # 卸载前的现场也收进 backups/，别再丢回 $HOME
      [ -f "$HOME/.zshrc" ] && hkw_bak_copy "$HOME/.zshrc" zshrc.uninstall >/dev/null
      cp "$LATEST_BAK" "$HOME/.zshrc"
      act M_UN_RESTORED "$(basename "$LATEST_BAK")"
    else
      # ⚠️ dry-run 里绝不能说「已还原」——本文件第 4 条设计底线就是
      #    「--dry-run 跑完能看到一模一样的清单」，说了等于骗人。
      printf "  ${d}[dry-run]${o} %s\n" "$(t M_UN_RESTORED "$(basename "$LATEST_BAK")")"
    fi
  else
    skip M_UN_KEEP_ZSHRC
  fi
else
  warn M_UN_NO_BAK
  skip M_UN_NO_BAK_NOTE
fi

# ---- 2. 配置文件 -------------------------------------------
head M_UN_S2
[ -f "$DP_DIR/hekouwang-active-theme.json" ] \
  && run M_UN_RM_DP -- rm -f "$DP_DIR/hekouwang-active-theme.json" \
  || skip M_UN_NO_DP
# 卸载前先把安装清单拷出来：下面会删整个 $RUNTIME，第 6 节还要读它
BREW_MANIFEST_SNAPSHOT=""
if [ -f "$RUNTIME/installed-brew.txt" ]; then
  BREW_MANIFEST_SNAPSHOT="$(mktemp)"
  cp "$RUNTIME/installed-brew.txt" "$BREW_MANIFEST_SNAPSHOT"
fi
[ -d "$RUNTIME" ] \
  && run M_UN_RM_RUNTIME -- rm -rf "$RUNTIME" \
  || skip M_UN_NO_RUNTIME
[ -f "$HOME/.config/starship.toml" ] && {
  if ask M_UN_ASK_STARSHIP n; then
    # 安装时承诺过「覆盖前先备份」，卸载就先把最新备份放回去；没有备份才删
    SS_BAK="$(find "$HOME/.config" -maxdepth 1 -name 'starship.toml.bak.*' -type f 2>/dev/null | sort | tail -1)"
    if [ -n "$SS_BAK" ]; then
      run_ok M_UN_RESTORE_STARSHIP "$(basename "$SS_BAK")" -- cp "$SS_BAK" "$HOME/.config/starship.toml"
    else
      run_ok M_UN_RM_STARSHIP -- rm -f "$HOME/.config/starship.toml"
    fi
  else skip M_UN_KEEP_STARSHIP; fi
}
# Ghostty：只删我们生成的 hekouwang-* 主题；config 有备份就还原
if [ -d "$HOME/.config/ghostty/themes" ]; then
  run M_UN_RM_GHOSTTY_THEMES -- bash -c \
    'rm -f "$HOME/.config/ghostty/themes/"hekouwang-*'
fi
GBAK="$(find "$HOME/.config/ghostty" -maxdepth 1 -name 'config.bak.*' -type f 2>/dev/null | sort | tail -1)"
if [ -n "$GBAK" ]; then
  if ask M_UN_ASK_GHOSTTY y; then
    run_ok M_UN_RESTORE_GHOSTTY "$(basename "$GBAK")" -- cp "$GBAK" "$HOME/.config/ghostty/config"
  fi
# ⚠️ 三种标记都认：现行 ASCII `hekouwang-terminal-skill`、旧技术代号
#    `hekouwang-terminal-kit`、以及 2.1 及更早的中文标题「会勇禾口王」。
elif [ -f "$HOME/.config/ghostty/config" ] && grep -qE "hekouwang-terminal-skill|hekouwang-terminal-kit|会勇禾口王" "$HOME/.config/ghostty/config" 2>/dev/null; then
  run M_UN_RM_GHOSTTY_CFG -- rm -f "$HOME/.config/ghostty/config"
fi
# bat 主题
if [ -d "$HOME/.config/bat/themes" ]; then
  run M_UN_RM_BAT -- bash -c 'rm -f "$HOME/.config/bat/themes/"hekouwang-*.tmTheme'
  [ "$DRY" = "0" ] && command -v bat >/dev/null 2>&1 && bat cache --build >/dev/null 2>&1
fi
# VS Code / Cursor 扩展
for ext_root in "$HOME/.vscode/extensions" "$HOME/.cursor/extensions"; do
  [ -d "$ext_root" ] || continue
found="$(find "$ext_root" -maxdepth 1 -name 'hekouwang*terminal-themes*' -type d 2>/dev/null)"
if [ -n "$found" ]; then
  while IFS= read -r d; do
    [ -n "$d" ] || continue
    run M_UN_RM_VSC "$(basename "$ext_root")" -- rm -rf "$d"
  done <<< "$found"
fi
done

# ---- 2b. macOS 自带终端 -------------------------------------
head M_UN_S2B
if [ -n "${TERM_PROGRAM:-}" ] && [ "${TERM_PROGRAM}" = "Apple_Terminal" ]; then
  warn M_UN_INSIDE_APPLE
  skip M_UN_INSIDE_APPLE_FIX
elif [ "$DRY" = "1" ]; then
  printf "  ${d}[dry-run]${o} %s\n" "$(t M_UN_APPLE_DRY)"
elif ask_text "$(t M_UN_ASK_ITEM "$(t M_UN_RM_APPLE)")" n; then
  python3 - <<'PY' 2>/dev/null || skip M_UN_APPLE_NONE
import plistlib, subprocess, sys
DOMAIN = 'com.apple.Terminal'
out = subprocess.run(['defaults', 'export', DOMAIN, '-'], capture_output=True)
if out.returncode != 0 or not out.stdout:
    sys.exit(1)
pl = plistlib.loads(out.stdout)
ws = pl.get('Window Settings', {})
# 双语之后 Profile 名有中英两种，两个前缀都要认 —— 只认一个就会留下一半没删干净
ours = [k for k in ws if k.startswith('会勇禾口王') or k.lower().startswith('hekouwang')]
if not ours:
    sys.exit(1)
for k in ours:
    ws.pop(k, None)
# 默认 Profile 还原：优先用我们当初记下的「原来是谁」，否则退回 Basic
prev = pl.pop('HekouwangPreviousDefault', None) or 'Basic'
for key in ('Default Window Settings', 'Startup Window Settings'):
    if str(pl.get(key, '')).startswith('会勇禾口王') or str(pl.get(key, '')).lower().startswith('hekouwang'):
        pl[key] = prev
subprocess.run(['defaults', 'import', DOMAIN, '-'], input=plistlib.dumps(pl), check=True)
print(f"  · 已删 {len(ours)} 个 Profile，默认 Profile 还原成 {prev}")
PY
  if ps -Ao ucomm= 2>/dev/null | grep -qx Terminal; then
    warn M_UN_APPLE_RUNNING
  fi
else
  skip M_UN_KEEP_ITEM
fi
[ -f "$HOME/.hekouwang-AppleTerminal-prefs.bak.plist" ] && \
  skip M_UN_APPLE_BAK

# ---- 3. 挂在别人配置里的引用 --------------------------------
head M_UN_S3
# ~/.gitconfig 的 [include]：只删指向本套装的那一段，别动别的 include
if [ -f "$HOME/.gitconfig" ] && grep -q "hekouwang-terminal" "$HOME/.gitconfig" 2>/dev/null; then
  if [ "$DRY" = "1" ]; then
    printf "  ${d}[dry-run]${o} %s\n" "$(t M_UN_GIT_DRY)"
  elif ! ask_text "$(t M_UN_ASK_ITEM "$(t M_UN_RM_GIT)")" n; then
    skip M_UN_KEEP_ITEM
  else
    cp "$HOME/.gitconfig" "$HOME/.gitconfig.bak.$(date +%Y%m%d%H%M%S)"
    python3 - "$HOME/.gitconfig" <<'PY'
import re, sys
p = sys.argv[1]
src = open(p, encoding='utf-8').read()
# 只摘掉 path 指向 hekouwang-terminal 的那一行；[include] 段若因此变空也一并去掉
src = re.sub(r'(?m)^\s*path\s*=\s*.*hekouwang-terminal.*\n', '', src)
src = re.sub(r'(?m)^\[include\]\s*\n(?=\s*(\[|$))', '', src)
open(p, 'w', encoding='utf-8').write(src)
PY
    act M_UN_GIT_DONE
  fi
else
  skip M_UN_GIT_NONE
fi
# ~/.tmux.conf 的 source-file
if [ -f "$HOME/.tmux.conf" ] && grep -q "hekouwang-terminal" "$HOME/.tmux.conf" 2>/dev/null; then
  if [ "$DRY" = "1" ]; then
    printf "  ${d}[dry-run]${o} %s\n" "$(t M_UN_TMUX_DRY)"
  elif ! ask_text "$(t M_UN_ASK_ITEM "$(t M_UN_RM_TMUX)")" n; then
    skip M_UN_KEEP_ITEM
  else
    cp "$HOME/.tmux.conf" "$HOME/.tmux.conf.bak.$(date +%Y%m%d%H%M%S)"
    grep -v "hekouwang-terminal" "$HOME/.tmux.conf" > "$HOME/.tmux.conf.tmp" \
      && mv "$HOME/.tmux.conf.tmp" "$HOME/.tmux.conf"
    act M_UN_TMUX_DONE
  fi
else
  skip M_UN_TMUX_NONE
fi


# ---- 5. iTerm2 GUI 设置还原 ---------------------------------
head M_UN_S5
# ⚠️ 和 setup-gui.sh 同一个坑：重置这些设置要求 iTerm2 先退出（否则它退出时会用内存里的
#    配置盖回去），但人往往就是**从 iTerm2 里**跑卸载的 —— 那等于把自己连脚本一起关掉，
#    卸载停在半截。判据用 iTerm2 注入的环境变量，不用 pgrep（沙箱下 pgrep 看不到 GUI 进程）。
INSIDE_ITERM=0
if [ -n "${ITERM_SESSION_ID:-}" ] || [ "${TERM_PROGRAM:-}" = "iTerm.app" ] || [ "${LC_TERMINAL:-}" = "iTerm2" ]; then
  INSIDE_ITERM=1
fi
if [ "$INSIDE_ITERM" = "1" ] && [ "$DRY" = "0" ]; then
  warn M_UN_INSIDE_ITERM
  skip M_UN_INSIDE_ITERM_WHY
  skip M_UN_INSIDE_ITERM_FIX "$SCRIPT_DIR"
  skip M_UN_INSIDE_ITERM_WHAT
elif ask M_UN_ASK_GUI y; then
  if [ "$DRY" = "0" ] && { pgrep -x iTerm2 >/dev/null 2>&1 || ps -Ao ucomm= 2>/dev/null | grep -qx iTerm2; }; then
    warn M_UN_ITERM_RUNNING
    osascript -e 'tell application "iTerm2" to quit' 2>/dev/null || killall iTerm2 2>/dev/null || true
    for _ in $(seq 1 20); do
      pgrep -x iTerm2 >/dev/null 2>&1 || ps -Ao ucomm= 2>/dev/null | grep -qx iTerm2 || break
      sleep 0.3
    done
  fi
  # 用 delete 而不是写回我们以为的默认值 —— delete 才是真·恢复默认
  for k in TabStyleWithAutomaticOption UseBorder HideTab ShowFullScreenTabBar \
           HideTabNumber HideScrollbar DimInactiveSplitPanes SplitPaneDimmingAmount \
           DimBackgroundWindows StatusBarPosition ToolbeltTools CommandSelection \
           CopySelection TripleClickSelectsFullWrappedLines ShowNewOutputIndicator; do
    run_ok "defaults delete $k" -- defaults delete "$DOMAIN" "$k"
  done
  # 默认 Profile：只有当它还指着我们的 Guid 时才删，别动用户后来自己设的
  CUR_DEF="$(defaults read "$DOMAIN" 'Default Bookmark Guid' 2>/dev/null || echo '')"
  if [ "$CUR_DEF" = "$GUID" ]; then
    run_ok "defaults delete 'Default Bookmark Guid'" -- defaults delete "$DOMAIN" "Default Bookmark Guid"
  else
    skip M_UN_DEFAULT_KEPT
  fi
  # Shift+Enter：只摘我们加的两个键，别整个 GlobalKeyMap 删掉（用户可能有自己的映射）
  if [ "$DRY" = "0" ]; then
    python3 - "$DOMAIN" <<'PY' 2>/dev/null || true
import subprocess, sys, plistlib
dom = sys.argv[1]
out = subprocess.run(['defaults', 'export', dom, '-'], capture_output=True)
if out.returncode == 0 and out.stdout:
    pl = plistlib.loads(out.stdout)
    km = pl.get('GlobalKeyMap')
    if isinstance(km, dict):
        before = len(km)
        for k in ('0xd-0x20000', '0xd-0x20000-0x24'):
            km.pop(k, None)
        if len(km) != before:
            pl['GlobalKeyMap'] = km
            subprocess.run(['defaults', 'import', dom, '-'],
                           input=plistlib.dumps(pl), check=False)
            print('  · 已摘掉 Shift+Enter 键映射（其余映射保留）')
PY
  else
    printf "  ${d}[dry-run]${o} %s\n" "$(t M_UN_KEYMAP_DRY)"
  fi
  # 长按连续重复：这是系统级、很多人本来就想要，单独问
  if ask M_UN_ASK_PRESSHOLD n; then
    run "defaults delete -g ApplePressAndHoldEnabled" -- defaults delete -g ApplePressAndHoldEnabled
  fi
else
  skip M_UN_KEEP_GUI
fi

# ---- 6. 可选：卸命令行工具 ----------------------------------
head M_UN_S6
MANIFEST="${BREW_MANIFEST_SNAPSHOT:-$RUNTIME/installed-brew.txt}"
RECORDED=""
COUNT=0
if [ -f "$MANIFEST" ]; then
  while IFS=: read -r kind name; do
    [ -n "$name" ] || continue
    case "$kind" in
      formula) brew list --formula "$name" >/dev/null 2>&1 || continue ;;
      cask)    brew list --cask "$name" >/dev/null 2>&1 || continue ;;
      *)       continue ;;
    esac
    RECORDED="$RECORDED $name"
    COUNT=$((COUNT + 1))
  done < "$MANIFEST"
fi
if [ "$COUNT" -gt 0 ]; then
  printf "  ${d}%s${o}\n" "$(t M_UN_INSTALLED_HERE "${RECORDED# }")"
  if ask M_UN_ASK_BREW n; then
    while IFS=: read -r kind name; do
      [ -n "$name" ] || continue
      case "$kind" in
        formula)
          brew list --formula "$name" >/dev/null 2>&1 \
            && run_ok "brew uninstall $name" -- brew uninstall "$name" ;;
        cask)
          brew list --cask "$name" >/dev/null 2>&1 \
            && run_ok "brew uninstall --cask $name" -- brew uninstall --cask "$name" ;;
      esac
    done < "$MANIFEST"
  else
    skip M_UN_KEEP_BREW
  fi
else
  skip M_UN_NO_BREW
fi
if [ -n "$BREW_MANIFEST_SNAPSHOT" ]; then
  rm -f "$BREW_MANIFEST_SNAPSHOT"
fi
if [ -d "$HOME/.oh-my-zsh" ]; then
  if ask M_UN_ASK_OMZ n; then
    run_ok M_UN_RM_OMZ -- rm -rf "$HOME/.oh-my-zsh"
  else skip M_UN_KEEP_OMZ; fi
fi

# ---- 汇总 --------------------------------------------------
printf "\n${b}%s${o}\n" "$(t M_UN_DONE)"
if [ "$DRY" = "1" ]; then
  printf "${y}%s${o}\n" "$(t M_UN_DONE_DRY)"
else
  printf "${g}%s${o}%s\n" "$(t M_UN_DONE_REAL_A)" "$(t M_UN_DONE_REAL_B)"
  printf "${d}%s\n" "$(t M_UN_DONE_KEPT)"
  printf "%s${o}\n" "$(t M_UN_DONE_KEPT2)"
fi
