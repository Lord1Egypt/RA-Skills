#!/bin/bash
# KPA 实机体验问题修复（v2.0.1 新增）
#
# 修五类实机反馈问题，全部只改配置、可回滚：
#   dos      DOSBox-pure 关闭倒带与自动存档  -> 消除左下角 "Save State Error" 弹窗
#   nds      melonDS 双屏改上下 + 原始宽高比  -> 修两屏并排被拉伸变形
#   flycast  关闭多线程渲染                  -> 修 Atomiswave 背景满屏雪花噪点
#   aw-osd   逐个 Atomiswave 游戏关闭 OSD 文字 -> 消除 "Please upgrade to MAME romsets" 提示
#   p2       断掉 2P 与 1P 共用同一手柄      -> 修"一个手柄同时控制两个角色"
#
# 用法：
#   bash scripts/kpa_gamefix.sh all              # 默认 dry-run，只打印将要做的改动
#   bash scripts/kpa_gamefix.sh all --apply      # 真正写入设备
#   bash scripts/kpa_gamefix.sh nds --apply      # 只做 NDS
#   bash scripts/kpa_gamefix.sh all --revert     # 用 .bakKPA3 备份回滚
#
# 注意：改配置后需重启对应平台才会生效（脚本会提示）。天马界面相关改动见 kpa_themetweak.sh。

set -u
cd "$(dirname "$0")" || exit 1
# shellcheck source=kpa_env.sh
. ./kpa_env.sh
require_device >/dev/null 2>&1 || { echo "ERROR: 未检测到 KPA 设备"; exit 1; }

ACTION="${1:-all}"
MODE="${2:-}"
CFG_INT="$INT/Android/data/$RA_PKG/files/retroarch.cfg"   # 天马 launch 传的 CONFIGFILE（实际生效）
CFG_RA2="$INT/RetroArch/retroarch.cfg"                      # 直接从 RA 图标启动时读的那份，需同步
RA_CONFIG="$INT/RetroArch/config"
DOS_CFG="$RA_CONFIG/DOSBox-pure/DOSBox-pure.cfg"
NDS_OPT="$RA_CONFIG/melonDS/melonDS.opt"
NDS_CFG="$RA_CONFIG/melonDS/melonDS.cfg"
FLY_OPT="$RA_CONFIG/Flycast/Flycast.opt"
AW_META="$TF/Roms/ATOMISWAVE/metadata.pegasus.txt"

[ "$MODE" = "--apply" ] && APPLY=1 || APPLY=0
[ "$MODE" = "--revert" ] && REVERT=1 || REVERT=0

say() { printf '%s\n' "$*"; }
plan() { if [ "$APPLY" = 1 ]; then say "  WRITE  $*"; else say "  PLAN   $*"; fi; }

# set_kv <设备文件> <键> <值>：存在则替换该行，不存在则追加。先备份为 .bakKPA3
set_kv() {
  local f="$1" k="$2" v="$3"
  local exists
  # 注意：adb 会吞 stdin，所有 adb 调用统一 </dev/null，否则外层 while read 只会跑第一轮
  exists=$(sh "grep -c '^$k = ' '$f' 2>/dev/null || true" </dev/null | tr -d '\r')
  plan "$(basename "$f"): $k = \"$v\"  (原有 $exists 行)"
  [ "$APPLY" = 1 ] || return 0
  sh "if [ -f '$f' ] && [ ! -f '$f.bakKPA3' ]; then cp '$f' '$f.bakKPA3'; fi" </dev/null >/dev/null 2>&1
  sh "f='$f'; k='$k'; v='$v'; touch \"\$f\"; if grep -q \"^\$k = \" \"\$f\"; then sed -i \"s|^\$k = .*|\$k = \\\"\$v\\\"|\" \"\$f\"; else printf '%s = \"%s\"\\n' \"\$k\" \"\$v\" >> \"\$f\"; fi" </dev/null
}

# revert_kv <设备文件> <键> <原值>：把键改回原值；原值传空表示删除该行
# 为什么不用 cp 备份回滚：同一份 cfg 可能被多次脚本/手工改动，.bak 很容易在某次
# "改完之后" 被创建，从而变成"已改版"备份 —— 此时 cp 回去等于没回滚。值级回滚更可靠。
revert_kv() {
  local f="$1" k="$2" v="$3"
  if [ -z "$v" ]; then
    say "  REVERT $(basename "$f"): 删除 $k 行"
    sh "sed -i '/^$k = /d' '$f'" </dev/null
  else
    say "  REVERT $(basename "$f"): $k = \"$v\""
    sh "sed -i 's|^$k = .*|$k = \"$v\"|' '$f'" </dev/null
  fi
  return 0
}

# restore <设备文件>：从 .bakKPA3 整份回滚（仅用于确认备份是改动前版本的场合）
restore() {
  local f="$1"
  if sh "[ -f '$f.bakKPA3' ] && echo yes" </dev/null 2>/dev/null | tr -d '\r' | grep -q yes; then
    sh "cp '$f.bakKPA3' '$f'" </dev/null
    say "  REVERT $(basename "$f")"
  else
    say "  SKIP   $(basename "$f")（无 .bakKPA3 备份）"
  fi
}

fix_dos() {
  say "[dos] DOSBox-pure：关闭倒带与自动存档"
  say "      根因：全局 rewind_enable=true，而 DOSBox-pure 进来先停在 START MENU、游戏尚未运行，"
  say "            存状态必然失败 -> 左下角 'Save State Error: Unable to save state while game is not running.'"
  if [ "$REVERT" = 1 ]; then
    revert_kv "$DOS_CFG" rewind_enable true
    revert_kv "$DOS_CFG" savestate_auto_save true
    return
  fi
  set_kv "$DOS_CFG" rewind_enable false
  set_kv "$DOS_CFG" savestate_auto_save false
}

