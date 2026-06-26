#!/bin/bash

# github-notify.sh - GitHub 通知推送工具
#
# 功能：
# 1. 推送 GitHub 事件到 Discord
# 2. 推送到钉钉机器人
# 3. 推送到 Telegram
# 4. 推送到 Slack
# 5. 自定义通知模板
#
# 用法：
#   ./github-notify.sh discord [options]   # 推送到 Discord
#   ./github-notify.sh dingtalk [options]  # 推送到钉钉
#   ./github-notify.sh telegram [options]  # 推送到 Telegram
#   ./github-notify.sh slack [options]     # 推送到 Slack
#   ./github-notify.sh all [options]       # 推送到所有通道
#   ./github-notify.sh help                # 显示帮助

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 默认配置
DEFAULT_TEMPLATE="default"
DEFAULT_EMOJI=":github:"

# 显示帮助信息
show_help() {
    cat << EOF
GitHub 通知推送工具

用法：
  github-notify.sh [target] [options]

目标平台:
  discord     推送到 Discord
  dingtalk    推送到钉钉机器人
  telegram    推送到 Telegram
  slack       推送到 Slack
  all         推送到所有已配置的平台

选项:
  -t, --type      事件类型 (issue, pr, release, commit, workflow)
  -m, --message   自定义消息内容
  -s, --status    事件状态 (open, closed, merged, etc.)
  -u, --url       相关 URL
  -a, --author    作者
  -l, --label     标签
  -r, --repo      GitHub 仓库
  -n, --number    问题/PR 编号
  -T, --title     标题
  -d, --desc      描述
  -i, --icon      自定义图标
  -c, --color     自定义颜色
  -f, --file      从文件读取消息
  --dry-run       仅显示消息内容，不发送

事件类型:
  issue       问题创建/更新
  pr          PR 创建/更新/合并
  release     发布新版本
  commit      代码提交
  workflow    工作流状态

模板类型:
  default     默认模板
  compact     紧凑模板
  detailed    详细模板
  emoji       Emoji 模板

示例:
  github-notify.sh discord --type pr --status open --repo owner/repo
  github-notify.sh dingtalk --type issue --status open --number 123
  github-notify.sh all --type commit --title "New features"
  github-notify.sh telegram --message "测试消息"

前提条件：
  1. 安装 jq: brew install jq
  2. 配置 Webhook URL (参考 README)
  3. 已安装 gh CLI: brew install gh (可选)

EOF
    exit 0
}

# 检查 jq
check_jq() {
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}❌ 错误：jq 未安装${NC}"
        echo ""
        echo -e "${BLUE}安装方法:${NC}"
        echo "   brew install jq"
        exit 1
    fi
}

# 发送 Discord 消息
send_discord() {
    local webhook_url="${DISCORD_WEBHOOK_URL:-}"
    local title="${1:-}"
    local description="${2:-}"
    local color="${3:-3447003}"
    local icon="${4:-}"
    
    if [[ -z "$webhook_url" ]]; then
        echo -e "${YELLOW}⚠️  Discord Webhook URL 未配置${NC}"
        echo -e "${CYAN}[Discord] ${title}: ${description}${NC}"
        return 0
    fi
    
    local payload=$(cat << EOF
{
  "content": "",
  "embeds": [
    {
      "title": "${title}",
      "description": "${description}",
      "color": ${color},
      "thumbnail": {
        "url": "${icon:-https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png}"
      }
    }
  ]
}
EOF
)
    
    curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "$webhook_url" > /dev/null 2>&1
    
    echo -e "${GREEN}✅ Discord 消息已发送${NC}"
}

# 发送钉钉消息
send_dingtalk() {
    local webhook_url="${DINGTALK_WEBHOOK_URL:-}"
    local title="${1:-}"
    local description="${2:-}"
    local color="${3:-}"
    
    if [[ -z "$webhook_url" ]]; then
        echo -e "${YELLOW}⚠️  钉钉 Webhook URL 未配置${NC}"
        echo -e "${CYAN}[钉钉] ${title}: ${description}${NC}"
        return 0
    fi
    
    local payload=$(cat << EOF
{
  "msgtype": "markdown",
  "markdown": {
    "title": "${title}",
    "text": "### ${title}\n${description}\n\n---\n发送时间: $(date '+%Y-%m-%d %H:%M:%S')"
  }
}
EOF
)
    
    curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "$webhook_url" > /dev/null 2>&1
    
    echo -e "${GREEN}✅ 钉钉消息已发送${NC}"
}

# 发送 Telegram 消息
send_telegram() {
    local bot_token="${TELEGRAM_BOT_TOKEN:-}"
    local chat_id="${TELEGRAM_CHAT_ID:-}"
    local title="${1:-}"
    local description="${2:-}"
    
    if [[ -z "$bot_token" ]] || [[ -z "$chat_id" ]]; then
        echo -e "${YELLOW}⚠️  Telegram 配置不完整${NC}"
        echo -e "${CYAN}[Telegram] ${title}: ${description}${NC}"
        return 0
    fi
    
    local text=$(printf "%s\n%s" "$title" "$description")
    
    curl -s -X POST \
        "https://api.telegram.org/bot${bot_token}/sendMessage" \
        -d "chat_id=${chat_id}" \
        -d "text=${text}" > /dev/null 2>&1
    
    echo -e "${GREEN}✅ Telegram 消息已发送${NC}"
}

