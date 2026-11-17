#!/bin/bash
# KPA 天马 + RetroArch + PPSSPP 一键安装（幂等编排 + 前置体检 + 备份 + 验收报告）
#
# 这是「通用安装」入口：只跑在任意一台 KPA 上都成立的 7 个幂等步骤。
# ⚠️ 针对特定机器数据的一次性修复（热门置顶 / DOS 同名 conf / GBA 真盒绘回填 /
#    《光明力量》ZIP 伪装解包 / 《大唐英雄传》GAME.IMG 补字节 / 土星坏 CHD 删除）
#    不属于通用安装，禁止塞进本脚本；按 references/PLAYBOOK.md §18–§19 单独处理。
#
# 用法：
#   bash kpa_oneclick.sh                 # 完整安装（先体检 → 备份 → 7 步 → 清缓存 → 校验 → 报告）
#   bash kpa_oneclick.sh --dry-run      # 只做只读体检 + 打印计划，不写设备
#   bash kpa_oneclick.sh --verify-only  # 只做全库静态校验 + 出报告
#   bash kpa_oneclick.sh --steps 3,4    # 只跑指定步骤（调试用，仍会备份）
#   bash kpa_oneclick.sh --no-backup    # 跳过备份（不建议）
#
# 环境变量：KPA_ADB / KPA_TF / KPA_WORKDIR（覆盖默认工作目录）
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$HERE/.." && pwd)"
source "$HERE/kpa_env.sh"

WORK="${KPA_WORKDIR:-$HOME/WorkBuddy/kpa-oneclick}"
TS="$(date +%Y%m%d-%H%M%S)"
RUN="$WORK/$TS"
LOG="$RUN/oneclick.log"

MODE="full"; STEPS=""; DO_BACKUP=1
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)     MODE="dry"; shift ;;
    --verify-only) MODE="verify"; shift ;;
    --steps)       STEPS="$2"; shift 2 ;;
    --no-backup)   DO_BACKUP=0; shift ;;
    -h|--help)     sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "未知参数: $1" >&2; exit 2 ;;
  esac
done

mkdir -p "$RUN"
exec > >(tee "$LOG") 2>&1

say() { printf '\n\033[1;36m== %s ==\033[0m\n' "$*"; }
ok()  { printf '  \033[1;32mOK\033[0m    %s\n' "$*"; }
warn(){ printf '  \033[1;33mWARN\033[0m  %s\n' "$*"; }
die() { printf '\n\033[1;31mERROR\033[0m %s\n' "$*" >&2; exit 1; }

STEPS_ALL=(step1_apps.sh step2_theme.sh step3_ra.sh step4_metadata.sh \
           step5_ppsspp.sh step6_cleanup.sh step7_verify.sh)

say "KPA 一键安装 · $MODE"
echo "时间      : $(date '+%F %T %Z')"
echo "skill     : $SKILL_DIR"
echo "工作目录  : $RUN"
echo "adb       : $ADB"
echo "TF 卡     : $TF"

# ── 阶段 0：只读前置体检 ────────────────────────────────────────────
say "阶段 0 / 前置体检（只读）"

[ -x "$ADB" ] || die "adb 不可执行，请设置 KPA_ADB=/path/to/adb"
ok "adb 可执行"

STATE="$("$ADB" get-state 2>/dev/null || true)"
if [ "$STATE" != "device" ]; then
  if [ "$MODE" = "dry" ]; then
    warn "设备未连接（dry-run 仍可预览计划）；正式执行前需 USB 连接授权，或 adb connect <ip>:5555"
    SERIAL="(offline)"
  else
    die "未检测到 KPA（adb devices 需显示 device）。USB 连接并授权调试，或 adb connect <ip>:5555"
  fi
else
  SERIAL="$("$ADB" get-serialno 2>/dev/null | tr -d '\r')"
  ok "设备在线  serial=$SERIAL"
fi

if [ "$STATE" = "device" ]; then
  sh "test -d '$TF/Roms'" >/dev/null 2>&1 || die "TF 卡路径 $TF/Roms 不存在；用 KPA_TF 覆盖（禁令：不同机型挂载点不同）"
  N_META="$(sh "find '$TF/Roms' -name metadata.pegasus.txt -type f 2>/dev/null | wc -l" | tr -d '\r[:space:]')"
  ok "TF 卡可读  metadata=$N_META 份"
else
  warn "跳过 TF 卡与 metadata 检查（设备离线）"
fi

# 必备资源完整性（缺一个都会让用户在半路失败，提前拦住）
MISSING=0
for f in SKILL.md assets/golden/retroarch.cfg.txt assets/golden/ppsspp.ini.txt \
         assets/data/platform_cores.tsv.txt assets/data/mame_orient.json; do
  if [ ! -f "$SKILL_DIR/$f" ]; then warn "缺少资源 $f（对应步骤可能 SKIP）"; MISSING=$((MISSING+1)); fi
