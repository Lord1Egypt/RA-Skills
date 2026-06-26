#!/bin/bash

# OpenClaw 每日自检脚本 v2
# 支持：历史记录 + 预警机制

LOG_FILE="/tmp/guardian_history.log"
THRESHOLD_MEM=80
THRESHOLD_DISK=80

REPORT="🛡️ OpenClaw 每日自检\n"
REPORT+="时间: $(date '+%Y-%m-%d %H:%M')\n"
REPORT+="----------------\n"

# 1. 外部守护
if crontab -l 2>/dev/null | grep -q "openclaw-gateway"; then
    REPORT+="✅ Cron 守护: 已配置\n"
else
    REPORT+="❌ Cron 守护: 未配置\n"
fi

# 2. Gateway 进程
if pgrep -f "openclaw-gateway" > /dev/null; then
    REPORT+="✅ Gateway: 运行中\n"
else
    REPORT+="❌ Gateway: 已停止\n"
fi

# 3. 系统资源 + 预警
# 系统输出中文，需要转换
MEM_TOTAL=$(free | grep "内存：" | awk '{print $2}')
MEM_USED=$(free | grep "内存：" | awk '{print $3}')
if [ -n "$MEM_TOTAL" ] && [ "$MEM_TOTAL" -gt 0 ]; then
    MEM_PCT=$((MEM_USED * 100 / MEM_TOTAL))
else
    MEM_PCT=0
fi

DISK_USED=$(df -h / | tail -1 | awk '{print int($5)}')

# 内存检查
if [ "$MEM_PCT" -ge "$THRESHOLD_MEM" ]; then
    REPORT+="⚠️ 内存: ${MEM_PCT}% (超过 ${THRESHOLD_MEM}% 阈值)\n"
else
    REPORT+="✅ 内存: ${MEM_PCT}%\n"
fi

# 磁盘检查
if [ "$DISK_USED" -ge "$THRESHOLD_DISK" ]; then
    REPORT+="⚠️ 磁盘: ${DISK_USED}% (超过 ${THRESHOLD_DISK}% 阈值)\n"
else
    REPORT+="✅ 磁盘: ${DISK_USED}%\n"
fi

# 4. Skills 检查（只显示差异）
SKILL_COUNT=$(ls -d ~/.openclaw/skills/*/ 2>/dev/null | wc -l)
SKILLS_TODAY=$(ls -d ~/.openclaw/skills/*/ 2>/dev/null | xargs -n1 basename | sort | tr '\n' ',' | sed 's/,$//')
SKILLS_YESTERDAY_FILE="/tmp/guardian_skills_yesterday.txt"

# 对比昨天
if [ -f "$SKILLS_YESTERDAY_FILE" ]; then
    SKILLS_YESTERDAY=$(cat "$SKILLS_YESTERDAY_FILE")
    
    # 转换为数组对比
    OLD_IFS=$IFS
    IFS=','
    read -ra OLD_SKILLS <<< "$SKILLS_YESTERDAY"
    read -ra NEW_SKILLS <<< "$SKILLS_TODAY"
    IFS=$OLD_IFS
    
    # 找出新增和丢失
    LOST=""
    ADDED=""
    for s in "${OLD_SKILLS[@]}"; do
        if [[ ! ",${SKILLS_TODAY}," == *",$s,"* ]]; then
            LOST="$LOST $s"
        fi
    done
    for s in "${NEW_SKILLS[@]}"; do
        if [[ ! ",${SKILLS_YESTERDAY}," == *",$s,"* ]]; then
            ADDED="$ADDED $s"
        fi
    done
    
    if [ -n "$LOST" ] || [ -n "$ADDED" ]; then
        [ -n "$LOST" ] && REPORT+="⚠️ Skills 丢失:$LOST\n"
        [ -n "$ADDED" ] && REPORT+="✅ Skills 新增:$ADDED\n"
    else
        REPORT+="✅ Skills: $SKILL_COUNT 个\n"
    fi
else
    REPORT+="✅ Skills: $SKILL_COUNT 个\n"
fi

# 保存今天的 skills 用于明天对比
echo "$SKILLS_TODAY" > "$SKILLS_YESTERDAY_FILE"

# 5. 历史趋势（最近 7 天）
REPORT+="----------------\n"
REPORT+="📈 历史趋势 (最近 7 天):\n"
if [ -f "$LOG_FILE" ]; then
    tail -7 "$LOG_FILE" | while read -r line; do
        REPORT+="  $line\n"
    done
else
    REPORT+="  暂无历史数据\n"
fi

# 判断状态
if echo "$REPORT" | grep -q "⚠️\|❌"; then
    REPORT+="----------------\n"
    REPORT+="状态: ⚠️ 需要关注\n"
else
    REPORT+="----------------\n"
    REPORT+="状态: 正常 ✅\n"
fi

# 保存到历史记录
echo "$(date '+%m-%d') 内存:${MEM_PCT}% 磁盘:${DISK_USED}%" >> "$LOG_FILE"

# 只保留最近 30 天
if [ -f "$LOG_FILE" ]; then
    tail -30 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
fi

echo -e "$REPORT"
