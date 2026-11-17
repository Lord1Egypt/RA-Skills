#!/bin/bash
# 统一修正竖版街机 per-game cfg。
# 规则（2026-11-14 实机验证）：video_rotation 必须为 "3"，
# 方向映射固定 up=h0right / down=h0left / left=h0up / right=h0down。
# 若 rotation 为 "1"，画面逆时针转 90°，与这套映射差 180°，方向全反 —— 这是历史 bug。
# 默认 dry-run；加 --apply 才写入。加 --keys 同时校验/恢复厂商按键基线（a=109/b=108/start=97/select=96，且无 x/y 行）。
set -euo pipefail
source "$(dirname "$0")/kpa_env.sh"
require_device

APPLY=0
KEYS=0
for a in "$@"; do
    case "$a" in
        --apply) APPLY=1 ;;
        --keys)  KEYS=1 ;;
    esac
done
[ "$APPLY" = "1" ] || echo "DRY-RUN：仅报告，不写入。确认后加 --apply 重跑。"

cat > /tmp/kpa_vertical_dev.sh <<'EOS'
#!/system/bin/sh
APPLY="$1"
KEYS="$2"
BASE=/sdcard/RetroArch/config
total=0; badrot=0; badmap=0; badkey=0; changed=0

for D in "$BASE"/*/; do
    [ -d "$D" ] || continue
    for f in "$D"*.cfg; do
        [ -f "$f" ] || continue
        case "$(basename "$f")" in *" "*) continue ;; esac
        grep -q '^video_rotation' "$f" || continue
        total=$((total+1))

        rot=$(grep -m1 '^video_rotation' "$f" | sed 's/.*= "//; s/"//')
        u=$(grep -m1 '^input_player1_up_btn' "$f" | sed 's/.*= "//; s/"//')
        d=$(grep -m1 '^input_player1_down_btn' "$f" | sed 's/.*= "//; s/"//')
        l=$(grep -m1 '^input_player1_left_btn' "$f" | sed 's/.*= "//; s/"//')
        r=$(grep -m1 '^input_player1_right_btn' "$f" | sed 's/.*= "//; s/"//')
        a=$(grep -m1 '^input_player1_a_btn' "$f" | sed 's/.*= "//; s/"//')
        st=$(grep -m1 '^input_player1_start_btn' "$f" | sed 's/.*= "//; s/"//')

        need=0
        [ "$rot" = "3" ] || { badrot=$((badrot+1)); need=1; }
        if [ "$u" != "h0right" ] || [ "$d" != "h0left" ] || [ "$l" != "h0up" ] || [ "$r" != "h0down" ]; then
            badmap=$((badmap+1)); need=1
        fi
        b=$(grep -m1 '^input_player1_b_btn' "$f" | sed 's/.*= "//; s/"//')
        se=$(grep -m1 '^input_player1_select_btn' "$f" | sed 's/.*= "//; s/"//')
        xy=$(grep -c '^input_player1_[xy]_btn' "$f" || true)
        if [ "$KEYS" = "1" ]; then
            # 厂商基线（用户 2026-11-12 验收）：a=109 b=108 start=97 select=96，且不得有 x/y 行
            if [ "$a" != "109" ] || [ "$b" != "108" ] || [ "$st" != "97" ] || [ "$se" != "96" ] || [ "$xy" != "0" ]; then
                badkey=$((badkey+1)); need=1
            fi
        fi

        if [ "$need" = "1" ]; then
            if [ "$APPLY" = "1" ]; then
                sed -i \
                    -e 's/^video_rotation = .*/video_rotation = "3"/' \
                    -e 's/^input_player1_up_btn = .*/input_player1_up_btn = "h0right"/' \
                    -e 's/^input_player1_down_btn = .*/input_player1_down_btn = "h0left"/' \
                    -e 's/^input_player1_left_btn = .*/input_player1_left_btn = "h0up"/' \
                    -e 's/^input_player1_right_btn = .*/input_player1_right_btn = "h0down"/' \
                    "$f"
                if [ "$KEYS" = "1" ]; then
                    sed -i \
                        -e 's/^input_player1_a_btn = .*/input_player1_a_btn = "109"/' \
                        -e 's/^input_player1_b_btn = .*/input_player1_b_btn = "108"/' \
                        -e 's/^input_player1_start_btn = .*/input_player1_start_btn = "97"/' \
                        -e 's/^input_player1_select_btn = .*/input_player1_select_btn = "96"/' \
                        -e '/^input_player1_x_btn/d' \
                        -e '/^input_player1_y_btn/d' \
                        "$f"
                fi
            else
                [ "$changed" -lt 12 ] && echo "  fix: $(basename "$f") rot=$rot up=$u left=$l"
            fi
            changed=$((changed+1))
        fi
    done
done

echo "RESULT total=$total bad_rotation=$badrot bad_mapping=$badmap bad_keys=$badkey need_fix=$changed apply=$APPLY keys=$KEYS"
EOS

"$ADB" push /tmp/kpa_vertical_dev.sh /sdcard/kpa_vertical_dev.sh >/dev/null
sh "sh /sdcard/kpa_vertical_dev.sh $APPLY $KEYS"
sh "rm -f /sdcard/kpa_vertical_dev.sh" >/dev/null
rm -f /tmp/kpa_vertical_dev.sh
[ "$APPLY" = "1" ] && echo "完成。验证：进 arkanoid，砖块应在屏幕右侧、挡板在左下；逆时针竖拿掌机画面正立、方向才对。"
exit 0