done
for s in "${STEPS_ALL[@]}"; do [ -f "$HERE/$s" ] || { warn "缺少步骤脚本 $s"; MISSING=$((MISSING+1)); }; done
[ "$MISSING" -eq 0 ] && ok "资源与 7 步脚本齐全" || warn "缺 $MISSING 项，仍可继续（缺项步骤会 SKIP 或报错中止）"

# 本机磁盘余量（备份要写 metadata 与配置）
FREE_MB=$(df -m "$WORK" 2>/dev/null | awk 'NR==2{print $4}')
[ "${FREE_MB:-0}" -ge 200 ] || warn "本机可用空间 ${FREE_MB:-?}MB 偏少，建议 ≥200MB"
ok "本机可用 ${FREE_MB:-?}MB"

# 打印护栏：这几条是本项目真实踩过的坑
say "护栏（违反过，已在实机造成故障）"
cat <<'GUARD'
  1  改 metadata / 新增目录后，必须删 dataCache.json 并重启天马 → 本脚本阶段 3 自动完成
  2  adb 注入按键 RetroArch 全部不接收 → 实体键手感只能人手确认，脚本不会假装验证
  3  按键/配置改动只单点验证再推广 → 本脚本不含任何按键批量改写
  4  静态引用 0 缺失 ≠ 封面看得见 → 视觉类必须实机截货架
  5  设备删除无废纸篓 → 阶段 1 先做配置级备份，删 ROM 前请另做整机备份
  6  禁止 am force-stop com.ayaneo.home → 会让系统按键全部失灵，只能关机重启恢复
GUARD

if [ "$MODE" = "dry" ]; then
  say "DRY-RUN 计划（未写入设备）"
  if [ -n "$STEPS" ]; then
    IFS=',' read -ra IDX <<< "$STEPS"
    for i in "${IDX[@]}"; do echo "  step$i -> ${STEPS_ALL[$((i-1))]:-?}"; done
  else
    for i in "${!STEPS_ALL[@]}"; do echo "  step$((i+1)) -> ${STEPS_ALL[$i]}"; done
  fi
  echo "  备份 -> $RUN/backup/"
  echo "  清 dataCache.json + 重启天马"
  echo "  静态校验 + 报告 -> $RUN/report.md"
  ok "DRY-RUN 完成：体检通过，可以执行 bash $0"
  exit 0
fi

# ── 阶段 1：配置级备份（回滚点） ─────────────────────────────────────
if [ "$DO_BACKUP" -eq 1 ] && [ "$MODE" = "full" ]; then
  say "阶段 1 / 配置级备份（回滚点）"
  BK="$RUN/backup"; mkdir -p "$BK/meta" "$BK/cfg"
  DEV_BK="/sdcard/backup/kpa-oneclick-$TS"
  sh "mkdir -p '$DEV_BK'; cp '$TF/Roms/'*/metadata.pegasus.txt '$DEV_BK/' 2>/dev/null; echo ok" >/dev/null 2>&1 || true
  sh "find '$TF/Roms' -name metadata.pegasus.txt -type f" 2>/dev/null | tr -d '\r' | while IFS= read -r p; do
    [ -n "$p" ] || continue
    plat="$(basename "$(dirname "$p")")"
    "$ADB" exec-out cat "$p" > "$BK/meta/$plat.txt" 2>/dev/null || true
  done
  for pair in \
    "$INT/Android/data/$RA_PKG/files/retroarch.cfg|retroarch.cfg" \
    "$INT/Android/data/$PPS_PKG/files/PSP/SYSTEM/ppsspp.ini|ppsspp.ini" \
    "/sdcard/pegasus-frontend/settings.txt|settings.txt"; do
    src="${pair%%|*}"; dst="${pair##*|}"
    sh "test -f '$src'" >/dev/null 2>&1 && "$ADB" exec-out cat "$src" > "$BK/cfg/$dst" 2>/dev/null || true
  done
  "$ADB" pull /sdcard/RetroArch/playlists "$BK/playlists" >/dev/null 2>&1 || true
  ok "本机回滚点 $BK（meta $(find "$BK/meta" -type f | wc -l | tr -d ' ') 份）"
  ok "设备侧同步副本 $DEV_BK"
else
  warn "跳过备份（--verify-only / --no-backup）"
fi

# ── 阶段 2：7 步幂等安装 ────────────────────────────────────────────
RESULTS=()
if [ "$MODE" = "full" ]; then
  say "阶段 2 / 7 步幂等安装"
  if [ -n "$STEPS" ]; then
    IFS=',' read -ra IDX <<< "$STEPS"
  else
    IDX=(1 2 3 4 5 6 7)
  fi
  for i in "${IDX[@]}"; do
    i=$((i)); [ "$i" -ge 1 ] && [ "$i" -le 7 ] || die "步骤号越界: $i"
    s="${STEPS_ALL[$((i-1))]}"
    echo; echo ">>> step$i  $s"
    if bash "$HERE/$s"; then
      RESULTS+=("step$i $s OK")
      ok "step$i 完成"
    else
      RESULTS+=("step$i $s FAILED")
      die "step$i ($s) 失败。已中止；修复后可原样重跑本脚本（幂等），回滚点在 $RUN/backup"
    fi
  done
