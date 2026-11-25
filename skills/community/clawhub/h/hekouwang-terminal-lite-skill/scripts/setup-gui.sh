#!/bin/bash
# ============================================================
# hekouwang-terminal-skill — GUI 三步自动化
# 用法: ./scripts/setup-gui.sh
# 把原本要手点的 3 处 GUI 设置用 defaults 一次写好：
#   1. Minimal 主题         (TabStyleWithAutomaticOption = 5)
#   2. 默认 Profile         (Default Bookmark Guid = 本 skill 共享 Guid)
#   3. Shift+Enter 换行      (GlobalKeyMap 加一条 Send Text = 换行)
# 外加几项 Minimal 搭配项（去窗口边框、单 tab 隐藏 tab bar）。
# ⚠️ defaults 写入会在 iTerm2 退出时被其内存配置覆盖，所以必须先退出 iTerm2。
# ============================================================
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/$(basename "${BASH_SOURCE[0]}")"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/i18n.sh"
hkw_i18n_init setup-gui "$@"
eval set -- "$HKW_ARGS"
DOMAIN="com.googlecode.iterm2"
GUID="catppuccin-mocha-dynamic-2026"   # 与 config/themes/*.json 内的共享 Guid 一致

c='\033[1;35m'; d='\033[2m'; o='\033[0m'
say() { printf "\n${c}▶ %s${o}\n" "$(t "$@")"; }

# ---- 0. 先退出 iTerm2（否则写入被 iTerm2 退出时的落盘覆盖）----
#
# ⚠️ 但绝不能在「本脚本正跑在 iTerm2 里」的时候退出它 —— 那等于把跑着 install.sh
#    的那个终端连同脚本一起杀掉，人被扔在半截状态（配置写了一半、后面的自检没跑）。
#    从 iTerm2 里重跑 install.sh 是很常见的（第二次装、升级），必须挡住。
#    判据用 iTerm2 自己注入的环境变量，不依赖 pgrep（沙箱/权限下 pgrep 可能看不到 GUI 进程）。
if [ -n "${ITERM_SESSION_ID:-}" ] || [ "${TERM_PROGRAM:-}" = "iTerm.app" ] || [ "${LC_TERMINAL:-}" = "iTerm2" ]; then
  printf "\n\033[1;33m%s\033[0m\n" "$(t M_GUI_INSIDE)"
  printf "\033[2m%s\n" "$(t M_GUI_INSIDE_1)"
  printf "%s\n" "$(t M_GUI_INSIDE_2)"
  printf "%s\n\n" "$(t M_GUI_INSIDE_3)"
  printf "%s\n" "$(t M_GUI_INSIDE_4)"
  printf "%s\n" "$(t M_GUI_INSIDE_A "$SCRIPT_PATH")"
  printf "%s\n\n" "$(t M_GUI_INSIDE_B)"
  printf "%s\n" "$(t M_GUI_INSIDE_5)"
  printf "%s\n" "$(t M_GUI_INSIDE_6)"
  printf "%s\033[0m\n" "$(t M_GUI_INSIDE_7)"
  exit 0
fi

if pgrep -x iTerm2 >/dev/null 2>&1 || ps -Ao ucomm= 2>/dev/null | grep -qx iTerm2; then
  say M_GUI_QUIT
  osascript -e 'tell application "iTerm2" to quit' 2>/dev/null || killall iTerm2 2>/dev/null || true
  for _ in $(seq 1 20); do
    pgrep -x iTerm2 >/dev/null 2>&1 || ps -Ao ucomm= 2>/dev/null | grep -qx iTerm2 || break
    sleep 0.3
  done
fi

# ---- 1. Minimal 主题 ----
say M_GUI_MINIMAL
defaults write "$DOMAIN" TabStyleWithAutomaticOption -int 5
defaults write "$DOMAIN" UseBorder -bool false                 # 去窗口边框
defaults write "$DOMAIN" HideTab -bool true                    # 单 tab 时隐藏 tab bar
defaults write "$DOMAIN" ShowFullScreenTabBar -bool true       # 全屏仍显示 tab bar
defaults write "$DOMAIN" HideTabNumber -bool false