fix_nds() {
  say "[nds] melonDS：双屏上下排列 + 核心原始宽高比"
  say "      根因：screen_layout=Left/Right 且 aspect_ratio_index=23，两屏并排后又被拉满屏，纵向变形。"
  say "            实测 index 21/22 才是核心原始比例（亮像素宽约 408px）；23/24 会拉满 918px。"
  if [ "$REVERT" = 1 ]; then
    revert_kv "$NDS_OPT" melonds_screen_layout "Left/Right"
    revert_kv "$NDS_OPT" melonds_touch_mode "Mouse"
    revert_kv "$NDS_CFG" aspect_ratio_index 23
    return
  fi
  set_kv "$NDS_OPT" melonds_screen_layout "Top/Bottom"
  set_kv "$NDS_OPT" melonds_touch_mode "Touchscreen"
  set_kv "$NDS_CFG" aspect_ratio_index 21
}

fix_flycast() {
  say "[flycast] 关闭多线程渲染"
  say "      根因：Atomiswave 下 reicast_threaded_rendering=enabled 会导致背景满屏随机雪花噪点。"
  if [ "$REVERT" = 1 ]; then revert_kv "$FLY_OPT" reicast_threaded_rendering "enabled"; return; fi
  set_kv "$FLY_OPT" reicast_threaded_rendering "disabled"
}

fix_p2() {
  say "[p2] 断开 2P 与 1P 共用同一手柄"
  say "      根因：本机 P1、P2 的 joypad_index 都是 0，且 P2 的 analog_dpad_mode=3。"
  say "      analog_dpad_mode 不依赖按键绑定，直接把左摇杆换算成该玩家方向键 —— "
  say "      于是推摇杆时 1P、2P 同时收到方向，出现\"一个手柄控制两个角色\"\"主副角色都进入\"。"
  say "      只有没写 remap 的核心会踩到：fbalpha2012_cps1/2/3/neogeo、mame2003_plus 等"
  say "      （FBNeo / MAME / Flycast 自带 remap 里已把 P2 的 analog_dpad_mode 固定为 0，所以它们正常）"
  local f
  for f in "$CFG_INT" "$CFG_RA2"; do
    if [ "$REVERT" = 1 ]; then
      revert_kv "$f" input_player2_analog_dpad_mode "3"
      revert_kv "$f" input_player2_joypad_index "0"
      revert_kv "$f" input_player3_joypad_index "1"
    else
      set_kv "$f" input_player2_analog_dpad_mode "0"
      set_kv "$f" input_player2_joypad_index "1"
      set_kv "$f" input_player3_joypad_index "2"
    fi
  done
  say "      说明：P2 改到 joypad index 1（当前不存在第二个手柄 => 2P 收不到任何输入）；"
  say "            P3 顺移到 2，避免以后插小手柄时 P2/P3 抢同一索引；P1 的 analog_dpad_mode 保持 3 不变。"
}

fix_aw_osd() {
  say "[aw-osd] Atomiswave：逐游戏关闭 OSD 文字"
  say "      根因：flycast 对旧 MAME romset 发 SET_MESSAGE 提示，RA 以 OSD 显示，约数秒不散。"
  say "      关键：video_font_enable 必须在 per-game cfg 层写，per-playlist（ATOMOSWAVE.cfg）实测不生效。"
  local names n=0
  names=$(sh "grep '^game: ' '$AW_META' 2>/dev/null | sed 's/^game: //'" </dev/null | tr -d '\r')
  if [ -z "$names" ]; then say "  SKIP   未读到 Atomiswave 游戏列表（检查 $AW_META）"; return; fi
  # 先落成临时文件再逐行读：循环体里会调 adb，直接 here-string 会被吞
  local listfile
  listfile=$(mktemp "${TMPDIR:-/tmp}/kpa_aw_names.XXXXXX")
  printf '%s\n' "$names" > "$listfile"
  while IFS= read -r name; do
    [ -z "$name" ] && continue
    n=$((n+1))
    if [ "$REVERT" = 1 ]; then
      revert_kv "$RA_CONFIG/Flycast/$name.cfg" video_font_enable ""
    else
      set_kv "$RA_CONFIG/Flycast/$name.cfg" video_font_enable false
    fi
  done < "$listfile"
  rm -f "$listfile"
  say "      共 $n 个游戏配置已处理"
  say "      副作用：该平台不再显示存档/快进/截图等 OSD 提示；需要时改回 true 即可。"
}

say "=== KPA 实机体验修复（$( [ "$APPLY" = 1 ] && echo 写入模式 || ([ "$REVERT" = 1 ] && echo 回滚模式 || echo dry-run) )）==="
case "$ACTION" in
  dos)     fix_dos ;;
  nds)     fix_nds ;;
  flycast) fix_flycast ;;
  aw-osd)  fix_aw_osd ;;
  p2)      fix_p2 ;;
  all)     fix_dos; echo; fix_nds; echo; fix_flycast; echo; fix_aw_osd; echo; fix_p2 ;;
  *)       echo "用法: $0 <dos|nds|flycast|aw-osd|p2|all> [--apply|--revert]"; exit 2 ;;
esac

echo
if [ "$APPLY" = 1 ] && [ "$REVERT" = 0 ]; then
  say "完成。任选一种方式让改动生效："
  say "  1) 掌机上重新进一次对应游戏（per-game cfg 在加载时读取）；"
  say "  2) 或：adb shell am force-stop $RA_PKG 后再启动。"
  say "回滚：bash $0 $ACTION --revert"
fi