else
  warn "verify-only：跳过 7 步安装"
fi

# ── 阶段 3：清缓存并重启天马（禁令 3） ──────────────────────────────
if [ "$MODE" = "full" ]; then
  say "阶段 3 / 清 dataCache.json 并重启天马"
  sh "am force-stop $PEG_PKG; rm -f /sdcard/pegasus-frontend/dataCache.json" >/dev/null 2>&1 || true
  sh "monkey -p $PEG_PKG -c android.intent.category.LAUNCHER 1" >/dev/null 2>&1 || true
  sleep 8
  sh "test -f /sdcard/pegasus-frontend/dataCache.json" >/dev/null 2>&1 \
    && ok "dataCache.json 已重建" || warn "缓存尚未重建（天马可能还在扫描，稍后自行确认）"
fi

# ── 阶段 4：全库静态校验 ────────────────────────────────────────────
say "阶段 4 / 全库静态校验（只读）"
if bash "$HERE/kpa_health_check.sh" > "$RUN/health.txt" 2>&1; then
  tail -25 "$RUN/health.txt"
  ok "静态校验通过，全文 $RUN/health.txt"
else
  warn "静态校验有告警，全文 $RUN/health.txt"
  tail -25 "$RUN/health.txt"
fi

# ── 阶段 5：验收报告（含「必须人手确认」清单） ──────────────────────
say "阶段 5 / 生成验收报告"
REPORT="$RUN/report.md"
{
  echo "# KPA 一键安装验收报告"
  echo
  echo "- 时间：$(date '+%F %T %Z')"
  echo "- 设备：$SERIAL"
  echo "- skill：kpa-pegasus-setup（$SKILL_DIR）"
  echo "- 模式：$MODE"
  echo "- 回滚点：$RUN/backup（设备侧 /sdcard/backup/kpa-oneclick-$TS）"
  echo
  echo "## 执行结果"
  echo '```'
  for r in "${RESULTS[@]:-}"; do [ -n "$r" ] && echo "$r"; done
  echo '```'
  echo
  echo "## 静态校验摘要"
  echo '```'
  tail -20 "$RUN/health.txt" 2>/dev/null || echo "(无)"
  echo '```'
  echo
  echo "## 必须人手实机确认（adb 无法代替）"
  cat <<'MANUAL'
  1. 所有实体按键手感：街机 CPS1/CPS3、ATOMISWAVE 竖版、PPSSPP/PS ABXY、N64 方向键
     —— RetroArch 直接 poll evdev，adb input keyevent / tap 全部无效，只有 BACK(4) 能呼出菜单
  2. DOSBox-Pure 核心菜单内的操作（本包用同名 .conf 的 [autoexec] 已绕开「选 exe」）
  3. 封面 / 遮罩在货架上的真实观感：切到该平台截一张图，确认中文名没被裁、没有空白格
  4. 每个平台各冷启动 1 款游戏（8–26 秒才算黑屏；汉化破解版可能有 60 秒以上片头）
  5. 从游戏按 select+B 能否退回天马对应平台页面
MANUAL
  echo
  echo "## 已知边界"
  cat <<'BOUND'
  - 主题二进制包（prosperoOS + 背景图）不随文本版分发，step2 会打印获取指引并 SKIP
  - 遮罩 PNG / BIOS / ROM / APK 均不随包分发（版权与体积），按 SKILL.md「按需读取」补齐
  - 本机曾验证的基线：35 平台 / 3706 条、ROM 与封面引用各 3706、缺失 0
    —— 这是那台实机的数字，不是新机的通过标准；请以本机 health.txt 的实际结果为准
  - 针对特定机器数据的一次性修复不属于通用安装，见 references/PLAYBOOK.md §18–§19
BOUND
  echo
  echo "## 失败/回滚"
  echo '```'
  echo "# 值级还原单个文件（推荐，别整份覆盖 metadata）"
  echo "adb push $RUN/backup/meta/<平台>.txt $TF/Roms/<平台>/metadata.pegasus.txt"
  echo "# 改完必须清缓存"
  echo "adb shell 'am force-stop $PEG_PKG; rm -f /sdcard/pegasus-frontend/dataCache.json'"
  echo '```'
} > "$REPORT"
ok "报告 $REPORT"

say "完成"
echo "  日志   : $LOG"
echo "  报告   : $REPORT"
echo "  回滚点 : $RUN/backup"
echo
echo "⚠️  安装完成 ≠ 已验收。报告里「必须人手实机确认」5 项请逐条在掌机上过一遍。"