# 发送 Slack 消息
send_slack() {
    local webhook_url="${SLACK_WEBHOOK_URL:-}"
    local title="${1:-}"
    local description="${2:-}"
    local color="${3:-#36a64f}"
    
    if [[ -z "$webhook_url" ]]; then
        echo -e "${YELLOW}⚠️  Slack Webhook URL 未配置${NC}"
        echo -e "${CYAN}[Slack] ${title}: ${description}${NC}"
        return 0
    fi
    
    local payload=$(cat << EOF
{
  "attachments": [
    {
      "title": "${title}",
      "text": "${description}",
      "color": "${color}",
      "footer": "GitHub Notifications",
      "ts": "$(date +%s)"
    }
  ]
}
EOF
)
    
    curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "$webhook_url" > /dev/null 2>&1
    
    echo -e "${GREEN}✅ Slack 消息已发送${NC}"
}

# 发送通知
send_notification() {
    local target="${1:-}"
    local title="${2:-}"
    local description="${3:-}"
    local color="${4:-3447003}"
    local icon="${5:-}"
    
    case "$target" in
        discord)
            send_discord "$title" "$description" "$color" "$icon"
            ;;
        dingtalk)
            send_dingtalk "$title" "$description" "$color"
            ;;
        telegram)
            send_telegram "$title" "$description"
            ;;
        slack)
            send_slack "$title" "$description" "$color"
            ;;
        all)
            send_discord "$title" "$description" "$color" "$icon" &>/dev/null &
            send_dingtalk "$title" "$description" "$color" &
            send_telegram "$title" "$description" &
            send_slack "$title" "$description" "$color" &
            wait
            echo -e "${GREEN}✅ 所有平台消息已发送${NC}"
            ;;
        *)
            echo -e "${RED}❌ 未知目标：${target}${NC}"
            return 1
            ;;
    esac
}

# 生成 PR 通知
generate_pr_notification() {
    local number="${1:-}"
    local title="${2:-}"
    local state="${3:-}"
    local author="${4:-}"
    local repo="${5:-}"
    local url="${6:-}"
    local labels="${7:-}"
    local action="${8:-created}"
    
    local status_emoji=""
    [[ "$state" == "open" ]] && status_emoji="🟢"
    [[ "$state" == "closed" ]] && status_emoji="🔴"
    [[ "$action" == "merged" ]] && status_emoji="🟣"
    
    local labels_str=""
    if [[ -n "$labels" ]]; then
        labels_str=" | 🔖 $labels"
    fi
    
    local title_text="$status_emoji **#${number} ${title}**"
    
    local description="**作者**: @${author}
**仓库**: ${repo}
**状态**: ${state}
**操作**: ${action}${labels_str}

[查看 PR](${url})"

    local color="3447003"
    [[ "$state" == "closed" ]] && color="15158332"
    [[ "$action" == "merged" ]] && color="10181046"
    
    echo -e "${title_text}\n${description}"
    echo "::${color}::"
}

# 生成 Issue 通知
generate_issue_notification() {
    local number="${1:-}"
    local title="${2:-}"
    local state="${3:-}"
    local author="${4:-}"
    local repo="${5:-}"
    local url="${6:-}"
    local labels="${7:-}"
    local action="${8:-opened}"
    
    local status_emoji=""
    [[ "$state" == "open" ]] && status_emoji="🟢"
    [[ "$state" == "closed" ]] && status_emoji="🔴"
    
    local labels_str=""
    if [[ -n "$labels" ]]; then
        labels_str=" | 🔖 $labels"
    fi
    
    local title_text="$status_emoji **#${number} ${title}**"
    
    local description="**作者**: @${author}
**仓库**: ${repo}
**状态**: ${state}
**操作**: ${action}${labels_str}

[查看 Issue](${url})"

    local color="3447003"
    [[ "$state" == "closed" ]] && color="15158332"
    
    echo -e "${title_text}\n${description}"
    echo "::${color}::"
}

# 生成 Commit 通知
generate_commit_notification() {
    local sha="${1:-}"
    local message="${2:-}"
    local author="${3:-}"
    local repo="${4:-}"
    local url="${5:-}"
    local branch="${6:-}"
    
    local title_text=" \`git commit\` **${sha:0:7}** - ${message}"
    
    local description="**作者**: ${author}
**分支**: ${branch}
**仓库**: ${repo}

[查看提交](${url})"

    local color="7136896"
    
    echo -e "${title_text}\n${description}"
    echo "::${color}::"
}

