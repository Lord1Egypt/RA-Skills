#!/bin/bash
# ============================================
# 磁盘健康哨兵 - 每日检查 sda(8T HDD) + nvme0n1(NVMe) SMART 关键指标
# 用法：Hermes cron no_agent 模式：stdout 空=健康静默，非空=推送告警
# 阈值：温度>=55 | 重映射/待映射/离线>0 | Command_Timeout 环比增长 | SMART FAILED
# 周自检闭环：周日触发 short selftest（距上次>144h），FAILED 即告警
# 本机 2026-09-04 实测通过，基线文件 ~/.hermes/scripts/disk_smart_baseline.txt
# ============================================
BASELINE="/home/<user>/.hermes/scripts/disk_smart_baseline.txt"
ALERT=""

# ---------- sda 机械盘 ----------
OVERALL=$(sudo smartctl -H /dev/sda 2>/dev/null | grep -E 'PASSED|FAILED' | awk '{print $NF}')
TEMP=$(sudo smartctl -A /dev/sda 2>/dev/null | awk '/Temperature_Celsius/{print $10}')
REALLOC=$(sudo smartctl -A /dev/sda 2>/dev/null | awk '/Reallocated_Sector_Ct/{print $10}')
PENDING=$(sudo smartctl -A /dev/sda 2>/dev/null | awk '/Current_Pending_Sector/{print $10}')
OFFLINE=$(sudo smartctl -A /dev/sda 2>/dev/null | awk '/Offline_Uncorrectable/{print $10}')
CTIMEOUT=$(sudo smartctl -A /dev/sda 2>/dev/null | awk '/Command_Timeout/{print $10}')
POH=$(sudo smartctl -A /dev/sda 2>/dev/null | awk '/Power_On_Hours/{print $10}')

if [ "$OVERALL" != "PASSED" ]; then ALERT="$ALERT\n[CRIT] sda SMART 总评=$OVERALL"; fi
if [ -n "$TEMP" ] && [ "$TEMP" -ge 55 ] 2>/dev/null; then ALERT="$ALERT\n[WARN] sda 温度=${TEMP}C (阈值55)"; fi
if [ -n "$REALLOC" ] && [ "$REALLOC" -gt 0 ] 2>/dev/null; then ALERT="$ALERT\n[CRIT] sda 重映射扇区=$REALLOC"; fi
if [ -n "$PENDING" ] && [ "$PENDING" -gt 0 ] 2>/dev/null; then ALERT="$ALERT\n[CRIT] sda 待映射扇区=$PENDING"; fi
if [ -n "$OFFLINE" ] && [ "$OFFLINE" -gt 0 ] 2>/dev/null; then ALERT="$ALERT\n[CRIT] sda 离线不可校正=$OFFLINE"; fi

# Command_Timeout 环比：读基线，当前 > 基线则告警并更新基线
PREV_CT=$( [ -f "$BASELINE" ] && grep 'sda_ctimeout' "$BASELINE" | awk '{print $2}' || echo 0 )
if [ -n "$CTIMEOUT" ] && [ -n "$PREV_CT" ] && [ "$CTIMEOUT" -gt "$PREV_CT" ] 2>/dev/null; then
  ALERT="$ALERT\n[WARN] sda Command_Timeout 增长: $PREV_CT -> $CTIMEOUT"
fi

# ---------- nvme0n1（awk 字段位：Temperature $2 / Percentage Used $3 / Errors $6 / Warning $3，必须 ^ 锚定） ----------
N_TEMP=$(sudo smartctl -A /dev/nvme0n1 2>/dev/null | awk '/^Temperature:/{print $2}')
N_USED=$(sudo smartctl -A /dev/nvme0n1 2>/dev/null | awk '/^Percentage Used/{print $3}' | tr -d '%')
N_ERR=$(sudo smartctl -A /dev/nvme0n1 2>/dev/null | awk '/^Media and Data Integrity Errors/{print $6}')
N_CRIT=$(sudo smartctl -A /dev/nvme0n1 2>/dev/null | awk '/^Critical Warning/{print $3}')

if [ "$N_CRIT" != "0x00" ] && [ -n "$N_CRIT" ] 2>/dev/null; then ALERT="$ALERT\n[CRIT] NVMe Critical Warning=$N_CRIT"; fi
if [ -n "$N_USED" ] && [ "$N_USED" -ge 80 ] 2>/dev/null; then ALERT="$ALERT\n[WARN] NVMe 磨损=$N_USED% (阈值80)"; fi
if [ -n "$N_ERR" ] && [ "$N_ERR" -gt 0 ] 2>/dev/null; then ALERT="$ALERT\n[CRIT] NVMe 数据完整性错误=$N_ERR"; fi

# ---------- sda 周自检自动闭环 ----------
# 规则：最近一次 short test 完成时间距今 >144h 且今天为周日 → 触发新自检
#       selftest 最近记录含 FAILED → 告警
DOW=$(date +%u)
LAST_TEST=$(sudo smartctl -l selftest /dev/sda 2>/dev/null | grep -E 'Short|Conveyance|Extended' | head -1)
LAST_TEST_HRS=$(echo "$LAST_TEST" | awk '{print $(NF-2)}' | tr -d '#')
if echo "$LAST_TEST" | grep -qiE 'failed|read failure'; then
  ALERT="$ALERT\n[CRIT] sda 上次自检异常: $LAST_TEST"
fi
if [ "$DOW" = "7" ]; then
  if [ -z "$LAST_TEST_HRS" ] || [ "$LAST_TEST_HRS" -gt 144 ] 2>/dev/null; then
    sudo smartctl -t short /dev/sda >/dev/null 2>&1
    echo "sda 周自检已触发 $(date '+%m-%d %H:%M')" >> "$BASELINE"
  fi
fi

# ---------- 更新基线 ----------
mkdir -p "$(dirname "$BASELINE")"
echo "sda_ctimeout $CTIMEOUT" > "$BASELINE"
echo "sda_realloc $REALLOC" >> "$BASELINE"
echo "sda_pending $PENDING" >> "$BASELINE"
echo "nvme_used $N_USED" >> "$BASELINE"

# ---------- 输出（空=健康静默） ----------
if [ -n "$ALERT" ]; then
  echo "磁盘健康告警 $(date '+%Y-%m-%d %H:%M')"
  echo "sda: temp=${TEMP}C realloc=$REALLOC pending=$PENDING offline=$OFFLINE ctimeout=$CTIMEOUT poh=${POH}h"
  echo "nvme: temp=${N_TEMP}C used=${N_USED}% err=$N_ERR critical=$N_CRIT"
  echo -e "$ALERT"
fi
