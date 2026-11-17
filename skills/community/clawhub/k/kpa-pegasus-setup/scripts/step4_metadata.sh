#!/bin/bash
# step4: 为 TF 卡各平台 metadata 写入 launch 行 + 按方向库生成竖屏 per-game cfg（幂等）
source "$(dirname "$0")/kpa_env.sh"
require_device

CORES_TSV="$KPA_SKILL_DIR/assets/data/platform_cores.tsv.txt"
ORIENT="$KPA_SKILL_DIR/assets/data/mame_orient.json"

# 生成设备端脚本
cat > /tmp/kpa_step4_device.sh <<'EOS'
#!/system/bin/sh
TF="${1:-/storage/6AF3-384F}"
ROMS="$TF/Roms"
done_launch=0; done_cfg=0; missing_meta=0

launch_line() {
  # $1=核心文件名 → RA 直启 launch 行
  echo "launch: am start --user 0 -n com.retroarch.aarch64/com.retroarch.browser.retroactivity.RetroActivityFuture -e ROM \"{file.path}\" -e LIBRETRO /data/data/com.retroarch.aarch64/cores/$1 -e CONFIGFILE /storage/emulated/0/Android/data/com.retroarch.aarch64/files/retroarch.cfg"
}

# 1) metadata launch 行
while IFS='	' read -r plat core; do
  case "$plat" in ''|'#'*) continue;; esac
  m="$ROMS/$plat/metadata.pegasus.txt"
  if [ ! -f "$m" ]; then missing_meta=$((missing_meta+1)); continue; fi
  if grep -q '^launch:' "$m"; then continue; fi
  cp "$m" "$m.tmp0" 2>/dev/null
  { launch_line "$core"; cat "$m.tmp0"; } > "$m.tmp" && mv "$m.tmp" "$m"
  rm -f "$m.tmp0"
  echo "launch-line: $plat <- $core"
  done_launch=$((done_launch+1))
done < "/sdcard/kpa_platform_cores.tsv"

# 2) 竖屏 cfg（方向库 → rom 名）
# 把 JSON 转成 "romname orientation" 列表
sed -n 's/.*"\([a-z0-9_]*\)": *\["vertical", *[01]\].*/\1 vertical/p' /sdcard/kpa_mame_orient.json > /sdcard/kpa_vertical.txt
# DB 查不到的补充竖版
cat >> /sdcard/kpa_vertical.txt <<EXTRA
gekiridn vertical
tengaij vertical
p47mus vertical
schmeisr vertical
EXTRA

# rot 值：MAME 系(mame2003_plus: MAME/VARCADE)=1；FBAlpha 系(FBNEO/CPS1/2/3/NEOGEO)=3
for plat in MAME VARCADE; do
  d="$ROMS/$plat"
  [ -d "$d" ] || continue
  for rom in "$d"/*.zip "$d"/*.7z; do
    [ -e "$rom" ] || continue
    base=$(basename "$rom"); name=$(echo "${base%.*}" | tr 'A-Z' 'a-z')
    grep -q "^$name vertical$" /sdcard/kpa_vertical.txt || continue
    cfg="$d/${base%.*}.cfg"
    if [ ! -f "$cfg" ]; then
      cat > "$cfg" <<CFG
video_rotation = "1"
aspect_ratio_index = "0"
video_scale_integer = "false"
input_overlay_enable = "false"
input_player1_up_btn = "h0right"
input_player1_down_btn = "h0left"
input_player1_left_btn = "h0up"
input_player1_right_btn = "h0down"
input_player1_a_btn = "109"
input_player1_b_btn = "108"
input_player1_start_btn = "97"
input_player1_select_btn = "96"
CFG
      done_cfg=$((done_cfg+1))
    fi
  done
done
for plat in FBNEO CPS1 CPS2 CPS3 NEOGEO; do
  d="$ROMS/$plat"
  [ -d "$d" ] || continue
  for rom in "$d"/*.zip "$d"/*.7z; do
    [ -e "$rom" ] || continue
    base=$(basename "$rom"); name=$(echo "${base%.*}" | tr 'A-Z' 'a-z')
    grep -q "^$name vertical$" /sdcard/kpa_vertical.txt || continue
    cfg="$d/${base%.*}.cfg"
    if [ ! -f "$cfg" ]; then
      cat > "$cfg" <<CFG
video_rotation = "3"
aspect_ratio_index = "0"
video_scale_integer = "false"
input_overlay_enable = "false"
input_player1_up_btn = "h0right"
input_player1_down_btn = "h0left"
input_player1_left_btn = "h0up"
input_player1_right_btn = "h0down"
input_player1_a_btn = "109"
input_player1_b_btn = "108"
input_player1_start_btn = "97"
input_player1_select_btn = "96"
CFG
      done_cfg=$((done_cfg+1))
    fi
  done
done

rm -f /sdcard/kpa_vertical.txt
echo "RESULT launch_lines_added=$done_launch cfg_created=$done_cfg metadata_missing=$missing_meta"
EOS

"$ADB" push "$CORES_TSV" /sdcard/kpa_platform_cores.tsv >/dev/null
"$ADB" push "$ORIENT" /sdcard/kpa_mame_orient.json >/dev/null
"$ADB" push /tmp/kpa_step4_device.sh /sdcard/kpa_step4_device.sh >/dev/null
sh "sh /sdcard/kpa_step4_device.sh $TF"
sh "rm -f /sdcard/kpa_step4_device.sh /sdcard/kpa_platform_cores.tsv /sdcard/kpa_mame_orient.json" >/dev/null
echo "step4 done"