# 生成 Release 通知
generate_release_notification() {
    local tag="${1:-}"
    local name="${2:-}"
    local author="${3:-}"
    local repo="${4:-}"
    local url="${5:-}"
    local prerelease="${6:-false}"
    
    local emoji="🎉"
    [[ "$prerelease" == "true" ]] && emoji="🧪"
    
    local title_text="${emoji} **发布新版本：${tag}**"
    
    local description="**发布者**: ${author}
**版本名称**: ${name}
**仓库**: ${repo}
**预发布**: ${prerelease}

[查看发布](${url})"

    local color="16752127"
    
    echo -e "${title_text}\n${description}"
    echo "::${color}::"
}

# 处理命令行参数
process_args() {
    local target="${1:-}"
    shift || true
    
    local repo=""
    local type=""
    local title=""
    local message=""
    local status=""
    local url=""
    local author=""
    local label=""
    local number=""
    local desc=""
    local icon=""
    local color=""
    local file=""
    local dry_run="false"
    
    # 解析选项
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -r|--repo)
                repo="$2"
                shift 2
                ;;
            -t|--type)
                type="$2"
                shift 2
                ;;
            -T|--title)
                title="$2"
                shift 2
                ;;
            -m|--message)
                message="$2"
                shift 2
                ;;
            -s|--status)
                status="$2"
                shift 2
                ;;
            -u|--url)
                url="$2"
                shift 2
                ;;
            -a|--author)
                author="$2"
                shift 2
                ;;
            -l|--label)
                label="$2"
                shift 2
                ;;
            -n|--number)
                number="$2"
                shift 2
                ;;
            -d|--desc)
                desc="$2"
                shift 2
                ;;
            -i|--icon)
                icon="$2"
                shift 2
                ;;
            -c|--color)
                color="$2"
                shift 2
                ;;
            -f|--file)
                file="$2"
                shift 2
                ;;
            --dry-run)
                dry_run="true"
                shift
                ;;
            --)
                shift
                break
                ;;
            *)
                break
                ;;
        esac
    done
    
    # 从文件读取消息
    if [[ -n "$file" ]] && [[ -f "$file" ]]; then
        message=$(cat "$file")
    fi
    
    # 确定通知类型
    local notification_type="${type:-custom}"
    
    # 生成通知内容
    local notification_title=""
    local notification_desc=""
    local notification_color="${color:-3447003}"
    
    case "$notification_type" in
        pr|pull_request)
            if [[ -z "$title" ]]; then
                title="新 PR"
            fi
            local result=$(generate_pr_notification "$number" "$title" "$status" "$author" "$repo" "$url" "$label" "${message:-created}")
            notification_title=$(echo "$result" | head -1)
            notification_desc=$(echo "$result" | tail -n +2 | head -1)
            notification_color=$(echo "$result" | grep "::" | cut -d':' -f2)
            ;;
        issue)
            if [[ -z "$title" ]]; then
                title="新 Issue"
            fi
            local result=$(generate_issue_notification "$number" "$title" "$status" "$author" "$repo" "$url" "$label" "${message:-opened}")
            notification_title=$(echo "$result" | head -1)
            notification_desc=$(echo "$result" | tail -n +2 | head -1)
            notification_color=$(echo "$result" | grep "::" | cut -d':' -f2)
            ;;
        commit)
            if [[ -z "$title" ]]; then
                title="新提交"
            fi
            local result=$(generate_commit_notification "$number" "$title" "$author" "$repo" "$url" "${label:-main}")
            notification_title=$(echo "$result" | head -1)
            notification_desc=$(echo "$result" | tail -n +2 | head -1)
            notification_color=$(echo "$result" | grep "::" | cut -d':' -f2)
            ;;
        release)
            if [[ -z "$title" ]]; then
                title="新发布"
            fi
            local result=$(generate_release_notification "$number" "$title" "$author" "$repo" "$url" "${label:-false}")
            notification_title=$(echo "$result" | head -1)
            notification_desc=$(echo "$result" | tail -n +2 | head -1)
            notification_color=$(echo "$result" | grep "::" | cut -d':' -f2)
            ;;
        custom|*)
            notification_title="${title:-GitHub 通知}"
            notification_desc="${message:-${desc}}"
            ;;
    esac
    
    # 输出或发送
    if [[ "$dry_run" == "true" ]]; then
        echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
        echo -e "${BLUE}║  📝 预览通知                                     ║${NC}"
        echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${YELLOW}目标：${target}${NC}"
        echo -e "${YELLOW}标题：${notification_title}${NC}"
        echo -e "${CYAN}描述：${notification_desc}${NC}"
        echo -e "${YELLOW}颜色：${notification_color}${NC}"
    else
        send_notification "$target" "$notification_title" "$notification_desc" "$notification_color" "$icon"
    fi
}

# 主函数
main() {
    check_jq
    
    local command="${1:-help}"
    shift || true
    
    case "$command" in
        discord)
            process_args "discord" "$@"
            ;;
        dingtalk)
            process_args "dingtalk" "$@"
            ;;
        telegram)
            process_args "telegram" "$@"
            ;;
        slack)
            process_args "slack" "$@"
            ;;
        all)
            process_args "all" "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}❌ 未知命令：${command}${NC}"
            echo ""
            show_help
            ;;
    esac
}

main "$@"
