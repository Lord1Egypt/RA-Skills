#!/bin/bash
# one-mail 邮件统计脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# 参数解析
ACCOUNT=""
DAYS=7

while [[ $# -gt 0 ]]; do
    case $1 in
        --account)
            ACCOUNT="$2"
            shift 2
            ;;
        --days)
            DAYS="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 加载配置
load_config

echo "📊 邮件统计报告"
echo "================"
echo ""
echo "统计周期: 最近 $DAYS 天"
echo ""

# 获取邮件数据
if [ -n "$ACCOUNT" ]; then
    emails=$(bash "$SCRIPT_DIR/fetch.sh" --account "$ACCOUNT" --limit 500)
else
    emails=$(bash "$SCRIPT_DIR/fetch.sh" --limit 500)
fi

# 计算日期范围
cutoff_date=$(date -v-${DAYS}d +%Y-%m-%d 2>/dev/null || date -d "$DAYS days ago" +%Y-%m-%d)

# 过滤日期范围内的邮件
recent_emails=$(echo "$emails" | jq --arg cutoff "$cutoff_date" '[.[] | select(.date >= $cutoff)]')

# 总邮件数
total_count=$(echo "$recent_emails" | jq 'length')
echo "📧 总邮件数: $total_count"
echo ""

# 按账户统计
echo "📊 按账户统计:"
echo "$recent_emails" | jq -r 'group_by(.account) | .[] | "  \(.[0].account): \(length) 封"'
echo ""

# 未读邮件数
unread_count=$(echo "$recent_emails" | jq '[.[] | select(.unread)] | length')
echo "📬 未读邮件: $unread_count"
echo ""

# 有附件的邮件数
attachment_count=$(echo "$recent_emails" | jq '[.[] | select(.has_attachments)] | length')
echo "📎 带附件邮件: $attachment_count"
echo ""

# 按日期统计
echo "📅 按日期统计:"
echo "$recent_emails" | jq -r '[.[] | .date | split("T")[0]] | group_by(.) | .[] | "  \(.[0]): \(length) 封"' | tail -7
echo ""

# Top 10 发件人
echo "👥 Top 10 发件人:"
echo "$recent_emails" | jq -r '[.[] | .from] | group_by(.) | sort_by(length) | reverse | .[:10] | .[] | "  \(.[0]): \(length) 封"'
echo ""

# 按小时统计（活跃时段）
echo "⏰ 邮件活跃时段:"
echo "$recent_emails" | jq -r '[.[] | .date | split("T")[1] | split(":")[0]] | group_by(.) | sort_by(.[0]) | .[] | "  \(.[0]):00 - \(length) 封"'
echo ""

# 平均每天邮件数
avg_per_day=$(echo "scale=1; $total_count / $DAYS" | bc)
echo "📈 平均每天: $avg_per_day 封"
echo ""

# 生成图表（简单的文本图表）
echo "📊 每日邮件趋势:"
echo "$recent_emails" | jq -r '[.[] | .date | split("T")[0]] | group_by(.) | .[] | {date: .[0], count: length}' | \
    jq -r '"  \(.date): \("█" * (.count / 2)[:20]) (\(.count))"'
echo ""

echo "✅ 统计完成"