# ---- 1b. 质感层的全局部分 ----
# 与 config/themes/*.json 里的毛玻璃/光标是一套（那边是 Profile 级、热加载；这三条只能全局）。
say M_GUI_TEXTURE
defaults write "$DOMAIN" HideScrollbar -bool true              # Minimal 的最后一块杂色
defaults write "$DOMAIN" DimInactiveSplitPanes -bool true      # 非活动分屏自动压暗，焦点一眼可见
defaults write "$DOMAIN" SplitPaneDimmingAmount -float 0.4     # 压暗强度 0–1，0.4 够明显又不瞎
defaults write "$DOMAIN" DimBackgroundWindows -bool false      # 别压暗整个后台窗口（录屏切窗会忽明忽暗）
# 窗口内边距：Minimal（无标题栏、无边框、无滚动条）时，文字默认贴着圆角窗沿，
# 加一圈留白整块画布才立得住。iTerm2 只有**全局**边距（Appearance ▸ Panes），
# 不能按 Profile/场景分别设；键名取自二进制里的 TerminalMargin / TerminalVMargin。
# ⚠️ 高级设置启动时读一次，写完要重开 iTerm2 才生效（不是热加载）。
defaults write "$DOMAIN" TerminalMargin -int 10                # 左右留白（点）
defaults write "$DOMAIN" TerminalVMargin -int 8                # 上下留白（点）

# ---- 1c. 功能层的全局部分 ----
# 状态栏「开不开 + 放哪些组件」在 Profile JSON 里（热加载）；只有「顶还是底」是全局。
say M_GUI_FUNC
defaults write "$DOMAIN" StatusBarPosition -int 1              # 0=顶 1=底；Minimal 下置底更像原生
# 工具带：右侧边栏。Captured Output 需要 Profile 里的 CaptureTrigger 才有内容。
defaults write "$DOMAIN" ToolbeltTools -array "Captured Output" "Snippets" "Command History"
# 语义交互层依赖：Cmd-click 打开 URL / Semantic History（出厂默认 YES，这里显式钉住防被关）
# 键名 = iTermPreferences.m 的 kPreferenceKeyCmdClickOpensURLs → @"CommandSelection"
defaults write "$DOMAIN" CommandSelection -bool true
# 常用操作：复制即选 / 三击选整行（含折行）/ 标签页新输出指示
# 三个键名都在 iTerm2 二进制里确认过，不是猜的。
defaults write "$DOMAIN" CopySelection -bool true
defaults write "$DOMAIN" TripleClickSelectsFullWrappedLines -bool true
defaults write "$DOMAIN" ShowNewOutputIndicator -bool true

# ---- 2. 默认 Profile ----
say M_GUI_PROFILE
defaults write "$DOMAIN" "Default Bookmark Guid" -string "$GUID"

# ---- 3. 全局键映射（Shift+Enter 换行等）----
# ⚠️ 键映射的内容在 config/keymap.json 里，**不写死在本脚本**。
#    脚本全部开源，写死的 defaults write 谁都能照抄；做成数据文件，
#    门控的才是「配置内容」而不是代码。文件不在（开源版）就静默跳过。
KEYMAP="$SCRIPT_DIR/config/keymap.json"
if [ -f "$KEYMAP" ]; then
  say M_GUI_KEYMAP
  while IFS=$'\t' read -r k v; do
    [ -n "$k" ] || continue
    defaults write "$DOMAIN" GlobalKeyMap -dict-add "$k" "$v"
    printf "${d}  + %s${o}\n" "$k"
  done < <(python3 -c "
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8')).get('GlobalKeyMap',{})
for k,v in d.items(): print(f'{k}\t{v}')
" "$KEYMAP")
else
  printf "${d}%s${o}\n" "$(t M_GUI_KEYMAP_SKIP)"
fi

# 注意：千万别在这里 killall cfprefsd —— defaults write 的改动先在 cfprefsd 内存里，
# 立刻 kill 会把还没落盘的写入一起丢掉。cfprefsd 会自行落盘，iTerm2 下次启动也会同步。
say M_GUI_DONE
printf "${d}%s${o}\n" "$(t M_GUI_DONE_1)"
printf "${d}%s${o}\n" "$(t M_GUI_DONE_2)"
